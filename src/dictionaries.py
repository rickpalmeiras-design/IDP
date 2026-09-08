"""Etapa 01: confirma o esquema da PNADC e traduz categorias pelo dicionário da fonte.

Nenhum código de categoria é digitado à mão: todos vêm do dicionário publicado da
Base dos Dados e são validados por expressão regular sobre o rótulo oficial.
"""
import json
import re
import unicodedata
from .config import CFG, INTERIM
from .common import client, query, json_write, parquet_write, required, note

TABELA = 'basedosdados.br_ibge_pnadc.microdados'
COLUNAS = ['ano', 'trimestre', 'sigla_uf', 'id_upa', 'v1008', 'v1014', 'v1016', 'v2003',
           'v2007', 'v2008', 'v20081', 'v20082', 'v2009', 'v2010', 'v1028', 'vd3004',
           'vd4001', 'vd4002', 'vd4009', 'v4010', 'v4013', 'v4018', 'v4019', 'v4040']


def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(value).lower()) if not unicodedata.combining(c)).strip()


def select_codes(frame, column, pattern):
    selected = frame[frame.nome_coluna.str.lower().eq(column.lower()) & frame.id_tabela.eq('microdados')]
    selected = selected[selected.valor.map(normalize).str.contains(pattern, regex=True)]
    found = sorted(set(selected.chave.astype(str)))
    if not found:
        raise ValueError(f'Dicionário não confirma {column}: {pattern}; verificar fonte oficial.')
    if not all(re.fullmatch(r'\d+', code) for code in found):
        raise ValueError(f'Código não numérico inesperado em {column}.')
    return found


def sql_codes(values):
    if not values or not all(re.fullmatch(r'\d+', str(v)) for v in values):
        raise ValueError('Códigos vazios ou inválidos.')
    return ','.join("'" + str(v) + "'" for v in values)


def load():
    return json.loads(required(INTERIM / 'dicionarios_verificados.json').read_text(encoding='utf-8'))


def stage01():
    cli = client()
    obj = cli.get_table(TABELA)
    columns = {field.name.lower(): field.field_type for field in obj.schema}
    missing = set(COLUNAS) - set(columns)
    if missing:
        raise ValueError(f'{TABELA}: colunas não confirmadas: {sorted(missing)}')
    dictionary = query('SELECT id_tabela, nome_coluna, chave, valor, cobertura_temporal '
                       'FROM `basedosdados.br_ibge_pnadc.dicionario`', 'dicionario_br_ibge_pnadc', metadata=True)
    parquet_write(dictionary, INTERIM / 'dicionario_br_ibge_pnadc.parquet')
    codebook = {
        'pnadc_ocupado': select_codes(dictionary, 'vd4002', r'^pessoas ocupadas$|^ocupad[oa]'),
        'pnadc_desocupado': select_codes(dictionary, 'vd4002', r'^pessoas desocupadas$'),
        'pnadc_inativo': select_codes(dictionary, 'vd4001', r'^pessoas fora da forca de trabalho$'),
        'pnadc_formal_empregado': select_codes(dictionary, 'vd4009', r'com carteira|militar|estatutario'),
        'pnadc_informal_empregado': select_codes(dictionary, 'vd4009', r'sem carteira|trabalhador familiar'),
        'pnadc_conta_empregador': select_codes(dictionary, 'vd4009', r'conta[- ]propria|empregador'),
        'pnadc_cnpj_sim': select_codes(dictionary, 'v4019', r'^sim$'),
        'pnadc_cnpj_nao': select_codes(dictionary, 'v4019', r'^nao$'),
    }
    verified = {'pnadc': {'tabela': TABELA, 'colunas': columns, 'modificado': obj.modified}, 'codigos': codebook}
    json_write(INTERIM / 'dicionarios_verificados.json', verified)
    note('01', 'Esquema da PNADC e categorias de condição de ocupação, posição na ocupação e CNPJ '
               'confirmados no dicionário da Base dos Dados. Conta-própria/empregador é classificado como '
               'formal apenas com CNPJ declarado; sem declaração fica nulo, nunca zero.')
    return {'colunas_confirmadas': len(COLUNAS), 'categorias': {k: len(v) for k, v in codebook.items()}}
