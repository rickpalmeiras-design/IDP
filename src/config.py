"""Caminhos e parâmetros. Tudo é relativo à raiz do pacote ricardo-pnadc."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / 'config.yaml').read_text(encoding='utf-8'))
RAW = ROOT / 'data/raw'
INTERIM = ROOT / 'data/interim'
PROCESSED = ROOT / 'data/processed'
LOGS = ROOT / 'logs'
OUT = ROOT / 'output'
TABLES = OUT / 'tabelas'
MODELS = OUT / 'modelos'
FIGURES = OUT / 'figuras'
REPORT = OUT / 'relatorio'
WORK = INTERIM / 'estimacao'
ROBUSTEZ = OUT / 'robustez'
DISS = ROOT / 'dissertacao'
DISS_TABLES = DISS / 'tabelas'
DISS_FIGURES = DISS / 'figuras'
for directory in (INTERIM, PROCESSED, LOGS, TABLES, MODELS, FIGURES, REPORT, WORK, ROBUSTEZ,
                  DISS_TABLES, DISS_FIGURES):
    directory.mkdir(parents=True, exist_ok=True)

ETAPAS = {'00': 'ambiente', '01': 'dicionarios', '02': 'insumos', '03': 'cobertura_pnadc',
          '04': 'painel_pareado', '05': 'estimacao', '06': 'tabelas_figuras', '07': 'robustez'}
