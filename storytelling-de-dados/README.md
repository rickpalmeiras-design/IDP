# Storytelling de dados

Pasta da matéria. Guarda tudo o que foi produzido para a aula, separado do material da
dissertação. Nada aqui é texto da dissertação nem resultado novo do trabalho: são recortes
dos dados já estimados, preparados para contar a história em um painel.

## Pedido da aula

Construir um painel em HTML que conte a história do trabalho, começando pelo contraste
entre as ocupações mais e menos expostas à inteligência artificial. O painel em si é
montado em outra conversa; esta pasta reúne os dados e o texto de apoio.

## O que tem aqui

| Arquivo | Para que serve |
| --- | --- |
| `dados_painel.json` | **O arquivo para carregar no painel.** Reúne tudo em uma estrutura só: metadados, números-chave, as dez ocupações com suas taxas, a distribuição do AIOE em faixas, os agregados pré e pós, os coeficientes, os avisos obrigatórios e o roteiro das seis telas. |
| `gera_json.py` | Regera o JSON a partir dos CSV desta pasta: `uv run python storytelling-de-dados/gera_json.py`. |
| `BRIEFING_DASH.md` | O documento principal. Resumo do trabalho, tabela de-para das dez ocupações, números autorizados, o que a história pode e não pode afirmar, roteiro de seis telas e, na seção 6, um prompt pronto para copiar e colar na conversa em que o painel será construído. |
| `dez_ocupacoes.csv` | As cinco ocupações de maior e as cinco de menor exposição, entre as que têm ao menos 100 mil trabalhadores, com AIOE, teletrabalhabilidade, tamanho e taxas de mudança de ocupação, deslocamento no gradiente e saída do emprego, no pré e no pós. |
| `exposicao_por_ocupacao.csv` | As 416 ocupações com AIOE, teletrabalhabilidade e número médio de trabalhadores por trimestre. Serve para gráficos de distribuição. |
| `descritivas_desfechos.csv` | Médias ponderadas dos sete desfechos, no pré e no pós. |
| `coeficientes.csv` | Coeficientes estimados dos sete desfechos, com erro-padrão e intervalo. |

## Como usar

1. Abra o `BRIEFING_DASH.md` e leia as seções 1 a 5 para ter a história na cabeça.
2. Copie o bloco da seção 6 e cole na conversa onde o painel será construído. Ele é
   autossuficiente: carrega contexto, números e regras, sem precisar anexar arquivo.
3. Para alimentar o painel, use o `dados_painel.json`. Os CSV continuam aqui como fonte
   bruta, todos em UTF-8 com cabeçalho em português.

## Estrutura do `dados_painel.json`

| Chave | Conteúdo |
| --- | --- |
| `meta` | título, fonte, janela, marco temporal, número de transições e as unidades usadas |
| `numeros_chave` | trabalhadores na base, share com AIOE abaixo de zero, totais dos dois grupos e o critério de seleção das dez ocupações |
| `ocupacoes_destaque` | as dez ocupações, cada uma com AIOE, tamanho e taxas pré e pós |
| `distribuicao_aioe` | sete faixas de exposição, com ocupações, trabalhadores e participação |
| `agregados` | os sete desfechos, com taxa pré, taxa pós e variação em pontos percentuais |
| `coeficientes` | efeito estimado, erro-padrão, intervalo de 95% e valor-p |
| `avisos` | as cinco ressalvas que o painel precisa mostrar |
| `telas` | o roteiro de seis telas, com título, mensagem, número de destaque e quais blocos de dados usar |

Taxas vêm em porcentagem (52.1 significa 52,1%) e efeitos em pontos percentuais. Um
detalhe de navegador: abrindo o HTML direto do disco, com `file://`, o `fetch` do JSON
costuma ser bloqueado. Ou sirva a pasta por um servidor local, ou cole o conteúdo do JSON
dentro do próprio HTML.

## Três coisas que o painel não pode errar

1. **Não afirmar causalidade.** O estudo mede associação condicional, em um período que
   contém muitas outras mudanças.
2. **Não tratar exposição como hierarquia.** AIOE menor significa menos exposição à IA, e
   não emprego pior ou salário menor.
3. **Não mostrar o nível da taxa de deslocamento no gradiente sem explicação.** Quem está
   no topo do índice só tem para onde descer, então dirigentes financeiros aparecem com
   70% e trabalhadores da construção com 0,08%. Boa parte disso é mecânico. O certo é
   mostrar as duas direções juntas ou a variação entre períodos.

## Procedência dos dados

Os CSV vieram de `data/interim/exposicao_cod.parquet`,
`data/processed/pnadc_transicoes.parquet` e `output/tabelas/`, do mesmo repositório. As
taxas por ocupação são médias ponderadas pelo peso amostral, calculadas no domínio em que
cada desfecho está definido. O número de trabalhadores é a soma dos pesos dividida pelos
27 trimestres, ou seja, uma média por trimestre, e não um total acumulado.
