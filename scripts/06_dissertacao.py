"""Regenera as tabelas e as figuras da dissertação a partir das saídas já estimadas.

Faz parte da etapa 06 e roda sozinho: não toca no BigQuery nem reestima nada.
"""
import _bootstrap
from src.dissertacao import gera

if __name__ == '__main__':
    resultado = gera()
    for nome in resultado['tabelas']:
        print(f'tabela  dissertacao/tabelas/{nome}.tex')
    for nome in resultado['figuras']:
        print(f'figura  dissertacao/figuras/{nome}')
