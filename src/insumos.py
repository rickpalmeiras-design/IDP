"""Etapa 02: exposição ocupacional à IA e crosswalk COD->SOC, construídos localmente.

Cadeia completa: AIOE (Felten, Raj e Seamans) e teletrabalho (Dingel e Neiman) vivem
na classificação SOC2010 dos EUA; a PNADC classifica ocupação em COD (adaptação
brasileira da ISCO-08). A ponte é COD -> ISCO-08 -> SOC2010, com resolução declarada.
"""
import pandas as pd
import requests
from .config import CFG, RAW, INTERIM, ROOT
from .common import json_write, parquet_write, required, unique, note

TELEWORK_URL = ('https://raw.githubusercontent.com/jdingel/DingelNeiman-workathome/master/'
                'onet_to_BLS_crosswalk/output/onet_teleworkable_blscodes.csv')


def aioe():
    """AIOE por SOC, direto do apêndice publicado pelos autores."""
    frame = pd.read_excel(required(ROOT / CFG['insumos']['aioe']), sheet_name='Appendix A')
    frame = frame.rename(columns={'SOC Code': 'soc_code', 'AIOE': 'aioe'})[['soc_code', 'aioe']]
    unique(frame, ['soc_code'], 'AIOE Felten')
    parquet_write(frame, INTERIM / 'aioe_soc.parquet')
    return frame


def telework():
    """Teletrabalhabilidade por SOC. Usa o arquivo local; só baixa se ele não existir."""
    path = ROOT / CFG['insumos']['telework']
    if not path.exists():
        response = requests.get(TELEWORK_URL, timeout=60)
        response.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)
        json_write(INTERIM / 'telework_proveniencia.json', {'fonte': TELEWORK_URL})
    frame = pd.read_csv(path, dtype={'OCC_CODE': str}).rename(
        columns={'OCC_CODE': 'soc_code', 'teleworkable': 'telework'})[['soc_code', 'telework']]
    unique(frame, ['soc_code'], 'Telework Dingel-Neiman')
    parquet_write(frame, INTERIM / 'telework_soc.parquet')
    return frame


def auditoria_cod():
    """Lista os códigos COD oficiais e verifica quais existem literalmente na ponte ISCO.

    Coincidência numérica não é equivalência semântica: o diagnóstico fica registrado,
    não é usado como se fosse validação.
    """
    structure = pd.read_excel(required(ROOT / CFG['insumos']['estrutura_cod']), header=2)
    detail = structure.iloc[:, [3, 4]].dropna(subset=[structure.columns[3]]).copy()
    detail.columns = ['cod', 'descricao_cod']
    detail['cod'] = pd.to_numeric(detail.cod, errors='raise').astype(int).astype(str).str.zfill(4)
    bridge = pd.read_csv(required(ROOT / CFG['insumos']['ponte_isco_soc']), dtype=str)
    detail['codigo_encontrado_na_ponte_isco'] = detail.cod.isin(bridge.isco2008)
    detail.to_csv(INTERIM / 'auditoria_cod_isco.csv', index=False)
    json_write(INTERIM / 'auditoria_cod_isco.json', {
        'codigos_cod': len(detail),
        'sem_codigo_identico_na_ponte': detail.loc[~detail.codigo_encontrado_na_ponte_isco, 'cod'].tolist(),
        'equivalencia_semantica_validada': False,
        'observacao': 'O IBGE documenta adaptações da ISCO-08; a coincidência de número não prova correspondência.'})
    return detail, bridge


def crosswalk_cod_soc(detail, bridge):
    """Ponte conservadora COD->SOC, com o nível de resolução explícito em cada elo."""
    rows = []
    for r in detail.itertuples():
        # Militares e o COD 5168 não recebem AIOE por mera semelhança numérica.
        if r.cod.startswith('0') or r.cod == '5168':
            continue
        # O IBGE reagrupa a agropecuária: o grupo 6 só é comparável em dois dígitos.
        digits = 2 if r.cod.startswith('6') else 4
        selected = bridge[bridge.isco2008.str[:digits].eq(r.cod[:digits])]
        # A ponte BLS reproduzida traz entradas agregadas de três dígitos (211, 315).
        selected = pd.concat([selected, bridge[bridge.isco2008.eq(r.cod[:3])]]).drop_duplicates(['isco2008', 'soc2010'])
        soc = selected.soc2010.drop_duplicates()
        for s in soc:
            rows.append({'cod': r.cod, 'soc_code': s, 'peso': 1 / len(soc),
                         'nivel_cod_isco': digits, 'metodo': 'reparticao_uniforme_entre_soc',
                         'fonte_cod': 'IBGE Estrutura_Ocupacao_COD.xls',
                         'fonte_soc': 'reproducao arquivada da ponte BLS ISCO08-SOC2010'})
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / CFG['insumos']['crosswalk_cod_soc'], index=False)
    json_write(INTERIM / 'crosswalk_cod_proveniencia.json', {
        'codigos_mapeados': int(out.cod.nunique()), 'elos': len(out),
        'sem_correspondencia': detail.loc[~detail.cod.isin(out.cod), 'cod'].tolist(),
        'limitacoes': [
            'Grupo 6 (agropecuaria) em dois digitos; demais grupos civis em quatro digitos.',
            'Militares e COD 5168 sem atribuicao de exposicao.',
            'Pesos uniformes entre SOC sao hipotese de construcao, nao probabilidades oficiais.',
            'Acesso direto ao XLS do BLS retorna HTTP 403; usa-se reproducao arquivada.']})
    return out


def weighted_mean(frame, group, value, weight):
    """Média ponderada que ignora elos sem valor em vez de tratá-los como zero."""
    valid = frame[value].notna() & frame[weight].gt(0)
    d = frame.loc[valid, [group, value, weight]].copy()
    d['numerador'] = d[value] * d[weight]
    g = d.groupby(group, observed=True)[['numerador', weight]].sum()
    return (g.numerador / g[weight]).rename(value)


def exposicao_por_cod():
    """AIOE e teletrabalho projetados para o código ocupacional da PNADC."""
    cross = pd.read_csv(required(ROOT / CFG['insumos']['crosswalk_cod_soc']), dtype={'cod': str, 'soc_code': str})
    if not {'cod', 'soc_code', 'peso'}.issubset(cross):
        raise ValueError('Crosswalk COD/SOC exige colunas cod, soc_code e peso.')
    scores = pd.read_parquet(required(INTERIM / 'aioe_soc.parquet')).merge(
        pd.read_parquet(required(INTERIM / 'telework_soc.parquet')), on='soc_code', how='outer', validate='one_to_one')
    joined = cross.merge(scores, on='soc_code', how='left', validate='many_to_one')
    result = pd.concat([weighted_mean(joined, 'cod', m, 'peso') for m in ['aioe', 'telework']], axis=1).reset_index()
    parquet_write(result, INTERIM / 'exposicao_cod.parquet')
    return result


def stage02():
    aioe_frame = aioe()
    tele = telework()
    detail, bridge = auditoria_cod()
    cross = crosswalk_cod_soc(detail, bridge)
    exposure = exposicao_por_cod()
    correlation = float(exposure[['aioe', 'telework']].corr().iloc[0, 1])
    json_write(INTERIM / 'auditoria_exposicao.json', {
        'soc_com_aioe': len(aioe_frame), 'soc_com_telework': len(tele),
        'cod_com_exposicao': int(exposure.aioe.notna().sum()),
        'correlacao_aioe_telework_entre_cod': correlation,
        'soc_por_cod_maximo': int(cross.groupby('cod').size().max())})
    note('02', 'AIOE e teletrabalho agregados ao COD por media ponderada dos elos, sem multiplicar '
               'ocupacoes. AIOE e padronizado entre ocupacoes: um ponto equivale a cerca de um desvio-padrao. '
               'AIOE alto/baixo e direcao de exposicao, nao hierarquia salarial. A correlacao alta com '
               'teletrabalho e o motivo de o teletrabalho entrar interagido com o pos em todos os modelos.')
    return {'cod_mapeados': int(cross.cod.nunique()), 'correlacao_aioe_telework': correlation}
