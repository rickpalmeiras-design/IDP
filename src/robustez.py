"""Etapa 07: robustezes do resultado principal, para avaliar antes de levar à dissertação.

Três exercícios sobre exatamente a mesma base da etapa 05 (o CSV que ela grava, conferido
pelo hash registrado nos metadados da Tabela 4):
(a) sem os trimestres de origem com coleta telefônica atípica;
(b) inferência com agrupamento na ocupação de origem e em ocupação e UPA, com correção de
    multiplicidade na família dos sete desfechos;
(c) estudo de evento, trocando a interação única com o pós por uma interação por trimestre
    relativo ao marco.
Nada aqui escreve em dissertacao/: tudo vai para output/robustez/.
"""
import hashlib
import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import pyfixest as pf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from scipy import stats
from .config import CFG, MODELS, WORK, ROBUSTEZ
from .common import note, required
from .estimacao import FORMULA, CONTROLES, CATEGORIAS, CATEGORIAS_LISTA

TERMO = 'aioe_origem:pos'
ALPHA = CFG['estimacao']['alpha']
FORMULA_EVENTO = ('{y} ~ i(rel, aioe_origem, ref=-1) + i(rel, telework, ref=-1) + ' + CONTROLES +
                  ' | cod_origem + sigla_uf^mes + ' + CATEGORIAS)
# Mesma ordem e mesmos rótulos da Tabela 4, para a comparação ler na mesma sequência.
ROTULOS = {
    'mobilidade_descendente_aioe': 'Transição para menor AIOE',
    'muda_ocupacao_3': 'Muda de ocupação (3 dígitos)',
    'muda_ocupacao_2': 'Muda de ocupação (2 dígitos)',
    'sai_do_emprego': 'Saída do emprego',
    'pareado': 'Pareamento (teste de atrito)',
    'formal_para_informal': 'Transição de formal para informal',
    'mobilidade_ascendente_aioe': 'Transição para maior AIOE',
}
AGRUPAMENTOS = {'upa': ['id_upa'], 'ocupacao': ['cod_origem'],
                'ocupacao_upa': ['cod_origem', 'id_upa']}
NOME_AGRUPAMENTO = {'upa': 'UPA', 'ocupacao': 'ocupação', 'ocupacao_upa': 'ocupação e UPA'}
TINTA = {'superficie': '#fcfcfb', 'primaria': '#0b0b0b', 'secundaria': '#52514e',
         'suave': '#898781', 'grade': '#e1e0d9', 'eixo': '#c3c2b7', 'faixa': '#f0efec'}
SERIE = '#2a78d6'


def _idx_choque():
    choque = pd.Timestamp(CFG['choque'])
    return choque.year * 4 + choque.quarter - 1


def trimestre(k):
    i = k + _idx_choque()
    return f'{i // 4}T{i % 4 + 1}'


def carregar():
    """Mesma base e mesma preparação da etapa 05."""
    path = required(WORK / '05_pnadc.csv')
    with open(path, 'rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    # Os artefatos 07b antigos rodaram sobre outra base; aqui a comparação só vale com a mesma.
    esperado = json.loads((MODELS / '05_pnadc_pareado_metadados.json')
                          .read_text(encoding='utf-8'))['sha256_dados']
    if digest != esperado:
        raise ValueError('O CSV de estimação não é o que gerou a Tabela 4; rode a etapa 05 antes da 07.')
    d = pd.read_csv(path, low_memory=False)
    d['pos'] = d['pos'].astype(float)
    d['coleta_atipica'] = d['coleta_atipica'].astype(bool)
    for v in CATEGORIAS_LISTA:
        d[v] = d[v].astype('string').fillna('ignorado').astype('category')
    d['rel'] = (d.ano * 4 + d.trimestre - 1) - _idx_choque()
    return d, digest


def baseline():
    return {y: pd.read_csv(required(MODELS / f'05_pnadc_{y}.csv')).set_index('termo').loc[TERMO]
            for y in ROTULOS}


def linha(b, ep, df, n, g):
    t = stats.t.ppf(1 - ALPHA / 2, df)
    return {'coef': b, 'ep': ep, 'ic_inf': b - t * ep, 'ic_sup': b + t * ep,
            'p': float(2 * stats.t.sf(abs(b / ep), df)), 'n': n, 'clusters': g}


def clusters_usados(modelo, coluna):
    # _data já é a amostra do ajuste (após NA e singleton); consultar pelo índice falha em recortes.
    return int(modelo._data[coluna].nunique())


def resumo(modelo, clusters):
    """Camada conservadora da etapa 05: t com G − 1 graus, G = clusters efetivamente usados
    (no agrupamento em duas vias, o menor dos dois, como no ajuste do próprio pyfixest)."""
    g = min(clusters_usados(modelo, c) for c in clusters)
    return linha(float(modelo.coef()[TERMO]), float(modelo.se()[TERMO]), g - 1, int(modelo._N), g)


def holm(p):
    p = np.asarray(p, float)
    n, ajuste, acumulado = len(p), np.empty(len(p)), 0.0
    for i, j in enumerate(np.argsort(p)):
        acumulado = max(acumulado, (n - i) * p[j])
        ajuste[j] = min(1.0, acumulado)
    return ajuste


def bh(p):
    p = np.asarray(p, float)
    n, ajuste, acumulado = len(p), np.empty(len(p)), 1.0
    for i, j in enumerate(np.argsort(p)[::-1]):
        acumulado = min(acumulado, p[j] * n / (n - i))
        ajuste[j] = acumulado
    return ajuste


def comparar(base, rob, nome):
    rows = []
    for y, r in rob.items():
        b0 = float(base[y].estimativa)
        rows.append({'variavel': y, 'desfecho': ROTULOS[y], 'coef_baseline_pp': 100 * b0,
                     'coef_robustez_pp': 100 * r['coef'], 'ep_pp': 100 * r['ep'],
                     'ic95_inf_pp': 100 * r['ic_inf'], 'ic95_sup_pp': 100 * r['ic_sup'],
                     'p_valor': r['p'], 'n': r['n'], 'clusters': r['clusters'],
                     'variacao_magnitude_pct': 100 * (abs(r['coef']) / abs(b0) - 1),
                     'sinal_invertido': bool(np.sign(r['coef']) != np.sign(b0))})
    frame = pd.DataFrame(rows)
    frame.to_csv(ROBUSTEZ / f'{nome}.csv', index=False)
    return frame


def sem_coleta(d):
    s = d[~d.coleta_atipica]
    out = {}
    for y in ROTULOS:
        m = pf.feols(FORMULA.format(y=y), data=s, weights='peso_total', vcov={'CRV1': 'id_upa'})
        out[y] = resumo(m, ['id_upa'])
    return out


def inferencia(d):
    """Um ajuste por desfecho; o agrupamento muda só a variância, não o coeficiente."""
    out = {k: {} for k in AGRUPAMENTOS}
    for y in ROTULOS:
        m = pf.feols(FORMULA.format(y=y), data=d, weights='peso_total', vcov={'CRV1': 'id_upa'})
        for k, cols in AGRUPAMENTOS.items():
            m = m.vcov({'CRV1': '+'.join(cols)})
            out[k][y] = resumo(m, cols)
    return out


def multiplicidade(inf):
    tab = pd.DataFrame({'variavel': list(ROTULOS), 'desfecho': list(ROTULOS.values())})
    for k in AGRUPAMENTOS:
        p = [inf[k][y]['p'] for y in ROTULOS]
        tab[f'p_{k}'], tab[f'holm_{k}'], tab[f'bh_{k}'] = p, holm(p), bh(p)
    tab.to_csv(ROBUSTEZ / 'b3_multiplicidade.csv', index=False)
    return tab


def evento(d):
    """Referência em k = −1. Resume o pós pela média simples dos k ≥ 0 e testa o pré (k ≤ −2)
    em conjunto, ambos com a covariância cluster-robusta do próprio ajuste."""
    coefs, medias, pre = [], {}, {}
    for y in ROTULOS:
        m = pf.feols(FORMULA_EVENTO.format(y=y), data=d, weights='peso_total',
                     vcov={'CRV1': 'id_upa'})
        g = clusters_usados(m, 'id_upa')
        nomes = list(m._coefnames)
        b = pd.Series(np.asarray(m.coef()), index=nomes)
        v = pd.DataFrame(m._vcov, index=nomes, columns=nomes)
        chave = {int(n.split('::')[1].split(':')[0]): n for n in nomes if n.endswith(':aioe_origem')}
        t = stats.t.ppf(1 - ALPHA / 2, g - 1)
        for k, n in sorted(chave.items()):
            ep = float(np.sqrt(v.loc[n, n]))
            coefs.append({'variavel': y, 'desfecho': ROTULOS[y], 'k': k, 'trimestre': trimestre(k),
                          'coef_pp': 100 * b[n], 'ep_pp': 100 * ep,
                          'ic95_inf_pp': 100 * (b[n] - t * ep), 'ic95_sup_pp': 100 * (b[n] + t * ep)})
        coefs.append({'variavel': y, 'desfecho': ROTULOS[y], 'k': -1, 'trimestre': trimestre(-1),
                      'coef_pp': 0.0, 'ep_pp': 0.0, 'ic95_inf_pp': 0.0, 'ic95_sup_pp': 0.0})
        ante = [chave[k] for k in sorted(chave) if k <= -2]
        bp = b[ante].to_numpy()
        f = float(bp @ np.linalg.solve(v.loc[ante, ante].to_numpy(), bp)) / len(ante)
        pre[y] = {'F': f, 'gl': len(ante), 'p': float(stats.f.sf(f, len(ante), g - 1))}
        depois = [chave[k] for k in sorted(chave) if k >= 0]
        w = np.full(len(depois), 1 / len(depois))
        media = float(w @ b[depois].to_numpy())
        ep_media = float(np.sqrt(w @ v.loc[depois, depois].to_numpy() @ w))
        medias[y] = linha(media, ep_media, g - 1, int(m._N), g)
    tab = pd.DataFrame(coefs).sort_values(['variavel', 'k'])
    tab.to_csv(ROBUSTEZ / 'c_estudo_evento_coeficientes.csv', index=False)
    pd.DataFrame([{'variavel': y, 'desfecho': ROTULOS[y], **pre[y]} for y in ROTULOS]).to_csv(
        ROBUSTEZ / 'c_estudo_evento_pretendencia.csv', index=False)
    return tab, medias, pre


def _n(v, casas=3, sinal=False):
    return (f'{v:+.{casas}f}' if sinal else f'{v:.{casas}f}').replace('-', '−').replace('.', ',')


def _p(v):
    return '<0,001' if v < 0.001 else _n(v)


def _p_frase(v):
    return 'p < 0,001' if v < 0.001 else f'p = {_n(v)}'


def _cientifico(v):
    return f'{v:.1e}'.replace('.', ',').replace('-', '−')


def _mil(v):
    return f'{int(v):,}'.replace(',', '.')


def figura(tab, pre, atipicos):
    plt.rcParams.update({'font.family': ['Segoe UI', 'DejaVu Sans']})
    fig, axes = plt.subplots(4, 2, figsize=(8.5, 11), facecolor=TINTA['superficie'])
    for i, (ax, y) in enumerate(zip(axes.flat, ROTULOS)):
        s = tab[tab.variavel == y].sort_values('k')
        ax.set_facecolor(TINTA['superficie'])
        ax.axvspan(min(atipicos) - 0.5, max(atipicos) + 0.5, color=TINTA['faixa'], lw=0, zorder=0)
        ax.axhline(0, color=TINTA['eixo'], lw=1, zorder=1)
        ax.axvline(-0.5, color=TINTA['secundaria'], lw=1, zorder=1)
        ax.vlines(s.k, s.ic95_inf_pp, s.ic95_sup_pp, color=SERIE, lw=1, zorder=2)
        ax.plot(s.k, s.coef_pp, 'o', color=SERIE, ms=5, mec=TINTA['superficie'], mew=1.2, zorder=3)
        ax.set_title(ROTULOS[y], loc='left', fontsize=9.5, color=TINTA['primaria'],
                     fontweight='bold', pad=15)
        ax.text(0, 1.02, f'pré-tendência: F = {_n(pre[y]["F"], 2)}, {_p_frase(pre[y]["p"])}',
                transform=ax.transAxes, fontsize=7.5, color=TINTA['secundaria'], va='bottom')
        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _n(v, 1)))
        ax.set_xticks(range(-15, 12, 5))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _n(v, 0)))
        ax.grid(axis='y', color=TINTA['grade'], lw=0.8)
        ax.set_axisbelow(True)
        for lado in ('top', 'right', 'left'):
            ax.spines[lado].set_visible(False)
        ax.spines['bottom'].set_color(TINTA['eixo'])
        ax.tick_params(colors=TINTA['suave'], labelsize=7.5, length=0)
        if i % 2 == 0:
            ax.set_ylabel('p.p.', color=TINTA['suave'], fontsize=8)
        if i >= 5:
            ax.set_xlabel('trimestre relativo ao marco (k)', color=TINTA['suave'], fontsize=8)
    nota = axes.flat[7]
    nota.axis('off')
    nota.text(0, 0.95, '\n'.join([
        'Pontos: coeficiente de AIOE × trimestre relativo, em p.p.',
        'Barras: IC 95% (cluster UPA, t com G − 1 graus).',
        f'Referência: k = −1 ({trimestre(-1)}), fixado em zero.',
        f'Linha vertical: marco (k = 0, {trimestre(0)}).',
        f'Faixa cinza: coleta telefônica ({trimestre(min(atipicos))}–{trimestre(max(atipicos))}).',
        'F: teste conjunto dos coeficientes pré (k ≤ −2).',
        'As escalas verticais diferem entre painéis.']),
        va='top', fontsize=8, color=TINTA['secundaria'], linespacing=1.7)
    fig.suptitle('Estudo de evento: AIOE × trimestre relativo ao lançamento do ChatGPT',
                 x=0.06, ha='left', fontsize=11, color=TINTA['primaria'], fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(ROBUSTEZ / 'fig_estudo_evento.pdf', facecolor=TINTA['superficie'])
    fig.savefig(ROBUSTEZ / 'fig_estudo_evento.png', dpi=150, facecolor=TINTA['superficie'])
    plt.close(fig)


def _md_comparacao(frame):
    linhas = ['| Desfecho | Coef. baseline (p.p.) | Coef. robustez (p.p.) | EP (p.p.) | IC 95% '
              '| p-valor | N | Clusters | Variação da magnitude |',
              '| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |']
    for r in frame.itertuples():
        var = _n(r.variacao_magnitude_pct, 1, sinal=True) + '%'
        if r.sinal_invertido:
            var += ' (sinal invertido)'
        linhas.append(f'| {r.desfecho} | {_n(r.coef_baseline_pp, sinal=True)} '
                      f'| {_n(r.coef_robustez_pp, sinal=True)} | {_n(r.ep_pp)} '
                      f'| [{_n(r.ic95_inf_pp, sinal=True)}; {_n(r.ic95_sup_pp, sinal=True)}] '
                      f'| {_p(r.p_valor)} | {_mil(r.n)} | {_mil(r.clusters)} | {var} |')
    return '\n'.join(linhas)


def _md_multiplicidade(tab):
    linhas = ['| Desfecho | ' + ' | '.join(f'p ({NOME_AGRUPAMENTO[k]}) | Holm | BH' for k in AGRUPAMENTOS) + ' |',
              '| --- |' + ' ---: |' * 3 * len(AGRUPAMENTOS)]
    for r in tab.itertuples():
        celulas = []
        for k in AGRUPAMENTOS:
            celulas += [_p(getattr(r, f'p_{k}')), _p(getattr(r, f'holm_{k}')), _p(getattr(r, f'bh_{k}'))]
        linhas.append(f'| {r.desfecho} | ' + ' | '.join(celulas) + ' |')
    return '\n'.join(linhas)


def relatorio(digest, validacao, atipicos, tabs, mult, pre):
    pre_md = ['| Desfecho | F | gl | p-valor |', '| --- | ---: | ---: | ---: |']
    pre_md += [f'| {ROTULOS[y]} | {_n(pre[y]["F"], 2)} | {pre[y]["gl"]} | {_p(pre[y]["p"])} |'
               for y in ROTULOS]
    texto = f"""# Robustezes do resultado principal

Gerado por `scripts/07_robustez.py` em {datetime.now(timezone.utc).date()}. Revisão interna:
nada aqui foi levado à dissertação.

- Base: o mesmo CSV da etapa 05 (SHA-256 `{digest[:12]}…`, conferido contra os metadados da Tabela 4).
- Motor: pyfixest {pf.__version__}, mesmos pesos (`peso_total`) e mesmos efeitos fixos da Tabela 4.
- Inferência conservadora como na Tabela 4: t com G − 1 graus de liberdade, G = número de clusters
  efetivamente usados (no agrupamento em duas vias, o menor dos dois).
- Coeficientes e EP em pontos percentuais. **Variação da magnitude** = |β robustez| / |β Tabela 4| − 1.
- **Reprodução da Tabela 4** dentro desta etapa (mesma especificação, cluster UPA): maior diferença
  de coeficiente {_cientifico(validacao['coef'])} p.p. e de EP {_cientifico(validacao['ep'])} p.p.;
  número de clusters idêntico em todos os desfechos: {'sim' if validacao['clusters'] else 'não'}.

## (a) Sem coleta telefônica atípica

Exclui os trimestres de origem {trimestre(min(atipicos))} a {trimestre(max(atipicos))} ({len(atipicos)}
trimestres), marcados por `coleta_atipica` na etapa 04. Mesma especificação, cluster UPA.

{_md_comparacao(tabs['a'])}

## (b) Inferência

Mesmo ajuste da Tabela 4; muda só o agrupamento dos erros-padrão. O coeficiente é idêntico por
construção, então a variação da magnitude é zero e o que importa são EP, IC e p-valor.

### (b1) Cluster na ocupação de origem

{_md_comparacao(tabs['b1'])}

### (b2) Cluster em duas vias: ocupação e UPA

{_md_comparacao(tabs['b2'])}

### (b3) Correção para multiplicidade

Família: os sete desfechos, para o termo AIOE × pós. Holm controla a taxa de erro por família;
Benjamini-Hochberg (BH), a taxa de falsas descobertas. O pareamento é um teste de atrito, e mantê-lo
na família torna a correção mais conservadora, não menos.

{_md_multiplicidade(mult)}

## (c) Estudo de evento

A interação única AIOE × pós vira uma interação por trimestre relativo ao marco, com referência em
k = −1 ({trimestre(-1)}); a teletrabalhabilidade é interagida da mesma forma. Cluster UPA.

A coluna **coef. robustez** é a média simples dos coeficientes pós (k ≥ 0, {trimestre(0)} em diante),
medida contra k = −1. Não é o mesmo estimando da Tabela 4, que compara o pós com a média de todo o
pré: se houver tendência no pré, as duas divergem, e a divergência é informativa em si.

{_md_comparacao(tabs['c'])}

### Pré-tendências

Teste F conjunto de que todos os coeficientes pré (k ≤ −2) são zero.

{chr(10).join(pre_md)}

![Estudo de evento](fig_estudo_evento.png)

## Arquivos

- `a_sem_coleta_atipica.csv`, `b1_cluster_ocupacao.csv`, `b2_cluster_ocupacao_upa.csv`,
  `c_estudo_evento_media_pos.csv` — as tabelas comparativas acima, em formato de dados.
- `b3_multiplicidade.csv` — p-valores brutos e ajustados.
- `c_estudo_evento_coeficientes.csv` — os coeficientes por trimestre (a tabela por trás da figura).
- `c_estudo_evento_pretendencia.csv` — o teste conjunto do pré.
- `fig_estudo_evento.pdf` / `.png`.
"""
    (ROBUSTEZ / 'ROBUSTEZ.md').write_text(texto, encoding='utf-8')


def stage07():
    d, digest = carregar()
    base = baseline()
    atipicos = sorted(int(k) for k in d.loc[d.coleta_atipica, 'rel'].unique())
    tabs = {'a': comparar(base, sem_coleta(d), 'a_sem_coleta_atipica')}
    inf = inferencia(d)
    tabs['b1'] = comparar(base, inf['ocupacao'], 'b1_cluster_ocupacao')
    tabs['b2'] = comparar(base, inf['ocupacao_upa'], 'b2_cluster_ocupacao_upa')
    validacao = {
        'coef': float(max(abs(100 * (inf['upa'][y]['coef'] - base[y].estimativa)) for y in ROTULOS)),
        'ep': float(max(abs(100 * (inf['upa'][y]['ep'] - base[y].erro_padrao_conservador)) for y in ROTULOS)),
        'clusters': bool(all(inf['upa'][y]['clusters'] == base[y].graus_liberdade_conservador + 1
                             for y in ROTULOS))}
    mult = multiplicidade(inf)
    tab_evento, medias, pre = evento(d)
    tabs['c'] = comparar(base, medias, 'c_estudo_evento_media_pos')
    figura(tab_evento, pre, atipicos)
    relatorio(digest, validacao, atipicos, tabs, mult, pre)
    note('07', 'Robustezes sobre a mesma base da Tabela 4 (hash conferido): sem os trimestres de origem '
               'de coleta telefonica, inferencia com cluster em ocupacao e em ocupacao e UPA com correcao '
               'de Holm e BH na familia dos sete desfechos, e estudo de evento com referencia no trimestre '
               'anterior ao marco. Saidas em output/robustez; nada foi levado a dissertacao.')
    return {'modelos': 3 * len(ROTULOS), 'reproducao_tabela4': validacao,
            'trimestres_atipicos': [trimestre(k) for k in atipicos]}
