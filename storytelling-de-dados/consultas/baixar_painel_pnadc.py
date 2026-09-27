"""
baixar_painel_pnadc.py
Monta o painel longitudinal oficial da PNAD Contínua (IBGE, via Base dos Dados no BigQuery),
junta a nota C-AIOE por ocupação e salva data/painel_final.parquet no formato que o
auditoria_e_fluxos.py já espera (sem mexer no CONFIG dele).

Pré-requisitos (uma vez só):
  pip install "google-cloud-bigquery[bqstorage,pandas]" pyarrow
  gcloud auth application-default login
Uso:
  python baixar_painel_pnadc.py

A query (SQL abaixo) também pode ser colada direto no console do BigQuery.
"""
from pathlib import Path
import pandas as pd

# ============================ CONFIG ============================
PROJETO_GCP = "SEU-PROJETO-GCP"            # projeto que paga a consulta (billing)
CROSSWALK   = Path("data/cod_aioe.csv")    # seu crosswalk: colunas cod (COD 4 dígitos) e aioe
SAIDA       = Path("data/painel_final.parquet")
# ================================================================

SQL = r"""
-- Painel longitudinal PNAD Contínua, 2021T1 em diante, pessoas com 14 anos ou mais.
-- Identificação do indivíduo (IBGE): domicílio (UPA + V1008 + V1014) + sexo + data de nascimento.
-- V2003 (ordem no domicílio) NÃO é usada: o IBGE avisa que ela não serve para análise longitudinal.
WITH base AS (
  SELECT
    ano                                   AS Ano,
    trimestre                             AS Trimestre,
    SAFE_CAST(id_uf   AS INT64)           AS id_uf,
    CONCAT(CAST(SAFE_CAST(id_upa AS INT64) AS STRING), '-',
           CAST(SAFE_CAST(V1008  AS INT64) AS STRING), '-',
           CAST(SAFE_CAST(V1014  AS INT64) AS STRING)) AS id_domicilio,
    SAFE_CAST(V1016   AS INT64)           AS V1016,    -- nº da entrevista (1 a 5)
    SAFE_CAST(V1028   AS FLOAT64)         AS V1028,    -- peso com calibração
    SAFE_CAST(V2007   AS INT64)           AS V2007,    -- sexo
    SAFE_CAST(V2008   AS INT64)           AS V2008,    -- dia de nascimento
    SAFE_CAST(V20081  AS INT64)           AS V20081,   -- mês de nascimento
    SAFE_CAST(V20082  AS INT64)           AS V20082,   -- ano de nascimento
    SAFE_CAST(V2009   AS INT64)           AS V2009,    -- idade
    SAFE_CAST(V4010   AS INT64)           AS V4010,    -- COD da ocupação
    SAFE_CAST(VD4001  AS INT64)           AS VD4001,   -- 1 força de trabalho / 2 fora
    SAFE_CAST(VD4002  AS INT64)           AS VD4002,   -- 1 ocupado / 2 desocupado
    SAFE_CAST(VD4009  AS INT64)           AS VD4009,   -- posição na ocupação (formal/informal)
    SAFE_CAST(VD4016  AS FLOAT64)         AS VD4016    -- rendimento habitual do trabalho principal
  FROM `basedosdados.br_ibge_pnadc.microdados`
  WHERE ano >= 2021                                    -- filtro direto na partição (barateia a consulta)
    AND SAFE_CAST(V2009 AS INT64) >= 14
),
com_id AS (
  SELECT
    * EXCEPT (id_domicilio),
    CONCAT(id_domicilio, '-', CAST(V2007 AS STRING), '-',
           FORMAT('%04d%02d%02d', V20082, V20081, V2008)) AS id_individuo
  FROM base
  WHERE V2008  BETWEEN 1 AND 31          -- descarta data de nascimento ignorada (99 / 9999)
    AND V20081 BETWEEN 1 AND 12
    AND V20082 BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE())
),
unicos AS (                               -- remove chaves ambíguas (ex.: gêmeos do mesmo sexo)
  SELECT * FROM com_id
  QUALIFY COUNT(*) OVER (PARTITION BY id_individuo, Ano, Trimestre) = 1
)
SELECT * FROM unicos
QUALIFY COUNT(*) OVER (PARTITION BY id_individuo) >= 2   -- só quem aparece em 2+ trimestres
"""


def main():
    from google.cloud import bigquery
    cliente = bigquery.Client(project=PROJETO_GCP)

    teste = cliente.query(SQL, job_config=bigquery.QueryJobConfig(dry_run=True, use_query_cache=False))
    print(f"A consulta vai ler {teste.total_bytes_processed / 1e9:.1f} GB (cota gratuita: 1.000 GB/mês).")

    print("Baixando o painel...")
    df = cliente.query(SQL).to_dataframe(create_bqstorage_client=True)
    print(f"{len(df):,} linhas, {df['id_individuo'].nunique():,} pessoas, "
          f"{df['Ano'].min()}T{df.loc[df['Ano'] == df['Ano'].min(), 'Trimestre'].min()} a "
          f"{df['Ano'].max()}T{df.loc[df['Ano'] == df['Ano'].max(), 'Trimestre'].max()}")

    if not CROSSWALK.exists():
        raise SystemExit(f"Não encontrei {CROSSWALK}. Exporte seu crosswalk COD→C-AIOE com as colunas cod e aioe.")
    cw = pd.read_csv(CROSSWALK)
    cw = cw.rename(columns=str.lower)[["cod", "aioe"]].drop_duplicates("cod")
    cw["cod"] = pd.to_numeric(cw["cod"], errors="coerce").astype("Int64")
    df["V4010"] = df["V4010"].astype("Int64")
    df = df.merge(cw, left_on="V4010", right_on="cod", how="left").drop(columns="cod")

    ocup = df["VD4002"] == 1
    print(f"Ocupados com nota C-AIOE: {100 * df.loc[ocup, 'aioe'].notna().mean():.1f}%")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SAIDA, index=False)
    print(f"Salvo em {SAIDA}. Próximo passo: python auditoria_e_fluxos.py")


if __name__ == "__main__":
    main()
