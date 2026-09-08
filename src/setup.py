"""Etapa 00: registra ambiente e confirma acesso ao BigQuery."""
import importlib.metadata
import shutil
import sys
from .config import CFG, INTERIM
from .common import query, json_write, note


def stage00():
    packages = {p: importlib.metadata.version(p) for p in
                ['pandas', 'pyarrow', 'duckdb', 'numpy', 'scipy', 'matplotlib', 'google-cloud-bigquery']}
    environment = {'python': sys.version, 'pacotes': packages, 'projeto': CFG['bigquery']['projeto'],
                   'Rscript': CFG['estimacao']['rscript'], 'Rscript_no_path': shutil.which('Rscript'),
                   'escopo': 'PNAD Contínua apenas'}
    json_write(INTERIM / 'ambiente.json', environment)
    query('SELECT 1 AS conexao', 'teste_conexao', metadata=True)
    note('00', 'Ambiente registrado. Cobrança do BigQuery no projeto declarado em config.yaml. '
               'A etapa 05 exige fixest no R indicado em estimacao.rscript.')
    return environment
