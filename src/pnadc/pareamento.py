"""Etapas 03 e 04: cobertura da PNADC e construção do painel de transições trimestrais.

Regra de dados: microdados individuais não são baixados. O pareamento entre entrevistas
é feito por autojunção no BigQuery e só descem células agregadas por UPA e covariáveis.
"""
import pandas as pd
from ..config import CFG, INTERIM, PROCESSED, ROOT, LOGS
from ..common import query, json_write, parquet_write, required, note
from ..dictionaries import load, sql_codes


def stage03():
    """Cobertura trimestral disponível na fonte; nada de microdado desce aqui."""
    meta = load()
    table = meta['pnadc']['tabela']
    coverage = query(f"SELECT ano,trimestre,COUNT(*) AS pessoas FROM `{table}` "
                     f"WHERE ano >= {CFG['inicio_pnadc']} GROUP BY ano,trimestre ORDER BY ano,trimestre",
                     'pnadc_cobertura')
    parquet_write(coverage, INTERIM / 'pnadc_cobertura.parquet')
    json_write(INTERIM / 'pnadc_extracao.json', {
        'tabela': table, 'pareamento': 'SQL remoto na etapa 04',
        'peso': 'V1028 transversal da entrevista de origem; nao e peso longitudinal',
        'microdados_locais': False})
    note('03', 'Etapa 03 verifica cobertura e prepara a fonte; a etapa 04 faz a autojuncao trimestral no '
               'BigQuery e baixa transicoes agregadas por UPA/covariaveis. id_pessoa nao e usado como se '
               'fosse identificador longitudinal validado.')
    return {'trimestres': len(coverage)}


def pairing_sql(meta, year, quarter):
    """Par = mesma pessoa em trimestre e visita consecutivos, com identidade validada.

    O casamento exige domicílio, número de ordem, sexo e data de nascimento coerentes, e
    idade que avança no máximo um ano. Chaves duplicadas dentro do trimestre não pareiam.
    """
    c = meta['codigos']
    table = meta['pnadc']['tabela']
    t = year * 4 + quarter - 1
    occupied = sql_codes(c['pnadc_ocupado'])
    unemployed = sql_codes(c['pnadc_desocupado'])
    inactive = sql_codes(c['pnadc_inativo'])
    formal = sql_codes(c['pnadc_formal_empregado'])
    informal = sql_codes(c['pnadc_informal_empregado'])
    selfemployed = sql_codes(c['pnadc_conta_empregador'])
    cnpj_yes = sql_codes(c['pnadc_cnpj_sim'])
    cnpj_no = sql_codes(c['pnadc_cnpj_nao'])
    return f"""WITH base AS (
      SELECT ano*4+trimestre-1 AS t,ano,trimestre,sigla_uf,id_upa,v1008,v1014,v2003,v1016,
        v2007 AS sexo,v2008 AS dia,v20081 AS mes_nascimento,v20082 AS ano_nascimento,v2009 AS idade,
        v2010 AS raca,vd3004 AS escolaridade,v1028 AS peso,v4010 AS cod,v4013 AS setor,
        v4040 AS tempo_emprego_categoria,v4018 AS tamanho_empresa_categoria,
        CASE WHEN vd4002 IN ({occupied}) THEN 'ocupado' WHEN vd4002 IN ({unemployed}) THEN 'desocupado'
          WHEN vd4001 IN ({inactive}) THEN 'inativo' END AS condicao_ocupacao,
        CASE WHEN vd4002 IN ({occupied}) THEN TRUE WHEN vd4002 IN ({unemployed}) OR vd4001 IN ({inactive}) THEN FALSE END AS ocupado,
        CASE WHEN vd4009 IN ({formal}) THEN 1
          WHEN vd4009 IN ({informal}) THEN 0
          WHEN vd4009 IN ({selfemployed}) AND v4019 IN ({cnpj_yes}) THEN 1
          WHEN vd4009 IN ({selfemployed}) AND v4019 IN ({cnpj_no}) THEN 0 ELSE NULL END AS formal,
        COUNT(*) OVER(PARTITION BY ano,trimestre,id_upa,v1008,v1014,v2003) AS duplicados
      FROM `{table}` WHERE ano BETWEEN {year} AND {year+1} AND ano*4+trimestre-1 BETWEEN {t} AND {t+1}
    ), pares AS (
      SELECT a.*, b.t IS NOT NULL AS pareado, b.cod AS cod_destino,b.ocupado AS ocupado_destino,
        b.formal AS formal_destino,b.condicao_ocupacao AS condicao_destino,
        IF(b.t IS NULL OR NOT b.ocupado,NULL,SUBSTR(a.cod,1,2)!=SUBSTR(b.cod,1,2)) AS muda_ocupacao_2,
        IF(b.t IS NULL OR NOT b.ocupado,NULL,SUBSTR(a.cod,1,3)!=SUBSTR(b.cod,1,3)) AS muda_ocupacao_3
      FROM base a LEFT JOIN base b ON b.t=a.t+1 AND b.id_upa=a.id_upa
        AND b.v1008=a.v1008 AND b.v1014=a.v1014 AND b.v2003=a.v2003
        AND b.v1016=a.v1016+1 AND a.duplicados=1 AND b.duplicados=1
        AND a.sexo=b.sexo AND a.dia=b.dia AND a.mes_nascimento=b.mes_nascimento
        AND a.dia BETWEEN 1 AND 31 AND a.mes_nascimento BETWEEN 1 AND 12
        AND a.ano_nascimento BETWEEN 1900 AND {year}
        AND b.ano_nascimento BETWEEN 1900 AND {year+1}
        AND ABS(a.ano_nascimento-b.ano_nascimento)<=1 AND b.idade BETWEEN a.idade AND a.idade+1
      WHERE a.t={t} AND a.v1016<5 AND a.ocupado
        AND a.idade BETWEEN {CFG['idade_minima_pnadc']} AND {CFG['idade_maxima_pnadc']}
    ) SELECT ano,trimestre,sigla_uf,id_upa,cod AS cod_origem,cod_destino,
      idade,sexo,raca,escolaridade,setor,tempo_emprego_categoria,tamanho_empresa_categoria,formal AS formal_origem,formal_destino,
      ocupado_destino,condicao_destino,pareado,muda_ocupacao_2,muda_ocupacao_3,
      COUNT(*) AS n, SUM(peso) AS peso_total, SUM(peso*peso) AS peso_quadrado_total,
      COUNTIF(duplicados>1) AS n_chave_duplicada,
      COUNTIF(peso IS NULL OR peso<=0) AS n_peso_invalido
    FROM pares GROUP BY ano,trimestre,sigla_uf,id_upa,cod_origem,cod_destino,idade,sexo,raca,
      escolaridade,setor,tempo_emprego_categoria,tamanho_empresa_categoria,formal_origem,formal_destino,ocupado_destino,condicao_destino,pareado,muda_ocupacao_2,muda_ocupacao_3"""


def stage04():
    coverage = pd.read_parquet(required(INTERIM / 'pnadc_cobertura.parquet'))
    meta = load()
    quarters = {(int(r.ano), int(r.trimestre)) for r in coverage.itertuples()}
    frames = []
    for year, quarter in sorted(quarters):
        following = (year + 1, 1) if quarter == 4 else (year, quarter + 1)
        if following not in quarters:
            continue  # A última entrevista disponível não entra no denominador de attrition.
        cached = INTERIM / f'pnadc_pares_{year}T{quarter}.parquet'
        sql = pairing_sql(meta, year, quarter)
        previous_sql = LOGS / 'sql' / f'pnadc_pares_{year}T{quarter}.sql'
        # Só reconsulta o BigQuery se o SQL mudou: o cache local torna a etapa reproduzível sem custo.
        reusable = cached.exists() and previous_sql.exists() and previous_sql.read_text(encoding='utf-8').strip() == sql.strip()
        if not reusable and cached.exists() and not previous_sql.exists():
            (LOGS / 'sql').mkdir(parents=True, exist_ok=True)
            (LOGS / 'sql' / f'pnadc_pares_{year}T{quarter}.sql').write_text(sql, encoding='utf-8')
            reusable = True
        frame = pd.read_parquet(cached) if reusable else query(sql, f'pnadc_pares_{year}T{quarter}')
        parquet_write(frame, INTERIM / f'pnadc_pares_{year}T{quarter}.parquet')
        frames.append(frame)
    if not frames:
        raise ValueError('Sem trimestres consecutivos para pareamento.')
    result = pd.concat(frames, ignore_index=True)
    if result.n_peso_invalido.sum():
        raise ValueError('PNADC possui pesos invalidos; revisar versao do dicionario e da fonte.')
    result['data'] = pd.to_datetime(dict(year=result.ano, month=(result.trimestre - 1) * 3 + 1, day=1))
    result['idade_quadrado'] = result.idade ** 2
    result['pos'] = result.data.ge(pd.Timestamp(CFG['choque']).to_period('Q').start_time)
    result['trimestre_transicao_choque'] = result.data.eq(pd.Timestamp(CFG['choque']).to_period('Q').start_time)
    result['coleta_atipica'] = result.data.between('2020-04-01', '2021-04-01')
    result['sai_do_emprego'] = (~result.ocupado_destino.astype('boolean')).where(result.pareado)
    observed_destination = result.ocupado_destino.notna() & (result.ocupado_destino.eq(False) | result.formal_destino.notna())
    result['formal_para_informal'] = (result.ocupado_destino.eq(True) & result.formal_destino.eq(0)).astype('boolean').where(
        result.pareado & result.formal_origem.eq(1) & observed_destination)
    result['n_pareado'] = result.n.where(result.pareado, 0)
    audit = result.groupby(['ano', 'trimestre'], as_index=False)[['n', 'n_pareado', 'peso_total', 'n_chave_duplicada']].sum()
    audit['taxa_pareamento'] = audit.n_pareado / audit.n
    parquet_write(audit, INTERIM / 'pnadc_taxa_pareamento.parquet')
    parquet_write(result, INTERIM / 'pnadc_transicoes_sem_exposicao.parquet')
    attrs = result.groupby(['ano', 'trimestre', 'sexo', 'escolaridade'], dropna=False, as_index=False)[['n', 'n_pareado']].sum()
    attrs['taxa_pareamento'] = attrs.n_pareado / attrs.n
    parquet_write(attrs, INTERIM / 'pnadc_attrition_descritiva.parquet')
    if (audit.taxa_pareamento < CFG['limite_pareamento']).any() and not CFG.get('autorizacao_alertas_preparacao', False):
        raise ValueError('Pareamento PNADC abaixo do limite configurado; revisar antes de liberar o painel.')
    exposure = pd.read_parquet(required(INTERIM / 'exposicao_cod.parquet'))
    mapped = exposure.set_index('cod').aioe.to_dict()
    result['aioe_origem'] = result.cod_origem.map(mapped)
    result['aioe_destino'] = result.cod_destino.map(mapped)
    result['telework'] = result.cod_origem.map(exposure.set_index('cod').telework.to_dict())
    both = result[['aioe_origem', 'aioe_destino']].notna().all(axis=1) & result.pareado
    result['mobilidade_descendente_aioe'] = (result.aioe_destino < result.aioe_origem).where(both)
    result['mobilidade_ascendente_aioe'] = (result.aioe_destino > result.aioe_origem).where(both)
    miss = result.loc[result.aioe_origem.isna(), 'peso_total'].sum() / result.peso_total.sum()
    json_write(INTERIM / 'pnadc_cobertura_exposicao.json', {'sem_match_ponderado': float(miss)})
    if miss > CFG['limite_sem_match']:
        raise ValueError('Exposicao PNADC sem match supera o limite configurado.')
    parquet_write(result, PROCESSED / 'pnadc_transicoes.parquet')
    note('04', 'Pares exigem trimestre e visita consecutivos, sexo/data de nascimento e idade coerentes; '
               'chaves duplicadas nao sao pareadas. Quinta visita e ultima onda ficam fora do denominador. '
               'V1028 da origem e peso transversal, sem correcao automatica para selecao longitudinal. '
               'AIOE menor e direcao de exposicao, nao prova de perda salarial.')
    return {'celulas': len(result), 'menor_taxa_pareamento': float(audit.taxa_pareamento.min()),
            'sem_match_ponderado': float(miss)}
