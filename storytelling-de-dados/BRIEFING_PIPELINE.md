# Briefing: painel PNADC → dashboard "Clássico da IA"

Repositório: `ricardo-pnadc` (pasta de trabalho: `storytelling-de-dados/`)
Responsável: Ricardo Carvalho | Orientador: Prof. Danny de Castro Soares (IDP)

> **Nota de arquivo.** Este é o briefing vindo da conversa em que o painel foi desenhado,
> guardado como registro das decisões da reunião de 22/09. O caminho descrito aqui
> (BigQuery → `painel_final.parquet` → `auditoria_e_fluxos.py`) **não foi executado**: ele
> traria microdados individuais para o disco local, o que a Seção 3.2 da dissertação diz que
> não é feito, e exige um projeto do Google Cloud que o `config.yaml` não tem. O painel foi
> preenchido com os mesmos números por outro caminho, o `gera_dashboard_data.py`, que parte
> do painel agregado do projeto. O que mudou em relação ao combinado está no `README.md`:
> a janela começa em 2019T1 (e não 2021T1) e os trimestres de coleta por telefone ficam fora
> das médias de pré e pós. O resto — pós a partir de 2023T1, 2022T4 fora, quartis fixados no
> pré, mudança medida no grande grupo, pares consecutivos com peso da origem — foi seguido.

## Objetivo

Gerar, a partir dos microdados oficiais da PNAD Contínua, o painel longitudinal com a nota C-AIOE,
auditar o painel, calcular os fluxos de trabalhadores e publicar o dashboard HTML com os números reais.
Atende aos três tópicos da reunião de 22/09:

1. Revisar os dados e como o painel final foi criado, antes do diff-in-diff.
2. Estatísticas descritivas dos fluxos: para qual área as pessoas estão migrando.
3. Dashboard de Storytelling de Dados em HTML.

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `storytelling-de-dados/baixar_painel_pnadc.py` | Query no BigQuery (Base dos Dados) + merge com C-AIOE. Gera `data/painel_final.parquet` |
| `storytelling-de-dados/auditoria_e_fluxos.py` | Auditoria do painel + tabelas de fluxo. Gera `out/` e `out/dashboard_data.json` |
| `storytelling-de-dados/classico_da_ia.html` | Dashboard. Lê os dados do bloco `<script id="dados-embutidos">` |
| `data/cod_aioe.csv` | Crosswalk COD → C-AIOE (colunas `cod`, `aioe`). Exportar do crosswalk já validado (427/434 códigos) |

## Passo a passo

### 1. Ambiente

```bash
pip install "google-cloud-bigquery[bqstorage,pandas]" pyarrow pandas numpy tabulate
gcloud auth application-default login
```

Preencher `PROJETO_GCP` no topo de `baixar_painel_pnadc.py`.

### 2. Crosswalk

Exportar o crosswalk COD → C-AIOE já usado na dissertação para `data/cod_aioe.csv`,
com exatamente duas colunas: `cod` (COD de 4 dígitos, inteiro) e `aioe` (nota padronizada).
Não recriar o crosswalk: usar o que reproduz a Tabela 4.

### 3. Baixar o painel

```bash
python baixar_painel_pnadc.py
```

Conferir no terminal:
- GB lidos na consulta (deve caber na cota gratuita de 1.000 GB/mês);
- período coberto começando em 2021T1;
- percentual de ocupados com nota C-AIOE (esperado acima de 95%).

Se o BigQuery reclamar de tipo em `ano >= 2021`, trocar por `SAFE_CAST(ano AS INT64) >= 2021`.

### 4. Auditoria e fluxos

```bash
python auditoria_e_fluxos.py
```

Ler `out/auditoria.md` e reportar todos os itens da seção de alertas. Pontos obrigatórios:
- duplicatas id × trimestre devem ser zero;
- sexo inconsistente dentro do mesmo id abaixo de 1%;
- idade inconsistente abaixo de 2%;
- lista dos CODs sem AIOE (top 10).

Se houver alerta, **parar e reportar** antes de seguir para o passo 5.

### 5. Publicar o dashboard com dados reais

Abrir `classico_da_ia.html` e colar o conteúdo inteiro de `out/dashboard_data.json` dentro de:

```html
<script id="dados-embutidos" type="application/json"></script>
```

Resultado: a faixa do topo passa de amarela ("Dados ilustrativos") para verde ("Dados reais carregados").
Não alterar nada além desse bloco.

## Decisões metodológicas (não mudar sem falar com o Ricardo)

- **Identificação do indivíduo:** domicílio (UPA + V1008 + V1014) + sexo (V2007) + data de nascimento
  (V2008, V20081, V20082). V2003 não entra: o IBGE avisa que ela não serve para análise longitudinal.
  Pessoas com data de nascimento ignorada e chaves duplicadas no mesmo trimestre são descartadas.
- **Janela:** a partir de 2021T1, para evitar a coleta por telefone de 2020.
- **Tratamento:** pós começa em 2023T1. O 2022T4 fica fora da comparação (ChatGPT lançado em 30/11/2022).
- **Quartis de exposição:** cortes calculados na distribuição ponderada do pré e aplicados ao pós.
- **Mudança de ocupação:** medida no grande grupo COD (1 dígito), para reduzir erro de codificação entre entrevistas.
- **Transições:** só pares de trimestres consecutivos do mesmo indivíduo, ocupado na origem, ponderados por V1028 da origem.
- **Células com menos de 30 observações** são sinalizadas e não devem ser interpretadas.

## Entregáveis esperados

1. `data/painel_final.parquet`
2. `out/auditoria.md` + CSVs das tabelas A, B, D, E e Sankey
3. `out/dashboard_data.json`
4. `classico_da_ia.html` com os dados embutidos
5. Resumo curto (5 a 10 linhas) com: nº de pessoas e transições, alertas da auditoria,
   placar Verdão (Q4) × Mengão (Q1) de "mudou de tipo de trabalho" no pós, e o veredito do VAR
   (as linhas andam lado a lado antes de 2022T4?).

## Fora do escopo

- Estimação do diff-in-diff e event study (próxima etapa, em `pyfixest`).
- Qualquer mudança no crosswalk ou no índice C-AIOE.
- Commit e push: deixar para o Ricardo revisar e subir pelo GitHub Desktop.
