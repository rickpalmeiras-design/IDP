"""Gera dados/dados_painel.json a partir dos CSV de dados/.

Roda sozinho, sem tocar no pipeline da dissertação:

    uv run python storytelling-de-dados/consultas/gera_json.py

Tudo o que o painel precisa fica em um único arquivo, com números já no formato de
exibição (porcentagem com uma casa, pontos percentuais com duas) e com os avisos que o
painel é obrigado a mostrar.
"""
import json
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parents[1] / 'dados'
SAIDA = PASTA / 'dados_painel.json'

ROTULOS = {
    'pareado': 'Foi reencontrado no painel',
    'muda_ocupacao_2': 'Muda de ocupação (2 dígitos)',
    'muda_ocupacao_3': 'Muda de ocupação (3 dígitos)',
    'sai_do_emprego': 'Sai do emprego',
    'formal_para_informal': 'De formal para informal',
    'mobilidade_descendente_aioe': 'Vai para ocupação menos exposta',
    'mobilidade_ascendente_aioe': 'Vai para ocupação mais exposta',
}

AVISOS = [
    'O estudo mede associação condicional, não causalidade: o período contém muitas '
    'outras mudanças além da inteligência artificial.',
    'Exposição não é hierarquia: AIOE menor significa menos exposição à inteligência '
    'artificial, e não emprego pior ou salário menor.',
    'O aumento geral de mobilidade aparece também em quem não tem exposição nenhuma, '
    'então ele não pode ser atribuído à inteligência artificial.',
    'Em 2020 e 2021 a PNAD Contínua foi coletada majoritariamente por telefone e a taxa '
    'medida de mudança de ocupação cai de forma abrupta, provavelmente por mudança de '
    'medida.',
    'A medida de exposição é de 2021, anterior à difusão dos modelos generativos, e o '
    'estudo não observa salários.',
]

TELAS = [
    {'n': 1, 'titulo': 'A pergunta',
     'mensagem': 'A inteligência artificial vai acabar com empregos? O marco é o '
                 'lançamento público do ChatGPT, em 30 de novembro de 2022.',
     'numero_destaque': '30 nov 2022', 'dados': []},
    {'n': 2, 'titulo': 'Como medir exposição',
     'mensagem': 'O índice AIOE liga aplicações de inteligência artificial às habilidades '
                 'exigidas por cada ocupação. De um lado, financeiro e jurídico; do outro, '
                 'construção, cozinha e campo.',
     'numero_destaque': '+1,45 contra −1,73', 'dados': ['ocupacoes_destaque']},
    {'n': 3, 'titulo': 'Quem é exposto no Brasil',
     'mensagem': 'A exposição alta atinge uma fatia pequena do emprego brasileiro.',
     'numero_destaque': '62% abaixo da média', 'dados': ['distribuicao_aioe']},
    {'n': 4, 'titulo': 'O que aconteceu depois de 2022',
     'mensagem': 'A mobilidade ocupacional subiu para todo mundo.',
     'numero_destaque': '23,6% para 31,8%', 'dados': ['agregados']},
    {'n': 5, 'titulo': 'A virada',
     'mensagem': 'O aumento é geral, inclusive entre quem não tem exposição. O que sobra, '
                 'ao comparar ocupações com exposições diferentes, é um gradiente pequeno e '
                 'no sentido da recomposição, não da destruição.',
     'numero_destaque': '+2,19 p.p.', 'dados': ['coeficientes']},
    {'n': 6, 'titulo': 'O que ainda não sabemos',
     'mensagem': 'Limitações do estudo.',
     'numero_destaque': None, 'dados': ['avisos']},
]


def pct(x, casas=1):
    return None if pd.isna(x) else round(float(x) * 100, casas)


def main():
    dez = pd.read_csv(PASTA / 'dez_ocupacoes.csv', encoding='utf-8-sig')
    todas = pd.read_csv(PASTA / 'exposicao_por_ocupacao.csv', encoding='utf-8-sig')
    desc = pd.read_csv(PASTA / 'descritivas_desfechos.csv', encoding='utf-8-sig')
    coef = pd.read_csv(PASTA / 'coeficientes.csv', encoding='utf-8-sig')

    ocupacoes = []
    for r in dez.itertuples():
        ocupacoes.append({
            'grupo': r.grupo,
            'cod': str(r.cod).zfill(4),
            'ocupacao': r.ocupacao,
            'aioe': round(float(r.aioe), 2),
            'teletrabalhabilidade': round(float(r.teletrabalhabilidade), 2),
            'trabalhadores': int(r.trabalhadores_media_trimestral),
            'taxas': {
                'muda_ocupacao': {'pre': pct(r.muda_ocup_pre), 'pos': pct(r.muda_ocup_pos)},
                'vai_para_menos_exposta': {'pre': pct(r.desce_gradiente_pre, 2),
                                           'pos': pct(r.desce_gradiente_pos, 2)},
                'sai_do_emprego': {'pre': pct(r.sai_emprego_pre), 'pos': pct(r.sai_emprego_pos)},
            },
        })

    total_trab = float(todas.trabalhadores_media_trimestral.sum())
    grupos = {}
    for g in ('Mais expostas', 'Menos expostas'):
        s = dez[dez.grupo == g].trabalhadores_media_trimestral.sum()
        grupos[g] = {'trabalhadores': int(s), 'share_pct': round(100 * s / total_trab, 2)}

    faixas = [(-3.0, -1.5), (-1.5, -1.0), (-1.0, -0.5), (-0.5, 0.0),
              (0.0, 0.5), (0.5, 1.0), (1.0, 1.5)]
    distribuicao = []
    for lo, hi in faixas:
        sub = todas[(todas.aioe >= lo) & (todas.aioe < hi)]
        distribuicao.append({
            'faixa': f'{lo:+.1f} a {hi:+.1f}',
            'min': lo, 'max': hi,
            'ocupacoes': int(len(sub)),
            'trabalhadores': int(sub.trabalhadores_media_trimestral.sum()),
            'share_pct': round(100 * sub.trabalhadores_media_trimestral.sum() / total_trab, 1),
        })

    agregados = []
    for var, sub in desc.groupby('variavel', sort=False):
        pre = sub[sub.periodo == 'Pre'].media_ponderada.iloc[0]
        pos = sub[sub.periodo == 'Pos'].media_ponderada.iloc[0]
        agregados.append({
            'desfecho': ROTULOS.get(var, var), 'chave': var,
            'pre_pct': pct(pre), 'pos_pct': pct(pos),
            'variacao_pp': round(100 * (pos - pre), 1),
        })

    coeficientes = []
    for r in coef[coef.termo == 'AIOE x pos'].itertuples():
        coeficientes.append({
            'desfecho': r.desfecho, 'chave': r.variavel,
            'efeito_pp': round(float(r.efeito_pp), 2),
            'erro_padrao_pp': round(float(r.erro_padrao_pp), 3),
            'ic95': [round(float(r.ic95_inferior_pp), 2), round(float(r.ic95_superior_pp), 2)],
            'p_valor': float(f'{r.p_valor:.4g}'),
            'significativo_5pct': bool(r.p_valor < 0.05),
        })

    painel = {
        'meta': {
            'titulo': 'Inteligência artificial e mobilidade ocupacional no Brasil',
            'fonte': 'PNAD Contínua trimestral (IBGE), via Base dos Dados; índice AIOE de '
                     'Felten, Raj e Seamans (2021)',
            'janela': '2019T1 a 2025T3',
            'marco': '2022-11-30',
            'primeiro_trimestre_pos': '2022T4',
            'transicoes_observadas': 4017289,
            'ocupacoes_na_estimacao': 413,
            'desvio_padrao_aioe': 0.9445,
            'correlacao_aioe_teletrabalho': 0.702,
            'unidades': {
                'taxas': 'porcentagem',
                'efeitos': 'pontos percentuais por unidade de AIOE',
                'trabalhadores': 'média por trimestre, soma dos pesos amostrais dividida por 27',
            },
            'aviso_de_uso': 'Material de aula. Não é texto da dissertação e não substitui os '
                            'resultados oficiais do trabalho.',
        },
        'numeros_chave': {
            'trabalhadores_na_base': int(total_trab),
            'share_aioe_negativo_pct': round(
                100 * todas.loc[todas.aioe < 0, 'trabalhadores_media_trimestral'].sum()
                / total_trab, 1),
            'grupos_destaque': grupos,
            'criterio_selecao': 'cinco maiores e cinco menores AIOE entre as ocupações com ao '
                                'menos 100 mil trabalhadores',
        },
        'ocupacoes_destaque': ocupacoes,
        'distribuicao_aioe': distribuicao,
        'agregados': agregados,
        'coeficientes': coeficientes,
        'avisos': AVISOS,
        'telas': TELAS,
    }

    SAIDA.write_text(json.dumps(painel, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{SAIDA.name}: {SAIDA.stat().st_size / 1024:.1f} KB, '
          f'{len(ocupacoes)} ocupações, {len(agregados)} agregados, '
          f'{len(coeficientes)} coeficientes')


if __name__ == '__main__':
    main()
