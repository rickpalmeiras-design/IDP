# -*- coding: utf-8 -*-
"""Extrai da própria dissertação os números que vão para os slides.

Lê as tabelas LaTeX de dissertacao/tabelas/ e o CSV do AIOE por ocupação, e grava
`dados_slides.json`. Os slides não carregam número digitado à mão: se a dissertação
mudar, basta rodar de novo este script e o gerador.

    uv run --with pandas --with numpy python apresentacao/prepara_dados.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

RAIZ = Path(__file__).resolve().parents[1]
TABELAS = RAIZ / 'dissertacao' / 'tabelas'
SAIDA = Path(__file__).resolve().parent / 'dados_slides.json'


def limpa(celula):
    """Tira a marcação LaTeX de uma célula, deixando só o texto."""
    s = celula
    s = s.replace('$+$', '+').replace('$-$', '-').replace('$<$', '<')
    s = re.sub(r'\\textbf\{([^}]*)\}', r'\1', s)
    s = s.replace('\\%', '%').replace('\\\\', '')
    return s.strip()


def numero(s):
    """'3.963.359' -> 3963359 ; '-3,60' -> -3.6 ; '<0,001' fica texto."""
    s = limpa(s)
    if s.startswith('<'):
        return s
    if re.fullmatch(r'[+-]?\d{1,3}(\.\d{3})+', s):
        return int(s.replace('.', ''))
    if re.fullmatch(r'[+-]?\d+(,\d+)?', s):
        return float(s.replace(',', '.'))
    return s


def linhas_de_dados(arquivo):
    """Linhas do corpo de uma tabela: células separadas por &, terminadas em \\\\."""
    texto = (TABELAS / arquivo).read_text(encoding='utf-8')
    texto = '\n'.join(l for l in texto.split('\n') if not l.lstrip().startswith('%'))
    # junta linhas continuadas até o fim de linha da tabela
    bruto = re.findall(r'((?:[^\n]*&[^\n]*)\\\\)', texto)
    return [[c for c in l.split('&')] for l in bruto if 'multicolumn' not in l]


def principal():
    saida = {'A': [], 'B': []}
    painel = 'A'
    texto = (TABELAS / 'tab_principal.tex').read_text(encoding='utf-8')
    for l in texto.split('\n'):
        if 'Painel B' in l:
            painel = 'B'
        if '&' not in l or 'multicolumn' in l or 'textbf' in l:
            continue
        c = l.split('&')
        ic = re.search(r'\[\$?([+-])\$?([\d,]+);\s*\$?([+-])\$?([\d,]+)\]', c[3])
        if not ic:
            continue
        lo = float(ic.group(2).replace(',', '.')) * (-1 if ic.group(1) == '-' else 1)
        hi = float(ic.group(4).replace(',', '.')) * (-1 if ic.group(3) == '-' else 1)
        saida[painel].append({'desfecho': limpa(c[0]), 'efeito': numero(c[1]), 'ep': numero(c[2]),
                              'lo': lo, 'hi': hi, 'p': numero(c[4])})
    return saida


def descritivas():
    saida = []
    for c in linhas_de_dados('tab_descritivas.tex'):
        if len(c) == 4 and isinstance(numero(c[1]), float):
            saida.append({'desfecho': limpa(c[0]), 'pre': numero(c[1]), 'pos': numero(c[2]), 'dif': numero(c[3])})
    return saida


def matriz():
    linhas = []
    for c in linhas_de_dados('tab_matriz.tex'):
        if len(c) == 6 and limpa(c[0]).startswith('Q'):
            linhas.append({'origem': limpa(c[0]), 'valores': [numero(x) for x in c[1:]]})
    return linhas


def escala():
    saida = []
    for c in linhas_de_dados('tab_escala.tex'):
        if len(c) == 5 and isinstance(numero(c[1]), int):
            saida.append({'dominio': limpa(c[0]), 'pessoas_transicoes': numero(c[1]), 'celulas': numero(c[2]),
                          'ocupacoes': int(numero(c[3])), 'upas': numero(c[4])})
    return saida


def aioe():
    d = pd.read_csv(RAIZ / 'storytelling-de-dados' / 'dados' / 'exposicao_por_ocupacao.csv', encoding='utf-8-sig')
    x = d['aioe'].dropna()
    contagens, bordas = np.histogram(x, bins=25)
    return {'n': int(len(x)), 'media': round(float(x.mean()), 4), 'dp': round(float(x.std(ddof=1)), 4),
            'bordas': [round(float(b), 3) for b in bordas], 'contagens': [int(c) for c in contagens]}


def main():
    dados = {'principal': principal(), 'descritivas': descritivas(), 'matriz': matriz(),
             'escala': escala(), 'aioe': aioe()}
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')

    # conferência: o que foi lido, em tela, para comparar com a dissertação
    print('PAINEL A (efeito, IC 95%, p):')
    for r in dados['principal']['A']:
        print(f"  {r['desfecho']:36} {r['efeito']:+7.3f}  [{r['lo']:+.3f}; {r['hi']:+.3f}]  p={r['p']}")
    print('PAINEL B:')
    for r in dados['principal']['B']:
        print(f"  {r['desfecho']:36} {r['efeito']:+7.3f}  [{r['lo']:+.3f}; {r['hi']:+.3f}]  p={r['p']}")
    print('DESCRITIVAS:')
    for r in dados['descritivas']:
        print(f"  {r['desfecho']:36} {r['pre']}  {r['pos']}  {r['dif']}")
    print('MATRIZ (diagonal):', [dados['matriz'][i]['valores'][i] for i in range(len(dados['matriz']))])
    print('ESCALA:')
    for r in dados['escala']:
        print(f"  {r['dominio']:42} {r['pessoas_transicoes']:>10,}  occ={r['ocupacoes']}  upas={r['upas']}")
    a = dados['aioe']
    print(f"AIOE: n={a['n']} media={a['media']} dp={a['dp']} pico={max(a['contagens'])} bins={len(a['contagens'])}")
    print(f'\ngravado em {SAIDA}')


if __name__ == '__main__':
    main()
