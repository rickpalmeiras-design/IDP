"""Etapa 05: LPM de transições e matriz de mobilidade entre quintis de exposição.

Desenho: diferenças-em-diferenças com tratamento contínuo. O choque é o lançamento
público do ChatGPT (config.yaml: choque); a intensidade é o AIOE da ocupação de origem.
O coeficiente de interesse é sempre `aioe_origem:pos`.

A estimação roda em Python com pyfixest (mesma sintaxe de fórmula do fixest em R,
incluindo o operador `^` para efeitos fixos interagidos). A versão R equivalente fica
arquivada em R/legado/modelos.R como gabarito histórico: os coeficientes dos dois
motores foram comparados termo a termo e batem a ruído de ponto flutuante.
"""
import hashlib
import json
import numpy as np
import pandas as pd
import duckdb
import pyfixest as pf
from scipy import stats
from .config import CFG, INTERIM, PROCESSED, MODELS, WORK
from .common import json_write, table, note, required

CONTROLES = 'idade + idade_quadrado'
CATEGORIAS_LISTA = ['sexo', 'raca', 'escolaridade', 'tempo_emprego_categoria',
                     'tamanho_empresa_categoria', 'setor']
CATEGORIAS = ' + '.join(CATEGORIAS_LISTA)
FORMULA = ('{y} ~ aioe_origem:pos + telework:pos + ' + CONTROLES +
           ' | cod_origem + sigla_uf^mes + ' + CATEGORIAS)


def write_data(frame, path):
    """Grava a base de estimação com o escritor vetorizado do DuckDB."""
    with duckdb.connect() as con:
        con.execute('SET threads=2')
        con.register('dados_exportar', frame)
        con.execute(f"COPY dados_exportar TO '{path.as_posix()}' (HEADER)")


def estimar_pyfixest(job):
    """Reestima os desfechos pendentes com pyfixest.

    Categorias ausentes viram a categoria 'ignorado' (a célula não é descartada em
    silêncio), igual à versão R. O erro-padrão é o cluster-robusto (`CRV1`) do próprio
    fit; por cima dele, uma camada conservadora recalcula os graus de liberdade como
    (nº de UPAs efetivamente usadas na amostra do modelo, após NA e singleton de FE)
    menos 1, e reaplica p-valor e IC95 com t-Student nesses graus — mesma lógica de
    R/legado/modelos.R.
    """
    if not CFG['estimacao']['autorizada']:
        raise PermissionError('Estimacao nao autorizada na configuracao.')
    d = pd.read_csv(job['dados'], low_memory=False)
    if 'pos' in d:
        d['pos'] = d['pos'].astype(float)
    for v in CATEGORIAS_LISTA:
        if v in d:
            d[v] = d[v].astype('string').fillna('ignorado').astype('category')

    resultados = []
    for item in job['modelos']:
        name = f"{job['nome']}_{item['nome']}"
        modelo = pf.feols(item['formula'], data=d, weights=job['pesos'],
                          vcov={'CRV1': job['cluster']})
        used_upa = d.loc[modelo._data.index, job['cluster']]
        df_cluster = int(used_upa.nunique()) - 1

        tidy = modelo.tidy().reset_index()
        out = pd.DataFrame({
            'termo': tidy['Coefficient'], 'estimativa': tidy['Estimate'],
            'erro_padrao': tidy['Std. Error'], 'estatistica': tidy['t value'],
            'p_valor': tidy['Pr(>|t|)'], 'n': int(modelo._N), 'modelo': name})
        out['erro_padrao_conservador'] = out['erro_padrao']
        out['graus_liberdade_conservador'] = df_cluster
        out['p_valor_conservador'] = 2 * stats.t.sf(
            np.abs(out.estimativa / out.erro_padrao_conservador), df=df_cluster)
        tcrit = stats.t.ppf(1 - job['alpha'] / 2, df_cluster)
        out['ic95_inferior_conservador'] = out.estimativa - tcrit * out.erro_padrao_conservador
        out['ic95_superior_conservador'] = out.estimativa + tcrit * out.erro_padrao_conservador
        out.to_csv(MODELS / f'{name}.csv', index=False)

        vcov = pd.DataFrame(modelo._vcov, index=modelo._coefnames, columns=modelo._coefnames)
        vcov.to_csv(MODELS / f'{name}_vcov.csv', index_label='')

        json_write(MODELS / f'{name}_metadados.json', {
            'formula': item['formula'], 'n': int(modelo._N), 'cluster': job['cluster'],
            'pesos': job['pesos'], 'clusters': df_cluster + 1,
            'pacote': f'pyfixest {pf.__version__}',
            'observacoes_entrada': int(len(d)), 'sha256_dados': job['sha256_dados']})

        table(out, name)
        resultados.append(f'{name}.csv')
    return resultados


def fit_job(name, data, formulas, cluster, weights):
    """Só reestima o que mudou: fórmula, cluster, pesos ou hash dos dados."""
    with open(data, 'rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    pending = []
    for item in formulas:
        meta = MODELS / f"{name}_{item['nome']}_metadados.json"
        if meta.exists():
            old = json.loads(meta.read_text(encoding='utf-8'))
            if (old.get('sha256_dados') == digest and old.get('formula') == item['formula']
                    and old.get('cluster') == cluster and (old.get('pesos') or None) == weights):
                continue
        pending.append(item)
    if not pending:
        return []
    return estimar_pyfixest({'nome': name, 'dados': str(data), 'modelos': pending,
                             'sha256_dados': digest, 'cluster': cluster, 'pesos': weights,
                             'alpha': CFG['estimacao']['alpha']})


def matriz_transicao(d, quintis, bootstrap, seed):
    """Matriz de mobilidade entre quintis de AIOE, com bootstrap de UPA conjunto pré/pós.

    Os quintis são fixos entre códigos ocupacionais (não entre pessoas), de modo que a
    composição do emprego não redefine as faixas entre os períodos.
    """
    valid = d[d.pareado.eq(1) & d.aioe_origem.notna() & d.aioe_destino.notna()].copy()
    score = d[['cod_origem', 'aioe_origem']].drop_duplicates().aioe_origem.dropna()
    bins = np.unique(np.quantile(score, np.linspace(0, 1, quintis + 1)))
    bins[0], bins[-1] = -np.inf, np.inf
    valid['q_origem'] = pd.cut(valid.aioe_origem, bins, labels=False) + 1
    valid['q_destino'] = pd.cut(valid.aioe_destino, bins, labels=False) + 1
    counts = valid.groupby(['pos', 'q_origem', 'q_destino'], observed=True).peso_total.sum().reset_index()
    counts['probabilidade'] = counts.peso_total / counts.groupby(['pos', 'q_origem']).peso_total.transform('sum')
    table(counts, '05_matriz_transicao')
    grouped = valid.groupby(['id_upa', 'pos', 'q_origem', 'q_destino'], observed=True).peso_total.sum().unstack(
        ['pos', 'q_origem', 'q_destino'], fill_value=0)
    rng = np.random.default_rng(seed)
    q = len(bins) - 1
    cells = pd.MultiIndex.from_product([[False, True], range(1, q + 1), range(1, q + 1)])
    g = grouped.reindex(columns=cells, fill_value=0).to_numpy()
    samples = []
    for _ in range(bootstrap):
        w = rng.multinomial(len(g), np.full(len(g), 1 / len(g)))
        a = (w @ g).reshape(2, q, q)
        den = a.sum(axis=2, keepdims=True)
        prob = np.divide(a, den, out=np.full_like(a, np.nan), where=den > 0)
        samples.append((prob[1] - prob[0]).ravel())
    boot = np.array(samples)
    point = g.sum(axis=0).reshape(2, q, q)
    point = point / point.sum(axis=2, keepdims=True)
    delta = (point[1] - point[0]).ravel()
    table(pd.DataFrame({'origem': np.repeat(np.arange(1, q + 1), q), 'destino': np.tile(np.arange(1, q + 1), q),
                        'diferenca_pos_pre': delta, 'erro_bootstrap_upa': np.nanstd(boot, axis=0, ddof=1),
                        'ic025': np.nanquantile(boot, .025, axis=0),
                        'ic975': np.nanquantile(boot, .975, axis=0)}), '05_diferencas_matriz')
    cov = np.cov(boot, rowvar=False)
    rank = int(np.linalg.matrix_rank(cov))
    chi = float(delta @ np.linalg.pinv(cov) @ delta)
    json_write(MODELS / '05_igualdade_matrizes.json', {'qui_quadrado_wald_cluster': chi,
                                                       'graus_liberdade': rank,
                                                       'p_valor': float(stats.chi2.sf(chi, rank))})
    return len(samples)


def stage05():
    d = pd.read_parquet(required(PROCESSED / 'pnadc_transicoes.parquet'))
    if 'telework' not in d:
        # Painel construído antes de o teletrabalho entrar na etapa 04: mapeia aqui, mesma fonte.
        exposure = pd.read_parquet(required(INTERIM / 'exposicao_cod.parquet')).set_index('cod')
        d['telework'] = d.cod_origem.map(exposure.telework.to_dict())
    d['mes'] = pd.to_datetime(d.data).dt.strftime('%Y-%m')
    for c in CFG['estimacao']['desfechos']:
        d[c] = d[c].astype('Float64')
    path = WORK / '05_pnadc.csv'
    write_data(d, path)
    jobs = [{'nome': y, 'formula': FORMULA.format(y=y)} for y in CFG['estimacao']['desfechos']]
    fit_job('05_pnadc', path, jobs, cluster='id_upa', weights='peso_total')
    draws = matriz_transicao(d, CFG['estimacao']['quintis'], CFG['estimacao']['bootstrap'], CFG['seed'])
    note('05', 'LPM ponderado pela soma de V1028 nas celulas; regressoras e desfechos sao constantes dentro '
               'de cada celula, o que preserva coeficientes e scores do cluster UPA. Pesos sao transversais. '
               'A matriz usa quintis fixos entre codigos ocupacionais, bootstrap de UPA conjunto pre/pos e '
               'teste de Wald com a covariancia do bootstrap. Alta/baixa AIOE e direcao de exposicao, nao '
               'mobilidade salarial.')
    return {'modelos': len(jobs), 'bootstrap': draws}
