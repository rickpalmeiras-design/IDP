"""Gera dados/dashboard_data.json para o painel `painel/classico_da_ia.html`.

Este script faz o mesmo que o `auditoria_e_fluxos.py` (vindo da outra conversa), mas
partindo do que este repositório realmente tem: `data/processed/pnadc_transicoes.parquet`,
o painel já agregado em células. O `auditoria_e_fluxos.py` espera um painel de microdados
individuais (`data/painel_final.parquet`), que não existe aqui e que a Seção 3.2 da
dissertação diz que não é trazido para o ambiente local.

A agregação não atrapalha: cada célula guarda trimestre, ocupação de origem e de destino,
condição no destino, AIOE dos dois lados, o peso somado e o número de transições. Tudo o
que o painel mostra são médias ponderadas, então basta somar pesos por célula em vez de
por pessoa. O número de observações de cada casa é a soma da coluna `n`.

    uv run python storytelling-de-dados/consultas/gera_dashboard_data.py

Saídas: storytelling-de-dados/dados/dashboard_data.json, no formato que o `valida()` do HTML
exige, e o mesmo conteúdo já embutido no bloco `<script id="dados-embutidos">` do painel.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PAINEL = RAIZ / 'data' / 'processed' / 'pnadc_transicoes.parquet'
PASTA = Path(__file__).resolve().parents[1]
SAIDA = PASTA / 'dados' / 'dashboard_data.json'
HTML = PASTA / 'painel' / 'classico_da_ia.html'
ABRE = '<script id="dados-embutidos" type="application/json">'
FECHA = '</script>'

# ----------------------------- decisões do recorte -----------------------------
# Trimestre de origem da transição. A janela completa é a da dissertação (27 trimestres).
# Para reproduzir o recorte do briefing da outra conversa, troque para (2021, 1).
PRIMEIRO = (2019, 1)
POS_INICIO = (2023, 1)      # pós começa no primeiro trimestre inteiro depois do lançamento
EXCLUIR = [(2022, 4)]       # trimestre do lançamento do ChatGPT (30/11/2022): fora da comparação
# Coleta remota da PNAD Contínua. O painel marca 2020T2 a 2021T2 em `coleta_atipica`; a série
# trimestral mostra a medida quebrada de 2020T1 a 2021T3 (a taxa cai quase pela metade e volta
# em 2021T4). Esses trimestres ficam fora das médias pré/pós, senão a comparação pré × pós vira
# medida por telefone contra medida presencial. Continuam na série, sinalizados, para aparecerem
# no gráfico. Para incluí-los nas médias, basta trocar para False.
FORA_DAS_MEDIAS_COLETA_REMOTA = True
TELEFONE = [(2020, 1), (2020, 2), (2020, 3), (2020, 4), (2021, 1), (2021, 2), (2021, 3)]
N_Q = 4                     # quartis de exposição
N_MIN = 30                  # células com menos observações são sinalizadas

GRUPOS = {
    '0': 'Forças armadas e policiais', '1': 'Dirigentes e gerentes',
    '2': 'Profissionais das ciências e intelectuais', '3': 'Técnicos de nível médio',
    '4': 'Apoio administrativo', '5': 'Serviços e vendas',
    '6': 'Agropecuária', '7': 'Indústria, construção e ofícios',
    '8': 'Operadores de máquinas', '9': 'Ocupações elementares',
}
DEST = ['Mesmo grupo', 'Outro grupo', 'Desocupado', 'Fora da força']
COLUNAS = ['ano', 'trimestre', 'pareado', 'cod_origem', 'cod_destino', 'condicao_destino',
           'aioe_origem', 'aioe_destino', 'peso_total', 'n', 'coleta_atipica']


def t_de(ano, tri):
    return ano * 4 + tri - 1


def wquantiles(x, w, qs):
    """Mesma função do auditoria_e_fluxos.py, para os cortes saírem idênticos."""
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    cw = np.cumsum(w) / w.sum()
    return np.interp(qs, cw, x)


def grupo_de(cod):
    s = pd.to_numeric(cod, errors='coerce')
    g = s.dropna().astype(int).astype(str).str.zfill(4).str[0].map(GRUPOS)
    return g.reindex(cod.index)


def carregar():
    df = pd.read_parquet(PAINEL, columns=COLUNAS)
    df['t'] = t_de(df.ano, df.trimestre)
    excl = {t_de(a, q) for a, q in EXCLUIR}
    t_pos = t_de(*POS_INICIO)
    df['periodo'] = np.where(df.t.isin(excl), 'excluído',
                             np.where(df.t >= t_pos, 'pós', 'pré'))
    df['tri_lbl'] = df.ano.astype(str) + 'T' + df.trimestre.astype(str)
    df['coleta_remota'] = df.t.isin({t_de(a, q) for a, q in TELEFONE})
    return df


def transicoes(df):
    """Pares válidos: reencontrados no painel, ocupados na origem e com AIOE na origem."""
    p = df[df.pareado & df.aioe_origem.notna() & df.condicao_destino.notna()
           & (df.periodo != 'excluído') & (df.t >= t_de(*PRIMEIRO))].copy()
    p['nas_medias'] = ~(p.coleta_remota & FORA_DAS_MEDIAS_COLETA_REMOTA)
    p['grupo'] = grupo_de(p.cod_origem)
    p['grupo1'] = grupo_de(p.cod_destino)

    pre = p[(p.periodo == 'pré') & p.nas_medias]
    cortes = wquantiles(pre.aioe_origem.to_numpy(), pre.peso_total.to_numpy(),
                        np.linspace(0, 1, N_Q + 1)[1:-1])
    p['q'] = 'Q' + (np.searchsorted(cortes, p.aioe_origem, side='right') + 1).astype(str)
    p['q1'] = np.where(p.aioe_destino.notna(),
                       'Q' + (np.searchsorted(cortes, p.aioe_destino.fillna(0),
                                              side='right') + 1).astype(str), None)
    p['destino'] = np.select(
        [p.condicao_destino == 'desocupado', p.condicao_destino == 'inativo',
         p.grupo1 == p.grupo],
        ['Desocupado', 'Fora da força', 'Mesmo grupo'], default='Outro grupo')
    return p, cortes


def matriz(p, linha, col, extra=()):
    k = [*extra, linha]
    m = p.pivot_table(index=k, columns=col, values='peso_total', aggfunc='sum', fill_value=0)
    n = p.groupby(k, observed=True)['n'].sum().rename('n_obs')
    return (100 * m.div(m.sum(axis=1), axis=0)).round(2).join(n)


def media_p(sub, mascara):
    return round(100 * float(np.average(mascara, weights=sub.peso_total)), 2)


def fluxos(p_todos):
    p = p_todos[p_todos.nas_medias]
    A = matriz(p, 'q', 'destino', ('periodo',)).reindex(columns=DEST + ['n_obs'], fill_value=0)
    dA = (A.loc['pós', DEST] - A.loc['pré', DEST]).round(2)

    muda = p[p.destino == 'Outro grupo']
    B = matriz(muda, 'q', 'grupo1', ('periodo',))

    dir_ = muda[muda.q1.notna()].copy()
    dir_['direcao'] = np.select([dir_.q1 > dir_.q, dir_.q1 < dir_.q],
                                ['Mais exposta', 'Menos exposta'], 'Mesmo quartil')
    D = matriz(dir_, 'q', 'direcao', ('periodo',))

    extremos = p_todos[p_todos.q.isin(['Q1', f'Q{N_Q}'])]
    linhas = []
    for (lbl, q), sub in extremos.groupby(['tri_lbl', 'q'], observed=True):
        linhas.append({
            'tri_lbl': lbl, 'q': q,
            'pct_muda_grupo': media_p(sub, (sub.destino == 'Outro grupo').to_numpy()),
            'pct_vai_desocupado': media_p(sub, (sub.destino == 'Desocupado').to_numpy()),
            'pct_sai_forca': media_p(sub, (sub.destino == 'Fora da força').to_numpy()),
            'n_obs': int(sub.n.sum()),
            'coleta_remota': bool(sub.coleta_remota.iloc[0]),
            'nas_medias': bool(sub.nas_medias.iloc[0]),
        })
    E = pd.DataFrame(linhas)

    mp = muda[muda.periodo == 'pós']
    nq = max(mp.t.nunique(), 1)
    S = (mp.groupby(['grupo', 'grupo1'], observed=True).peso_total.sum() / nq / 1e3).round(1)
    S = S[S > 0].sort_values(ascending=False).head(25).reset_index()
    S.columns = ['origem', 'destino', 'mil_pessoas_por_trimestre']
    return A, dA, B, D, E, S


def auditoria(df, p):
    """O que dá para auditar em células. Pareamento, cobertura do AIOE e buracos do painel."""
    tri = df.groupby(['ano', 'trimestre'], observed=True).agg(
        obs=('n', 'sum'), pop_mi=('peso_total', lambda w: w.sum() / 1e6),
        pct_pareado=('pareado', 'mean'))
    primeiro, ultimo = tri.index[0], tri.index[-1]
    peso_sem_aioe = df.loc[df.aioe_origem.isna(), 'peso_total'].sum() / df.peso_total.sum()
    usados = p[p.periodo != 'excluído']
    r = {
        'trimestres': f'{primeiro[0]}T{primeiro[1]} a {ultimo[0]}T{ultimo[1]}',
        'celulas': int(len(df)),
        'transicoes_no_painel': int(df.n.sum()),
        'transicoes_usadas': int(usados.n.sum()),
        'pct_pareado': round(100 * float(df.loc[df.pareado, 'n'].sum() / df.n.sum()), 2),
        'pct_peso_origem_sem_aioe': round(100 * float(peso_sem_aioe), 2),
        'trimestres_de_coleta_atipica': sorted(
            df.loc[df.coleta_atipica, 'tri_lbl'].unique().tolist()),
        'obs_por_trimestre': tri.round(2).reset_index().to_dict('records'),
        'unidade': 'célula de transição (pessoa-trimestre agregada); n é o número de pares',
        'origem_dos_dados': 'data/processed/pnadc_transicoes.parquet, o mesmo painel da Tabela 4',
    }
    alertas = []
    baixo = tri[tri.pct_pareado < 0.80]
    if len(baixo):
        alertas.append(f'{len(baixo)} trimestres com pareamento abaixo de 80%: '
                       + ', '.join(f'{a}T{q}' for a, q in baixo.index))
    if r['pct_peso_origem_sem_aioe'] > 5:
        alertas.append('Mais de 5% do peso na origem sem AIOE — revisar o crosswalk.')
    if r['trimestres_de_coleta_atipica']:
        alertas.append('Coleta majoritariamente por telefone em '
                       + ', '.join(r['trimestres_de_coleta_atipica'])
                       + ': a taxa medida de mudança de ocupação cai por mudança de medida, '
                         'não por mudança no mercado.')
    alertas.append('Auditoria de identidade (duplicatas id×trimestre, sexo e idade '
                   'inconsistentes) não roda aqui: é feita no ambiente remoto, antes da '
                   'agregação. O que chega ao disco local já vem em células.')
    r['alertas'] = alertas
    return r


def veredito_var(E, qmax):
    """Replica em Python o cálculo que o HTML faz no gráfico do VAR."""
    corte = t_de(2022, 4)
    ordem = E.tri_lbl.str.slice(0, 4).astype(int) * 4 + E.tri_lbl.str.slice(5).astype(int)
    E = E.assign(ordem=ordem)
    E = E[E.nas_medias]
    sv = E[E.q == qmax].set_index('ordem').pct_muda_grupo.sort_index()
    sm = E[E.q == 'Q1'].set_index('ordem').pct_muda_grupo.sort_index()
    gap_pre = sv[sv.index < corte].mean() - sm[sm.index < corte].mean()
    gap_pos = sv[sv.index > corte].mean() - sm[sm.index > corte].mean()
    incl = lambda s: np.polyfit(s.index.to_numpy(float), s.to_numpy(float), 1)[0]
    d_incl = incl(sv[sv.index < corte]) - incl(sm[sm.index < corte])
    return {'gap_pre_pp': round(float(gap_pre), 2), 'gap_pos_pp': round(float(gap_pos), 2),
            'diferenca_de_inclinacao_pre': round(float(d_incl), 4),
            'veredito': 'lance limpo' if abs(d_incl) < 0.03 else 'lance duvidoso'}


def embutir(texto):
    """Escreve o JSON dentro do bloco <script id="dados-embutidos"> do painel.

    Evita o copia e cola do passo 5 do briefing: o HTML fica sempre com o mesmo
    conteúdo do arquivo em dados/.
    """
    s = HTML.read_text(encoding='utf-8')
    i = s.index(ABRE) + len(ABRE)
    j = s.index(FECHA, i)
    corpo = '\n' + texto.strip() + '\n'
    HTML.write_text(s[:i] + corpo + s[j:], encoding='utf-8')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    df = carregar()
    p, cortes = transicoes(df)
    A, dA, B, D, E, S = fluxos(p)
    aud = auditoria(df, p)
    qmax = f'Q{N_Q}'

    rec = lambda t: json.loads(t.reset_index().to_json(orient='records', force_ascii=False))
    dados = {
        'meta': {
            'titulo': 'Clássico da IA — PNAD Contínua × exposição à inteligência artificial',
            'fonte': 'PNAD Contínua trimestral (IBGE), via Base dos Dados; índice AIOE de '
                     'Felten, Raj e Seamans (2021)',
            'gerado_por': 'storytelling-de-dados/consultas/gera_dashboard_data.py',
            'base': 'data/processed/pnadc_transicoes.parquet (painel agregado em células)',
            'janela': aud['trimestres'],
            'pos_inicio': list(POS_INICIO),
            'excluidos': [list(e) for e in EXCLUIR],
            'cortes_quartis_aioe': [round(float(c), 4) for c in cortes],
            'n_transicoes': int(p[p.nas_medias].n.sum()),
            'trimestres_fora_das_medias': [f'{a}T{q}' for a, q in TELEFONE]
                                          if FORA_DAS_MEDIAS_COLETA_REMOTA else [],
            'n_min_celula': N_MIN,
            'amostra': 'pessoas de 18 a 65 anos, ocupadas na origem, reencontradas no '
                       'trimestre seguinte; peso amostral da origem',
            'aviso_de_uso': 'Material da disciplina de storytelling de dados. Descritivo: '
                            'não é o resultado estimado da dissertação e não afirma causalidade.',
        },
        'auditoria': aud,
        'destino_por_quartil': rec(A),
        'dif_pos_pre': rec(dA),
        'grupo_destino': rec(B),
        'direcao_exposicao': rec(D),
        'serie_q1_q4': json.loads(E.to_json(orient='records', force_ascii=False)),
        'sankey_pos': json.loads(S.to_json(orient='records', force_ascii=False)),
    }
    dados['meta']['veredito_var'] = veredito_var(E, qmax)
    texto = json.dumps(dados, ensure_ascii=False, indent=1)
    SAIDA.write_text(texto, encoding='utf-8')
    embutir(texto)

    print(f'fora das médias (coleta remota): {int(p[~p.nas_medias].n.sum()):,} transições'
          .replace(',', '.'))
    placar_v = A.loc[('pós', qmax), 'Outro grupo']
    placar_m = A.loc[('pós', 'Q1'), 'Outro grupo']
    print(f'{SAIDA.name}: {SAIDA.stat().st_size / 1024:.1f} KB, embutido em {HTML.name}')
    print(f'transições nas médias: {int(p[p.nas_medias].n.sum()):,}'.replace(',', '.'))
    print(f'cortes dos quartis (AIOE): {[round(float(c), 3) for c in cortes]}')
    print(f'placar pós — Verdão {qmax} {placar_v:.1f} x {placar_m:.1f} Mengão Q1')
    print('diferença pós − pré (p.p.):')
    print(dA.to_string())
    print('VAR:', dados['meta']['veredito_var'])
    pequenas = A[A.n_obs < N_MIN]
    if len(pequenas):
        print(f'ATENÇÃO: {len(pequenas)} células com n < {N_MIN}')
    for a in aud['alertas']:
        print('- ' + a)


if __name__ == '__main__':
    main()
