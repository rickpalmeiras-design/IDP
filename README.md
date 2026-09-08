# Exposição ocupacional à IA e transições de trabalho na PNAD Contínua

Pacote autocontido do paper que usa **exclusivamente** a PNAD Contínua. Nada aqui depende
de CAGED, RAIS ou de qualquer artefato do projeto de origem: os insumos, o painel, as
estimações, as tabelas e as figuras são construídos dentro desta pasta.

## Pergunta

Depois do lançamento público do ChatGPT (novembro de 2022), trabalhadores em ocupações mais
expostas à inteligência artificial passaram a apresentar transições de trabalho diferentes —
mudança de ocupação, saída do emprego, informalização, movimento no gradiente de exposição?

## Desenho em uma tela

- **Unidade**: par pessoa-trimestre na PNADC, ligando a entrevista de origem à seguinte.
- **Tratamento**: AIOE (Felten, Raj e Seamans) da ocupação de origem — contínuo, padronizado
  entre ocupações, de modo que um ponto equivale a cerca de um desvio-padrão.
- **Choque**: `2022-11-01`, no trimestre correspondente (`config.yaml: choque`).
- **Estimador**: diferenças-em-diferenças com tratamento contínuo, LPM com efeitos fixos de
  ocupação de origem e UF × mês, ponderado por V1028, com cluster de UPA.
- **Coeficiente de interesse**: `aioe_origem:pos`.

```
y ~ aioe_origem:pos + telework:pos + idade + idade_quadrado
    | cod_origem + sigla_uf^mes + sexo + raca + escolaridade
    + tempo_emprego_categoria + tamanho_empresa_categoria + setor
```

Sete desfechos: `pareado` (teste de atrito), `muda_ocupacao_2`, `muda_ocupacao_3`,
`sai_do_emprego`, `formal_para_informal`, `mobilidade_descendente_aioe`,
`mobilidade_ascendente_aioe`. Mais a matriz de mobilidade entre quintis de AIOE, com
bootstrap de UPA e teste de Wald de igualdade entre pré e pós.

## Pipeline

O pipeline é linear e tem sete etapas. As checagens de robustez foram realizadas,
mas não integram esta versão nem são reportadas nela.

| Etapa | Script | O que faz |
| --- | --- | --- |
| 00 | `scripts/00_ambiente.py` | Registra versões e confirma o acesso ao BigQuery. |
| 01 | `scripts/01_dicionarios.py` | Confirma o esquema da PNADC e traduz categorias pelo dicionário oficial. |
| 02 | `scripts/02_insumos.py` | AIOE e teletrabalho por SOC, auditoria do COD, crosswalk COD→ISCO→SOC, exposição por COD. |
| 03 | `scripts/03_cobertura_pnadc.py` | Cobertura trimestral disponível na fonte. |
| 04 | `scripts/04_painel_pnadc.py` | Autojunção trimestral no BigQuery e painel de transições agregado por UPA. |
| 05 | `scripts/05_estimacao.py` | Os sete LPM (via `R/modelos.R`, fixest) e a matriz de transição. |
| 06 | `scripts/06_tabelas_figuras.py` | Tabelas de síntese, figuras e `output/relatorio/RELATORIO.md`. |
| 06 | `scripts/06_dissertacao.py` | Tabelas em LaTeX e figuras da dissertação, em `dissertacao/tabelas` e `dissertacao/figuras`. |

```bash
python scripts/executa_tudo.py              # tudo
python scripts/executa_tudo.py --inicio 05  # só reestimar e refazer os resultados
make estimacao resultados
python -m pytest -q
```

O pacote já vem com os dados intermediários e o painel construídos, então **as etapas 05 e 06
rodam sem BigQuery**. As etapas 01, 03 e 04 exigem credencial do projeto declarado em
`config.yaml`; a 04 reaproveita os parquets em `data/interim/pnadc_pares_*.parquet` sempre que o
SQL gerado for idêntico ao registrado em `logs/sql/`, e só reconsulta quando algo muda.

A etapa 05 precisa de R com `fixest`, `data.table` e `jsonlite`. Bibliotecas instaladas e ambientes
virtuais não são versionados. Em outra máquina, rode `Rscript R/instala_pacotes.R` para construir
a biblioteca local `.tools/R-library`, que `R/modelos.R` coloca à frente do caminho de bibliotecas.
Ajuste o caminho do executável do R em `config.yaml: estimacao.rscript`.

Para preparar o Python 3.12 com as versões registradas no pacote, use `uv sync --locked`.
Execute os scripts com `uv run python` ou ative o ambiente `.venv` criado localmente.
As credenciais não acompanham o repositório: para consultar o BigQuery, configure a autenticação
local e preencha seu projeto em `config.yaml: bigquery.projeto`. O painel e os resultados já
incluídos permitem examinar a pesquisa sem autenticação. Esta é uma versão de trabalho;
as limitações metodológicas estão em `METODOLOGIA.md` e no capítulo final da dissertação.

O comando `executa_tudo.py` termina no relatório. Para atualizar também as tabelas e figuras
da dissertação, execute separadamente `uv run python scripts/06_dissertacao.py`.

## Regras de dados que o código impõe

- **Microdados individuais nunca são baixados.** `src/common.query` recusa qualquer consulta sem
  agregação; o pareamento acontece no BigQuery e só descem células por UPA e covariáveis.
- **Nenhum código de categoria é digitado à mão**: condição de ocupação, posição na ocupação e CNPJ
  vêm do dicionário publicado, validados por rótulo (`src/dictionaries.py`).
- **Par exige identidade coerente**: mesmo domicílio, número de ordem, visita seguinte, sexo e data
  de nascimento iguais, idade avançando no máximo um ano. Chave duplicada no trimestre não pareia.
- **Ausente não vira zero**: conta-própria sem CNPJ declarado fica nulo; desfechos de destino só
  existem onde houve par; a média ponderada da exposição ignora elos sem valor.
- **Toda tabela sai em CSV, TXT e TeX**, e todo modelo grava fórmula, cluster, pesos, número de
  clusters, versão do fixest e hash SHA-256 dos dados que rodaram.

## Estrutura

```
config.yaml            parâmetros: janela, choque, amostra, limites, caminhos dos insumos
src/                   config, common, dictionaries, insumos, pnadc/pareamento, estimacao, resultados
scripts/               um script por etapa, mais executa_tudo.py
R/modelos.R            estimação fixest chamada pela etapa 05
R/instala_pacotes.R    refaz .tools/R-library se necessário
.tools/R-library/      fixest, data.table, jsonlite e dependências, para rodar sem instalar nada
data/raw/              AIOE, ponte ISCO-SOC, estrutura COD, teletrabalho, crosswalk COD-SOC
data/interim/          pares trimestrais, exposição por COD, auditorias, taxa de pareamento
data/processed/        pnadc_transicoes.parquet — o painel de estimação
output/modelos/        coeficientes, matrizes de covariância, metadados, teste de Wald
output/tabelas/        tabelas em CSV, TXT e TeX
output/figuras/        PDFs
output/relatorio/      RELATORIO.md
logs/                  log por etapa, SQL executado, notas de decisão
```

## Leitura dos resultados

`output/relatorio/RELATORIO.md` é gerado a partir dos modelos e traz os números com as ressalvas.
Três pontos que não devem se perder na citação:

1. Os coeficientes são **gradientes por desvio-padrão de AIOE, por transição trimestral** — não são
   percentuais de trabalhadores afetados pela IA.
2. **AIOE menor não é emprego pior.** É direção de exposição, não hierarquia salarial.
3. **Não há adoção de IA observada.** O tratamento é um índice ocupacional e o choque é único e
   nacional; a queda de permanência ocupacional em todos os quintis mostra que parte do movimento é
   comum ao mercado de trabalho do período. São associações condicionais, não efeito causal medido.

## Fontes

- PNAD Contínua trimestral, IBGE, via `basedosdados.br_ibge_pnadc.microdados`.
- AIOE: Felten, Raj e Seamans, *Occupational Heterogeneity in Exposure to Generative AI* — apêndice
  de dados em `data/raw/aioe/`.
- Teletrabalhabilidade: Dingel e Neiman, arquivo publicado pelos autores em `data/raw/telework/`.
- Estrutura ocupacional COD: IBGE, `data/raw/cod/Estrutura_Ocupacao_COD.xls`.
- Ponte ISCO-08 → SOC2010: reprodução arquivada da correspondência do BLS.

## Tabelas da dissertação

`scripts/06_dissertacao.py` gera as quatro tabelas de dados do texto direto das saídas
da etapa 05, cada uma como um flutuante ABNT completo em `dissertacao/tabelas/`, e copia
as figuras para `dissertacao/figuras/`. O Capítulo 4 as consome por `\input`, então
nenhum número de tabela é digitado à mão: reestimar e rodar `make dissertacao` atualiza
o texto. Os arquivos gerados trazem um aviso no topo e não devem ser editados.

| Arquivo | Rótulo | Fonte dos números |
| --- | --- | --- |
| `tab_escala.tex` | `tab:escala` | painel + metadados dos modelos |
| `tab_descritivas.tex` | `tab:descritivas` | `06_descritivas_desfechos.csv` |
| `tab_matriz.tex` | `tab:matriz` | `05_diferencas_matriz.csv`, `05_igualdade_matrizes.json` |
| `tab_principal.tex` | `tab:principal` | `06_coeficientes_principais.csv` |

Os quadros conceituais dos capítulos 2 e 3 (roteiro de leitura, etapas do procedimento,
definição dos desfechos) continuam no `.tex`: são texto, não resultado.
