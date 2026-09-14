"""Etapa 06: tabelas de síntese, figuras e relatório do paper.

Nada aqui reestima: tudo lê `output/modelos` e o painel, e monta o material final.
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .config import CFG, INTERIM, PROCESSED, MODELS, TABLES, FIGURES, REPORT
from .common import table, json_write, note, required
from .dissertacao import gera

ROTULOS = {
    'pareado': 'pareamento entre entrevistas (teste de atrito)',
    'muda_ocupacao_2': 'mudanca de ocupacao (2 digitos)',
    'muda_ocupacao_3': 'mudanca de ocupacao (3 digitos)',
    'sai_do_emprego': 'saida do emprego',
    'formal_para_informal': 'transicao formal para informal',
    'mobilidade_descendente_aioe': 'transicao para ocupacao de menor AIOE',
    'mobilidade_ascendente_aioe': 'transicao para ocupacao de maior AIOE',
}
TERMOS = {'aioe_origem:pos': 'AIOE x pos', 'telework:pos': 'Teletrabalho x pos'}


def coeficientes():
    """Junta os modelos em uma tabela única, já em pontos percentuais."""
    rows = []
    for y, rotulo in ROTULOS.items():
        path = MODELS / f'05_pnadc_{y}.csv'
        if not path.exists():
            continue
        d = pd.read_csv(path)
        meta = json.loads((MODELS / f'05_pnadc_{y}_metadados.json').read_text(encoding='utf-8'))
        for termo, nome in TERMOS.items():
            r = d[d.termo.eq(termo)]
            if r.empty:
                continue
            r = r.iloc[0]
            rows.append({'desfecho': rotulo, 'variavel': y, 'termo': nome,
                         'efeito_pp': 100 * r.estimativa, 'erro_padrao_pp': 100 * r.erro_padrao_conservador,
                         'ic95_inferior_pp': 100 * r.ic95_inferior_conservador,
                         'ic95_superior_pp': 100 * r.ic95_superior_conservador,
                         'p_valor': r.p_valor_conservador, 'n_celulas': int(r.n),
                         'clusters_upa': meta.get('clusters')})
    result = pd.DataFrame(rows)
    table(result, '06_coeficientes_principais')
    table(result[result.termo.eq('AIOE x pos')].drop(columns='termo'), '06_efeitos_aioe')
    return result


def auditoria():
    """Ficha de cada modelo: fórmula, amostra, cluster e hash dos dados que rodaram."""
    rows = []
    for y in ROTULOS:
        path = MODELS / f'05_pnadc_{y}_metadados.json'
        if not path.exists():
            continue
        meta = json.loads(path.read_text(encoding='utf-8'))
        rows.append({'modelo': f'05_pnadc_{y}', 'n': meta['n'], 'formula': meta['formula'],
                     'cluster': meta['cluster'], 'pesos': meta['pesos'], 'clusters': meta.get('clusters'),
                     'motor': meta.get('pacote'), 'sha256_dados': meta['sha256_dados']})
    result = pd.DataFrame(rows)
    table(result, '06_auditoria_modelos')
    return result


def descritivas():
    d = pd.read_parquet(required(PROCESSED / 'pnadc_transicoes.parquet'))
    rows = []
    for y in CFG['estimacao']['desfechos']:
        for periodo, sel in [('Pre', ~d.pos), ('Pos', d.pos)]:
            s = d.loc[sel, [y, 'peso_total']].dropna()
            rows.append({'variavel': y, 'periodo': periodo, 'celulas': len(s),
                         'media_ponderada': float(np.average(s[y].astype(float), weights=s.peso_total))
                         if len(s) else np.nan})
    # A escala da exposição vem da tabela por COD, não do painel: uma linha por ocupação.
    exposure = pd.read_parquet(required(INTERIM / 'exposicao_cod.parquet')).rename(
        columns={'aioe': 'aioe_origem'}).dropna(subset=['aioe_origem'])
    w = d.dropna(subset=['aioe_origem'])
    media = float(np.average(w.aioe_origem, weights=w.peso_total))
    resumo = pd.DataFrame(rows)
    table(resumo, '06_descritivas_desfechos')
    escala = pd.DataFrame([
        {'medida': 'AIOE entre ocupacoes (COD)', 'n': len(exposure), 'media': exposure.aioe_origem.mean(),
         'desvio_padrao': exposure.aioe_origem.std(), 'minimo': exposure.aioe_origem.min(),
         'maximo': exposure.aioe_origem.max()},
        {'medida': 'AIOE ponderado por trabalhador', 'n': len(exposure), 'media': media,
         'desvio_padrao': float(np.sqrt(np.average((w.aioe_origem - media) ** 2, weights=w.peso_total))),
         'minimo': exposure.aioe_origem.min(), 'maximo': exposure.aioe_origem.max()},
        {'medida': 'Teletrabalho entre ocupacoes (COD)', 'n': int(exposure.telework.notna().sum()),
         'media': exposure.telework.mean(), 'desvio_padrao': exposure.telework.std(),
         'minimo': exposure.telework.min(), 'maximo': exposure.telework.max()}])
    table(escala, '06_escala_exposicao')
    correlacao = float(exposure[['aioe_origem', 'telework']].corr().iloc[0, 1])
    json_write(MODELS / '06_correlacao_aioe_telework.json', {'pearson_entre_cod': correlacao})
    return resumo, escala, correlacao


def figuras():
    pares = pd.read_parquet(required(INTERIM / 'pnadc_taxa_pareamento.parquet')).sort_values(['ano', 'trimestre'])
    pares['periodo'] = pares.ano.astype(str) + 'T' + pares.trimestre.astype(str)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(pares.periodo, pares.taxa_pareamento, marker='o')
    ax.axhline(CFG['limite_pareamento'], color='black', ls='--', lw=1, label='limite de referencia')
    choque = pd.Timestamp(CFG['choque']).to_period('Q')
    ax.axvline(f'{choque.year}T{choque.quarter}', color='crimson', ls=':', label='choque')
    ax.set(ylabel='Taxa de pareamento', xlabel='Trimestre de origem')
    ax.tick_params(axis='x', rotation=90)
    ax.legend()
    fig.tight_layout(); fig.savefig(FIGURES / 'fig_taxa_pareamento.pdf'); plt.close(fig)

    coef = pd.read_csv(TABLES / '06_coeficientes_principais.csv')
    coef = coef[coef.termo.eq('AIOE x pos')].sort_values('efeito_pp')
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(coef))
    ax.errorbar(coef.efeito_pp, y, xerr=[coef.efeito_pp - coef.ic95_inferior_pp,
                                         coef.ic95_superior_pp - coef.efeito_pp],
                fmt='o', capsize=3)
    ax.axvline(0, color='black', lw=1)
    ax.set_yticks(y); ax.set_yticklabels(coef.desfecho)
    ax.set_xlabel('Efeito de AIOE x pos (pontos percentuais por unidade de AIOE)')
    fig.tight_layout(); fig.savefig(FIGURES / 'fig_coeficientes_aioe.pdf'); plt.close(fig)

    dif = pd.read_csv(TABLES / '05_diferencas_matriz.csv')
    q = int(dif.origem.max())
    grid = dif.pivot(index='origem', columns='destino', values='diferenca_pos_pre').to_numpy()
    fig, ax = plt.subplots(figsize=(6, 5))
    lim = np.nanmax(np.abs(grid))
    im = ax.imshow(grid, cmap='RdBu_r', vmin=-lim, vmax=lim)
    ax.set_xticks(range(q), [f'Q{i+1}' for i in range(q)])
    ax.set_yticks(range(q), [f'Q{i+1}' for i in range(q)])
    ax.set(xlabel='Quintil de AIOE de destino', ylabel='Quintil de AIOE de origem')
    for i in range(q):
        for k in range(q):
            ax.text(k, i, f'{100*grid[i, k]:+.1f}', ha='center', va='center', fontsize=8)
    fig.colorbar(im, ax=ax, label='Diferenca pos - pre')
    fig.tight_layout(); fig.savefig(FIGURES / 'fig_matriz_diferencas.pdf'); plt.close(fig)

    exposure = pd.read_parquet(required(INTERIM / 'exposicao_cod.parquet'))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(exposure.aioe.dropna(), bins=25)
    ax.set(xlabel='AIOE por codigo ocupacional (COD)', ylabel='Ocupacoes')
    fig.tight_layout(); fig.savefig(FIGURES / 'fig_distribuicao_aioe.pdf'); plt.close(fig)
    return sorted(p.name for p in FIGURES.glob('*.pdf'))


def relatorio(coef, escala, correlacao):
    wald = json.loads((MODELS / '05_igualdade_matrizes.json').read_text(encoding='utf-8'))
    pareamento = pd.read_parquet(INTERIM / 'pnadc_taxa_pareamento.parquet')
    cobertura = json.loads((INTERIM / 'pnadc_cobertura_exposicao.json').read_text(encoding='utf-8'))
    dif = pd.read_csv(TABLES / '05_diferencas_matriz.csv')
    diagonal = dif[dif.origem.eq(dif.destino)]
    aioe = coef[coef.termo.eq('AIOE x pos')].sort_values('efeito_pp', ascending=False)
    linhas = '\n'.join(
        f'| {r.desfecho} | {r.efeito_pp:+.3f} | [{r.ic95_inferior_pp:+.3f}; {r.ic95_superior_pp:+.3f}] | '
        f'{r.p_valor:.3g} | {r.n_celulas:,} |'.replace(',', '.') for r in aioe.itertuples())
    texto = f"""# Exposição ocupacional à IA e transições de trabalho na PNAD Contínua

Gerado pela etapa 06. Todos os números vêm de `output/modelos` e `output/tabelas`.

## Desenho

Painel de transições trimestrais da PNADC ({CFG['inicio_pnadc']} em diante), pessoas ocupadas de
{CFG['idade_minima_pnadc']} a {CFG['idade_maxima_pnadc']} anos. Diferenças-em-diferenças com tratamento
contínuo: o choque é {CFG['choque']} e a intensidade é o AIOE da ocupação de origem.

Especificação comum aos {len(ROTULOS)} desfechos:

```
y ~ aioe_origem:pos + telework:pos + idade + idade_quadrado
    | cod_origem + sigla_uf^mes + sexo + raca + escolaridade
    + tempo_emprego_categoria + tamanho_empresa_categoria + setor
```

Pesos: soma de V1028 da entrevista de origem (transversal). Cluster: UPA.
AIOE é padronizado entre ocupações (desvio-padrão {escala.iloc[0].desvio_padrao:.3f}); os coeficientes
são reportados por unidade de AIOE, o que equivale a cerca de um desvio-padrão de exposição.

## Qualidade do painel

- Taxa de pareamento por trimestre: {pareamento.taxa_pareamento.min():.3f} a {pareamento.taxa_pareamento.max():.3f}
  (limite de referência {CFG['limite_pareamento']}; os trimestres abaixo são os de coleta atípica de 2020-2021).
- Peso sem AIOE atribuído: {100*cobertura['sem_match_ponderado']:.2f}%.
- Correlação AIOE-teletrabalho entre ocupações: {correlacao:.3f}. Por isso o teletrabalho entra
  interagido com o pós em todos os modelos.

## Efeitos de AIOE x pós (pontos percentuais por unidade de AIOE)

| Desfecho | Efeito | IC95 | p | N células |
| --- | --- | --- | --- | --- |
{linhas}

## Matriz de mobilidade entre quintis de AIOE

Diferença pós menos pré na diagonal (permanência no mesmo quintil):
{', '.join(f"Q{int(r.origem)} {100*r.diferenca_pos_pre:+.1f} p.p." for r in diagonal.itertuples())}.

Teste de Wald de igualdade das matrizes pré e pós: qui-quadrado {wald['qui_quadrado_wald_cluster']:.1f},
{wald['graus_liberdade']} graus de liberdade, p = {wald['p_valor']:.3g}.

## Como interpretar

1. Os coeficientes são gradientes por unidade de AIOE, por transição trimestral. Não são
   percentuais de trabalhadores afetados pela IA.
2. AIOE menor não significa emprego pior: é direção de exposição, não hierarquia salarial.
3. Parte da assimetria entre mobilidade ascendente e descendente é mecânica, porque quem parte de
   AIOE alto tem mais destinos possíveis abaixo. O efeito fixo absorve o nível dessa assimetria, mas
   não sua interação com um aumento geral de mobilidade; o contraste pós menos pré por quintil é
   informativo, mas não isola a direção do movimento de seu volume.
4. Não há adoção de IA observada. O tratamento é um índice ocupacional e o choque é único e nacional:
   qualquer fator que tenha atingido ocupações de alto AIOE de forma diferencial no mesmo período
   entra no coeficiente. A queda de permanência em todos os quintis mostra que parte do movimento é
   comum ao mercado de trabalho do período.
5. A seleção longitudinal não está resolvida. O peso é transversal da origem e não há correção de
   atrito; o modelo de `pareado` é um teste de atrito, não uma prova de ausência de seleção.

## Limites

Ponte COD-ISCO-SOC com repartição uniforme entre SOC, resolução de dois dígitos no grupo 6 e sem
atribuição a militares. AIOE e teletrabalho são medidas americanas aplicadas à estrutura ocupacional
brasileira. O horizonte de cada transição é de um trimestre: efeitos mais lentos não aparecem aqui.
"""
    (REPORT / 'RELATORIO.md').write_text(texto, encoding='utf-8')
    return texto


def stage06():
    coef = coeficientes()
    fichas = auditoria()
    _, escala, correlacao = descritivas()
    arquivos = figuras()
    relatorio(coef, escala, correlacao)
    indice = pd.DataFrame([{'tabela': p.stem, 'linhas': len(pd.read_csv(p))}
                           for p in sorted(TABLES.glob('*.csv')) if not p.stem.startswith('06_indice')])
    table(indice, '06_indice_tabelas')
    dissertacao = gera()
    note('06', 'Tabelas de sintese, figuras e relatorio gerados a partir dos modelos salvos. Efeitos '
               'convertidos para pontos percentuais; a inferencia e a mesma do pyfixest com cluster de UPA.')
    return {'modelos_lidos': len(fichas), 'figuras': arquivos, 'tabelas': len(indice),
            'dissertacao': dissertacao}
