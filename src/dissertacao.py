"""Tabelas e figuras da dissertação, geradas a partir das saídas da etapa 05.

Cada tabela sai como um flutuante ABNT completo em `dissertacao/tabelas/`, pronto
para `\\input`, com a mesma legenda, o mesmo rótulo e a mesma nota que o capítulo
já usava. As figuras são copiadas de `output/figuras` para `dissertacao/figuras`.

Nada aqui reestima e nada aqui inventa número: tudo vem de `output/modelos`,
`output/tabelas` e do painel. Os arquivos gerados não devem ser editados à mão.
"""
import json
import shutil

import pandas as pd

from .config import CFG, INTERIM, PROCESSED, MODELS, TABLES, FIGURES, DISS_TABLES, DISS_FIGURES
from .common import note, required

CABECALHO = ('% Gerado por scripts/06_dissertacao.py a partir de output/modelos e output/tabelas.\n'
             '% Não editar à mão: a próxima execução sobrescreve este arquivo.\n')

FONTE = 'Elaboração própria a partir da PNADC/IBGE.'

# Domínio de estimação de cada desfecho: a coluna cuja ausência define quem sai da amostra.
DOMINIOS = [('Todas as origens (pareamento)', 'pareado'),
            ('Pares (saída do emprego)', 'sai_do_emprego'),
            ('Destino ocupado (muda de ocupação)', 'muda_ocupacao_2'),
            ('AIOE nos dois lados (margens direcionais)', 'mobilidade_descendente_aioe'),
            ('Origem formal (informalização)', 'formal_para_informal')]

GRUPOS = [('Continuidade e vínculo', ['pareado', 'sai_do_emprego', 'formal_para_informal']),
          ('Mobilidade ocupacional', ['muda_ocupacao_2', 'muda_ocupacao_3']),
          ('Gradiente de exposição', ['mobilidade_descendente_aioe', 'mobilidade_ascendente_aioe'])]

DESCRITIVAS = {'pareado': 'Pareamento entre entrevistas',
               'sai_do_emprego': 'Saída do emprego',
               'formal_para_informal': 'Transição de formal para informal',
               'muda_ocupacao_2': 'Muda de ocupação (2 dígitos)',
               'muda_ocupacao_3': 'Muda de ocupação (3 dígitos)',
               'mobilidade_descendente_aioe': 'Transição para menor AIOE',
               'mobilidade_ascendente_aioe': 'Transição para maior AIOE'}

# No painel de coeficientes o desfecho de pareamento é lido como teste de atrito.
COEFICIENTES = dict(DESCRITIVAS, pareado='Pareamento (teste de atrito)')


# ---------------------------------------------------------------- formatação

def inteiro(valor):
    """3960585 -> 3.960.585"""
    return f'{int(valor):,}'.replace(',', '.')


def decimal(valor, casas=3):
    """2.187 -> 2,187"""
    return f'{float(valor):.{casas}f}'.replace('.', ',')


def milhar(valor, casas=1):
    """3040.1 -> 3.040,1"""
    return f'{float(valor):,.{casas}f}'.replace(',', '\x00').replace('.', ',').replace('\x00', '.')


def assinado(valor, casas=3):
    """-0.26 -> $-$0,260 (o sinal em modo matemático para não virar hífen)."""
    sinal = '$-$' if float(valor) < 0 else '$+$'
    return sinal + decimal(abs(float(valor)), casas)


def pvalor(valor):
    return '$<$0,001' if float(valor) < 0.001 else decimal(valor, 3)


def extremos(d):
    """Primeiro e último trimestre de origem de um recorte do painel, como 2019T1."""
    periodos = sorted({(int(a), int(t)) for a, t in zip(d.ano, d.trimestre)})
    return f'{periodos[0][0]}T{periodos[0][1]}', f'{periodos[-1][0]}T{periodos[-1][1]}'


def flutuante(nome, legenda, rotulo, alinhamento, linhas, nota):
    """Monta o flutuante ABNT e grava em dissertacao/tabelas/<nome>.tex."""
    corpo = '\n'.join(f'    {linha}' for linha in linhas)
    texto = (f'{CABECALHO}\\begin{{table}}[htb]\n'
             f'  \\caption{{{legenda}}}\n'
             f'  \\label{{{rotulo}}}\n'
             f'  \\centering\n'
             f'  \\espacosimples\\idpcorpodez\n'
             f'  \\begin{{tabular}}{{@{{}}{alinhamento}@{{}}}}\n'
             f'{corpo}\n'
             f'  \\end{{tabular}}\n'
             f'  \\fonte{{{FONTE}}}\n'
             f'  \\nota{{{nota}}}\n'
             f'\\end{{table}}\n')
    (DISS_TABLES / f'{nome}.tex').write_text(texto, encoding='utf-8')
    return nome


def alinha(celulas, larguras):
    """Alinha as colunas do fonte LaTeX para o arquivo continuar legível."""
    partes = [texto.ljust(largura) for texto, largura in zip(celulas, larguras)]
    return ' & '.join(partes).rstrip() + ' \\\\'


# ------------------------------------------------------------------ insumos

def painel():
    """Painel restrito ao domínio comum: exposição e teletrabalho atribuídos à origem."""
    colunas = ['ano', 'trimestre', 'id_upa', 'cod_origem', 'n', 'pos', 'aioe_origem',
               *DESCRITIVAS]
    d = pd.read_parquet(required(PROCESSED / 'pnadc_transicoes.parquet'), columns=colunas)
    exposicao = pd.read_parquet(required(INTERIM / 'exposicao_cod.parquet')).set_index('cod')
    telework = d.cod_origem.map(exposicao.telework.to_dict())
    return d[d.aioe_origem.notna() & telework.notna()]


def metadados():
    fichas = {}
    for y in DESCRITIVAS:
        caminho = MODELS / f'05_pnadc_{y}_metadados.json'
        if caminho.exists():
            fichas[y] = json.loads(caminho.read_text(encoding='utf-8'))
    return fichas


# ------------------------------------------------------------------ tabelas

def tab_escala(base, fichas):
    """Tamanho de cada domínio de estimação: pessoas, células, ocupações e UPAs."""
    linhas = ['\\toprule',
              alinha(['\\textbf{Domínio (desfecho)}', '\\textbf{Pessoas-}', '\\textbf{Células}',
                      '\\textbf{Ocupa-}', '\\textbf{UPAs}'], [42, 12, 12, 10, 0]),
              alinha(['', '\\textbf{transições}', '\\textbf{estimadas}', '\\textbf{ções}', ''],
                     [42, 12, 12, 10, 0]),
              '\\midrule']
    for rotulo, coluna in DOMINIOS:
        d = base[base[coluna].notna()]
        # Pessoas-transições somam o tamanho das células; a célula é a unidade estimada.
        linhas.append(alinha([rotulo, inteiro(d.n.sum()), inteiro(fichas[coluna]['n']),
                              inteiro(d.cod_origem.nunique()), inteiro(d.id_upa.nunique())],
                             [42, 12, 12, 10, 0]))
    linhas.append('\\bottomrule')
    inicio, fim = extremos(base)
    nota = (f'Origens de {inicio} a {fim}. Pessoas-transições não são pessoas únicas: o\n'
            '        mesmo indivíduo contribui com até quatro pares. A coluna de células é o\n'
            '        número de observações efetivamente estimadas em cada modelo.')
    return flutuante('tab_escala', 'Escala dos domínios de estimação', 'tab:escala',
                     'lrrrr', linhas, nota)


def tab_descritivas(base):
    """Médias ponderadas de cada desfecho antes e depois do marco."""
    d = pd.read_csv(required(TABLES / '06_descritivas_desfechos.csv'))
    media = d.pivot(index='variavel', columns='periodo', values='media_ponderada')
    linhas = ['\\toprule',
              alinha(['\\textbf{Desfecho}', '\\textbf{Pré}', '\\textbf{Pós}', '\\textbf{Diferença}'],
                     [37, 5, 5, 0]),
              '\\midrule']
    for posicao, (grupo, desfechos) in enumerate(GRUPOS):
        if posicao:
            linhas.append('\\addlinespace')
        linhas.append(f'\\multicolumn{{4}}{{@{{}}l}}{{\\textit{{{grupo}}}}} \\\\')
        for y in desfechos:
            pre, pos = float(media.loc[y, 'Pre']), float(media.loc[y, 'Pos'])
            linhas.append(alinha([DESCRITIVAS[y], decimal(pre), decimal(pos), assinado(pos - pre)],
                                 [37, 5, 5, 0]))
    linhas.append('\\bottomrule')
    pre_inicio, pre_fim = extremos(base[~base.pos])
    pos_inicio, pos_fim = extremos(base[base.pos])
    nota = (f'Pré: origens de {pre_inicio} a {pre_fim}. Pós: origens de {pos_inicio} a {pos_fim}, pelo\n'
            '        corte da equação~\\eqref{eq:pos}. Médias ponderadas pelo peso amostral da\n'
            '        entrevista de origem, cada uma no domínio próprio do desfecho.')
    return flutuante('tab_descritivas', 'Médias ponderadas dos desfechos, antes e depois do marco',
                     'tab:descritivas', 'lrrr', linhas, nota)


def tab_matriz():
    """Diferença pós menos pré entre as matrizes de mobilidade por quintil de exposição."""
    d = pd.read_csv(required(TABLES / '05_diferencas_matriz.csv'))
    wald = json.loads(required(MODELS / '05_igualdade_matrizes.json').read_text(encoding='utf-8'))
    q = int(d.origem.max())
    grade = d.pivot(index='origem', columns='destino', values='diferenca_pos_pre')
    colunas = ' & '.join(f'\\textbf{{Q{i}}}' for i in range(1, q + 1))
    linhas = ['\\toprule',
              f'\\textbf{{Faixa de origem}} & \\multicolumn{{{q}}}{{c}}'
              f'{{\\textbf{{Faixa de destino (p.p.)}}}} \\\\',
              f'\\cmidrule(l){{2-{q + 1}}}',
              f' & {colunas} \\\\',
              '\\midrule']
    for i in range(1, q + 1):
        rotulo = {1: 'Q1 (menor exposição)', q: f'Q{q} (maior exposição)'}.get(i, f'Q{i}')
        celulas = [assinado(100 * grade.loc[i, k], 2) for k in range(1, q + 1)]
        linhas.append(alinha([rotulo, *celulas], [20] + [8] * (q - 1) + [0]))
    linhas.append('\\bottomrule')
    erro = 100 * d.erro_bootstrap_upa
    nota = ('Faixas fixas entre códigos ocupacionais. Erros-padrão por reamostragem\n'
            f"        de UPA ({CFG['estimacao']['bootstrap']} réplicas) variam entre {decimal(erro.min(), 2)} "
            f'e {decimal(erro.max(), 2)} p.p.; todas as células\n'
            '        têm intervalo de 95\\% que exclui zero. Teste de Wald de igualdade das\n'
            # Em modo matemático a vírgula decimal precisa de chaves para não ganhar espaço.
            f"        matrizes: $\\chi^2 = {milhar(wald['qui_quadrado_wald_cluster']).replace(',', '{,}')}$, "
            f"{wald['graus_liberdade']} graus de liberdade.")
    return flutuante('tab_matriz',
                     'Diferença entre as matrizes de mobilidade pós e pré, por faixa de exposição',
                     'tab:matriz', 'l' + 'r' * q, linhas, nota)


def tab_principal():
    """Painel A (exposição × pós) e painel B (teletrabalhabilidade × pós), mesma estimação."""
    d = pd.read_csv(required(TABLES / '06_coeficientes_principais.csv'))
    larguras = [34, 9, 5, 22, 0]
    linhas = ['\\toprule',
              alinha(['\\textbf{Desfecho}', '\\textbf{Efeito (p.p.)}', '\\textbf{E.P.}',
                      '\\textbf{IC 95\\%}', '\\textbf{$p$}'], larguras),
              '\\midrule']
    # A ordem do painel A, por efeito decrescente, vale também para o painel B.
    ordem = list(d[d.termo.eq('AIOE x pos')].sort_values('efeito_pp', ascending=False).variavel)
    paineis = [('Painel A --- Exposição $\\times$ pós', 'AIOE x pos'),
               ('Painel B --- Teletrabalhabilidade $\\times$ pós', 'Teletrabalho x pos')]
    for posicao, (titulo, termo) in enumerate(paineis):
        if posicao:
            linhas.append('\\addlinespace')
        linhas.append(f'\\multicolumn{{5}}{{@{{}}l}}{{\\textit{{{titulo}}}}} \\\\')
        linhas.append('\\addlinespace[2pt]')
        bloco = d[d.termo.eq(termo)].set_index('variavel')
        for y in ordem:
            r = bloco.loc[y]
            ic = f'[{assinado(r.ic95_inferior_pp)}; {assinado(r.ic95_superior_pp)}]'
            linhas.append(alinha([COEFICIENTES[y], assinado(r.efeito_pp), decimal(r.erro_padrao_pp),
                                  ic, pvalor(r.p_valor)], larguras))
    linhas.append('\\bottomrule')
    grupos = d.clusters_upa
    nota = ('Efeito em pontos percentuais por desvio-padrão de exposição da ocupação\n'
            '        de origem, no painel A, e por unidade do índice de teletrabalhabilidade,\n'
            '        no painel B. Os dois painéis vêm da mesma estimação. Erros-padrão\n'
            f'        agrupados por UPA, entre {inteiro(grupos.min())} e {inteiro(grupos.max())} '
            'grupos conforme o domínio. O\n'
            '        desfecho de pareamento é um teste de atrito: não rejeitar é o resultado\n'
            '        desejável.')
    return flutuante('tab_principal', 'Gradiente de exposição e de teletrabalhabilidade, cenário único',
                     'tab:principal', 'lrrlr', linhas, nota)


# ------------------------------------------------------------------ figuras

def copia_figuras():
    """Leva as figuras da etapa 06 para a pasta que o LaTeX enxerga."""
    copiadas = []
    for origem in sorted(FIGURES.glob('*.pdf')):
        destino = DISS_FIGURES / origem.name
        shutil.copyfile(origem, destino)
        copiadas.append(origem.name)
    return copiadas


def indice(tabelas, figuras):
    """Manifesto do que a pasta contém, para conferência rápida."""
    linhas = ['# Tabelas e figuras da dissertação', '',
              'Gerado por `scripts/06_dissertacao.py`. Não editar à mão.', '',
              '| Arquivo | Rótulo | Onde entra |', '| --- | --- | --- |']
    rotulos = {'tab_escala': ('tab:escala', 'Capítulo 4, escala dos domínios'),
               'tab_descritivas': ('tab:descritivas', 'Capítulo 4, médias pré e pós'),
               'tab_matriz': ('tab:matriz', 'Capítulo 4, matrizes de mobilidade'),
               'tab_principal': ('tab:principal', 'Capítulo 4, resultado principal')}
    for nome in tabelas:
        rotulo, onde = rotulos[nome]
        linhas.append(f'| `tabelas/{nome}.tex` | `{rotulo}` | {onde} |')
    for nome in figuras:
        linhas.append(f'| `figuras/{nome}` | — | `\\includegraphics` nos capítulos 3 e 4 |')
    (DISS_TABLES / 'README.md').write_text('\n'.join(linhas) + '\n', encoding='utf-8')


def gera():
    """Regenera toda a pasta de tabelas e as figuras da dissertação."""
    base = painel()
    fichas = metadados()
    tabelas = [tab_escala(base, fichas), tab_descritivas(base), tab_matriz(), tab_principal()]
    figuras = copia_figuras()
    indice(tabelas, figuras)
    note('06', 'Tabelas da dissertacao regeradas a partir de output/modelos e output/tabelas, em '
               'dissertacao/tabelas, e figuras copiadas para dissertacao/figuras. Os capitulos usam '
               'esses arquivos por \\input: numero de tabela nao e mais digitado a mao.')
    return {'tabelas': tabelas, 'figuras': figuras}
