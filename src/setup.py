"""Etapa 00: registra ambiente e confirma acesso ao BigQuery."""
import importlib.metadata
import sys
from .config import CFG, INTERIM
from .common import query, json_write, note


def stage00():
    packages = {p: importlib.metadata.version(p) for p in
                ['pandas', 'pyarrow', 'duckdb', 'numpy', 'scipy', 'matplotlib', 'google-cloud-bigquery', 'pyfixest']}
    environment = {'python': sys.version, 'pacotes': packages, 'projeto': CFG['bigquery']['projeto'],
                   'escopo': 'PNAD Contínua apenas'}
    json_write(INTERIM / 'ambiente.json', environment)
    query('SELECT 1 AS conexao', 'teste_conexao', metadata=True)
    note('00', 'Ambiente registrado. Cobrança do BigQuery no projeto declarado em config.yaml. '
               'A etapa 05 estima com pyfixest em Python; R/legado/modelos.R fica como gabarito histórico.')
    return environment
