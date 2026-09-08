"""Executa o pipeline inteiro, em ordem, com --inicio/--fim para retomar de onde parou."""
import argparse
import _bootstrap
from src.common import run
from src.config import ETAPAS
from src.setup import stage00
from src.dictionaries import stage01
from src.insumos import stage02
from src.pnadc.pareamento import stage03, stage04
from src.estimacao import stage05
from src.resultados import stage06

FUNCOES = {'00': stage00, '01': stage01, '02': stage02, '03': stage03,
           '04': stage04, '05': stage05, '06': stage06}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline PNADC x exposicao a IA')
    parser.add_argument('--inicio', default='00', choices=sorted(FUNCOES))
    parser.add_argument('--fim', default='06', choices=sorted(FUNCOES))
    args = parser.parse_args()
    for stage in sorted(FUNCOES):
        if args.inicio <= stage <= args.fim:
            print(f'== etapa {stage}: {ETAPAS[stage]}')
            run(stage, FUNCOES[stage])
