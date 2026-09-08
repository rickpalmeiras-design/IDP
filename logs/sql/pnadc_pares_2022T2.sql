WITH base AS (
      SELECT ano*4+trimestre-1 AS t,ano,trimestre,sigla_uf,id_upa,v1008,v1014,v2003,v1016,
        v2007 AS sexo,v2008 AS dia,v20081 AS mes_nascimento,v20082 AS ano_nascimento,v2009 AS idade,
        v2010 AS raca,vd3004 AS escolaridade,v1028 AS peso,v4010 AS cod,v4013 AS setor,
        v4040 AS tempo_emprego_categoria,v4018 AS tamanho_empresa_categoria,
        CASE WHEN vd4002 IN ('1') THEN 'ocupado' WHEN vd4002 IN ('2') THEN 'desocupado'
          WHEN vd4001 IN ('2') THEN 'inativo' END AS condicao_ocupacao,
        CASE WHEN vd4002 IN ('1') THEN TRUE WHEN vd4002 IN ('2') OR vd4001 IN ('2') THEN FALSE END AS ocupado,
        CASE WHEN vd4009 IN ('1','3','5','7') THEN 1
          WHEN vd4009 IN ('10','2','4','6') THEN 0
          WHEN vd4009 IN ('8','9') AND v4019 IN ('1') THEN 1
          WHEN vd4009 IN ('8','9') AND v4019 IN ('2') THEN 0 ELSE NULL END AS formal,
        COUNT(*) OVER(PARTITION BY ano,trimestre,id_upa,v1008,v1014,v2003) AS duplicados
      FROM `basedosdados.br_ibge_pnadc.microdados` WHERE ano BETWEEN 2022 AND 2023 AND ano*4+trimestre-1 BETWEEN 8089 AND 8090
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
        AND a.ano_nascimento BETWEEN 1900 AND 2022
        AND b.ano_nascimento BETWEEN 1900 AND 2023
        AND ABS(a.ano_nascimento-b.ano_nascimento)<=1 AND b.idade BETWEEN a.idade AND a.idade+1
      WHERE a.t=8089 AND a.v1016<5 AND a.ocupado
        AND a.idade BETWEEN 18 AND 65
    ) SELECT ano,trimestre,sigla_uf,id_upa,cod AS cod_origem,cod_destino,
      idade,sexo,raca,escolaridade,setor,tempo_emprego_categoria,tamanho_empresa_categoria,formal AS formal_origem,formal_destino,
      ocupado_destino,condicao_destino,pareado,muda_ocupacao_2,muda_ocupacao_3,
      COUNT(*) AS n, SUM(peso) AS peso_total, SUM(peso*peso) AS peso_quadrado_total,
      COUNTIF(duplicados>1) AS n_chave_duplicada,
      COUNTIF(peso IS NULL OR peso<=0) AS n_peso_invalido
    FROM pares GROUP BY ano,trimestre,sigla_uf,id_upa,cod_origem,cod_destino,idade,sexo,raca,
      escolaridade,setor,tempo_emprego_categoria,tamanho_empresa_categoria,formal_origem,formal_destino,ocupado_destino,condicao_destino,pareado,muda_ocupacao_2,muda_ocupacao_3