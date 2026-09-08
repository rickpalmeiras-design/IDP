"""Testes de construção: garantem que as regras do desenho não se percam em refatorações."""
import json
import numpy as np
import pandas as pd
import pytest

from src.config import CFG, INTERIM, PROCESSED, MODELS
from src.estimacao import FORMULA
from src.insumos import weighted_mean
from src.dictionaries import sql_codes, normalize
from src.config import ROOT, DISS_TABLES
from src.dissertacao import inteiro, decimal, milhar, assinado, pvalor


def test_formula_tem_interacoes_e_efeitos_fixos():
    f = FORMULA.format(y='sai_do_emprego')
    assert 'aioe_origem:pos' in f and 'telework:pos' in f
    assert 'cod_origem' in f and 'sigla_uf^mes' in f


def test_sql_codes_rejeita_codigo_nao_numerico():
    assert sql_codes(['1', '2']) == "'1','2'"
    with pytest.raises(ValueError):
        sql_codes(['1', 'ocupado'])
    with pytest.raises(ValueError):
        sql_codes([])


def test_normalize_remove_acento():
    assert normalize('Conta-Própria') == 'conta-propria'


def test_weighted_mean_ignora_valor_ausente():
    d = pd.DataFrame({'cod': ['1', '1', '2'], 'aioe': [1.0, None, 4.0], 'peso': [0.5, 0.5, 1.0]})
    result = weighted_mean(d, 'cod', 'aioe', 'peso')
    assert result['1'] == 1.0 and result['2'] == 4.0


@pytest.mark.skipif(not (PROCESSED / 'pnadc_transicoes.parquet').exists(), reason='painel ainda nao construido')
def test_painel_respeita_amostra_e_choque():
    d = pd.read_parquet(PROCESSED / 'pnadc_transicoes.parquet',
                        columns=['idade', 'data', 'pos', 'pareado', 'sai_do_emprego', 'aioe_origem'])
    assert d.idade.between(CFG['idade_minima_pnadc'], CFG['idade_maxima_pnadc']).all()
    corte = pd.Timestamp(CFG['choque']).to_period('Q').start_time
    assert d.pos.eq(pd.to_datetime(d.data).ge(corte)).all()
    # Desfechos de destino só existem onde houve par.
    assert d.loc[~d.pareado.astype(bool), 'sai_do_emprego'].isna().all()


@pytest.mark.skipif(not (INTERIM / 'exposicao_cod.parquet').exists(), reason='insumos ainda nao preparados')
def test_exposicao_por_cod_e_unica_e_padronizada():
    e = pd.read_parquet(INTERIM / 'exposicao_cod.parquet')
    assert not e.cod.duplicated().any()
    assert 0.5 < e.aioe.std() < 2  # AIOE é padronizado: coeficiente por unidade ~ por desvio-padrão.


@pytest.mark.skipif(not (MODELS / '05_pnadc_sai_do_emprego.csv').exists(), reason='modelos ainda nao estimados')
def test_modelos_usam_cluster_upa_e_pesos():
    for path in MODELS.glob('05_pnadc_*_metadados.json'):
        meta = json.loads(path.read_text(encoding='utf-8'))
        assert meta['cluster'] == 'id_upa'
        assert meta['pesos'] == 'peso_total'


@pytest.mark.skipif(not (MODELS / '05_igualdade_matrizes.json').exists(), reason='matriz ainda nao calculada')
def test_matriz_de_transicao_soma_um_por_origem():
    m = pd.read_csv(MODELS.parent / 'tabelas' / '05_matriz_transicao.csv')
    soma = m.groupby(['pos', 'q_origem']).probabilidade.sum()
    assert np.allclose(soma, 1)


def test_numeros_saem_no_padrao_brasileiro():
    assert inteiro(3960585) == '3.960.585'
    assert decimal(2.1874, 3) == '2,187'
    assert milhar(3040.1034) == '3.040,1'
    assert assinado(-0.2605) == '$-$0,261'   # sinal em modo matemático, não hífen
    assert assinado(0.0152) == '$+$0,015'
    assert pvalor(0.0301) == '0,030'
    assert pvalor(2.6e-10) == '$<$0,001'


@pytest.mark.skipif(not (DISS_TABLES / 'tab_principal.tex').exists(), reason='tabelas ainda nao geradas')
def test_tabelas_da_dissertacao_sao_flutuantes_completos():
    for nome in ('tab_escala', 'tab_descritivas', 'tab_matriz', 'tab_principal'):
        texto = (DISS_TABLES / f'{nome}.tex').read_text(encoding='utf-8')
        assert texto.count('\\begin{table}') == 1 and texto.count('\\end{table}') == 1
        assert '\\caption{' in texto and '\\label{tab:' in texto
        assert '\\fonte{' in texto and '\\nota{' in texto
        # O gerador é a única fonte destes arquivos: o aviso tem de sobreviver.
        assert 'Não editar à mão' in texto


@pytest.mark.skipif(not (DISS_TABLES / 'tab_principal.tex').exists(), reason='tabelas ainda nao geradas')
def test_capitulo_usa_as_tabelas_geradas_e_nao_numeros_digitados():
    capitulo = (ROOT / 'dissertacao/capitulos/04-analise-e-discussao.tex').read_text(encoding='utf-8')
    for nome in ('tab_escala', 'tab_descritivas', 'tab_matriz', 'tab_principal'):
        assert f'\\input{{tabelas/{nome}}}' in capitulo
    assert '\\begin{tabular}' not in capitulo
