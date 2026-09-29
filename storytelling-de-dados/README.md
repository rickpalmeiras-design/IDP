# Storytelling de dados

Pasta da matéria. Guarda tudo o que foi produzido para a aula, separado do material da
dissertação. Nada aqui é texto da dissertação nem resultado novo do trabalho: são recortes
dos dados já estimados, preparados para contar a história em um painel.

## Pedido da aula

Construir um painel em HTML que conte a história do trabalho, começando pelo contraste
entre as ocupações mais e menos expostas à inteligência artificial. O painel foi desenhado
em outra conversa (`painel/classico_da_ia.html`) e aqui ele foi preenchido com os números reais do
projeto, pela montagem que está em `painel/fontes/`.

## Como a pasta está organizada

```
storytelling-de-dados/
├── painel/      o HTML final, pronto para abrir, e as fontes que o montam
├── dados/       o que o painel lê e os CSV de apoio
├── consultas/   os scripts que geram os dados
└── briefing/    os dois documentos de texto
```

### `painel/`

| Arquivo | Para que serve |
| --- | --- |
| `classico_da_ia.html` | **O painel, pronto e com os dados reais dentro.** Um arquivo só, de 16 MB, com o estádio e os atletas embutidos como imagem. Dê dois cliques e ele abre no navegador: a faixa do topo aparece verde, com "Dados do projeto: 2.452.987 transições nas médias". Não precisa de servidor, de internet nem de carregar arquivo. |
| `validacao-dados-oficiais.json` | O que a montagem conferiu antes de gravar o painel: o sha256 do `dashboard_data.json` que entrou, o número de linhas de cada tabela e a lista de verificações. |
| `fontes/` | De onde o painel sai. `classico_animado.html` é a página com a metáfora do jogo; `assets/` guarda o estádio e a prancha dos atletas em PNG, com os prompts que os geraram; `build-stadium.cjs` junta os dois e embute as imagens; `build-official.cjs` injeta o `dados/dashboard_data.json`, apaga o gerador de demonstração e grava o painel. Para refazer: `node storytelling-de-dados/painel/fontes/build-stadium.cjs` e depois `node .../build-official.cjs`. |

Na seção "Chama o VAR", o painel passa sozinho pelos três indicadores: a cada troca o
árbitro faz o sinal do VAR, o gráfico é redesenhado da esquerda para a direita e o veredito
entra em seguida. Clicar em um indicador encerra o rodízio e devolve o controle a quem lê; o
botão "Rodar sozinho" religa. Sob preferência de movimento reduzido nada disso roda: o
gráfico aparece pronto e o rodízio nem começa. O árbitro é um pictograma vetorial, desenhado
no próprio HTML, sem semelhança com nenhum árbitro real.

Os atletas são uma representação visual dos fluxos de trabalhadores. O uniforme e o rosto
de cada um não dizem nada sobre a exposição à IA da ocupação: são desenho, não medida. A
comparação descritiva do painel e a inspeção visual das séries não comprovam causalidade.

### `consultas/`

| Arquivo | Para que serve |
| --- | --- |
| `gera_dashboard_data.py` | Gera os dados do painel a partir do painel agregado do projeto e já os escreve dentro do HTML: `uv run python storytelling-de-dados/consultas/gera_dashboard_data.py`. |
| `gera_json.py` | Regera o `dados/dados_painel.json` a partir dos CSV de `dados/`. |
| `auditoria_e_fluxos.py` | Script da outra conversa que monta as tabelas do painel a partir de microdados individuais. **Não roda neste repositório** (veja abaixo). |
| `baixar_painel_pnadc.py` | Consulta ao BigQuery da outra conversa, que baixaria o painel individual. **Não deve ser rodada sem falar com o Danny** (veja abaixo). |

### `briefing/`

| Arquivo | Para que serve |
| --- | --- |
| `BRIEFING_DASH.md` | O documento da aula: resumo do trabalho, tabela de-para das dez ocupações, números autorizados, o que a história pode e não pode afirmar, roteiro de seis telas e, na seção 6, um prompt pronto para colar em outra conversa. |
| `BRIEFING_PIPELINE.md` | O briefing da outra conversa, com as decisões da reunião de 22/09 e o passo a passo original (BigQuery → auditoria → painel). Guardado como registro. |

### `dados/`

| Arquivo | Para que serve |
| --- | --- |
| `dashboard_data.json` | O que o painel lê. É o mesmo conteúdo embutido no HTML, e serve para recarregar pelo botão da faixa do topo. |
| `dados_painel.json` | Reúne em uma estrutura só os metadados, números-chave, as dez ocupações, a distribuição do AIOE, os agregados pré e pós, os coeficientes, os avisos e o roteiro das telas. |
| `dez_ocupacoes.csv` | As cinco ocupações de maior e as cinco de menor exposição, entre as que têm ao menos 100 mil trabalhadores. |
| `exposicao_por_ocupacao.csv` | As 416 ocupações com AIOE, teletrabalhabilidade e número médio de trabalhadores por trimestre. |
| `descritivas_desfechos.csv` | Médias ponderadas dos sete desfechos, no pré e no pós. |
| `coeficientes.csv` | Coeficientes estimados dos sete desfechos, com erro-padrão e intervalo. |

## Por que o pipeline do BigQuery não foi usado

O `consultas/auditoria_e_fluxos.py` espera `data/painel_final.parquet`, um painel com uma linha por
pessoa e por trimestre. Esse arquivo não existe aqui, e não existe de propósito: a Seção 3.2
da dissertação diz que o pareamento das pessoas é feito no ambiente remoto e que só os
resultados já agregados em células vêm para o computador. Rodar o `consultas/baixar_painel_pnadc.py`
traria microdados individuais para o disco local e deixaria essa frase falsa. Além disso,
ele precisa de um projeto do Google Cloud, que o `config.yaml` não tem preenchido.

A saída é a mesma sem quebrar nada: o `consultas/gera_dashboard_data.py` produz exatamente o mesmo
JSON a partir de `data/processed/pnadc_transicoes.parquet`, o painel agregado que já
reproduz a Tabela 4. Cada célula guarda trimestre, ocupação de origem e de destino, condição
no destino, o AIOE dos dois lados, o peso somado e o número de pares. Como tudo o que o
painel mostra são médias ponderadas, somar pesos por célula dá o mesmo número que somar por
pessoa.

## Os números que estão no painel

Janela de 2019T1 a 2025T3, pessoas de 18 a 65 anos, ocupadas na origem, reencontradas no
trimestre seguinte. 2.452.987 transições entram nas médias.

| O que | Verdão (Q4, mais expostos) | Mengão (Q1, menos expostos) |
| --- | --- | --- |
| Mudou de grande grupo de ocupação, pré | 24,5% | 19,5% |
| Mudou de grande grupo de ocupação, pós | 25,3% | 20,1% |
| Diferença | +0,9 p.p. | +0,6 p.p. |
| Ficou desempregado, pré → pós | 2,3% → 1,6% (−0,7 p.p.) | 4,8% → 3,2% (−1,6 p.p.) |
| Parou de trabalhar e de procurar, pré → pós | 3,8% → 3,8% (−0,0 p.p.) | 7,6% → 8,1% (+0,5 p.p.) |

O VAR do painel compara as duas linhas antes do lançamento: a distância média era de 5,0
pontos antes e passou a 5,3 pontos depois, com as inclinações do pré praticamente iguais.

## Uma decisão que muda o número do placar

Entre 2020T1 e 2021T3 o IBGE pesquisou majoritariamente por telefone, e a taxa medida de
mudança de ocupação cai quase pela metade (de cerca de 23% para cerca de 11% no Q4). Não é o
mercado que mudou, é a forma de perguntar. Se esses trimestres entram na média do "pré", o
painel mostra um salto de mais de 5 pontos depois do ChatGPT que é quase todo artefato de
medida. Por isso eles ficam **fora das médias de antes e depois**, mas **continuam no gráfico
do VAR**, marcados em cinza, para a quebra ficar visível na aula.

Para voltar atrás, basta trocar `FORA_DAS_MEDIAS_COLETA_REMOTA` para `False` no topo do
`consultas/gera_dashboard_data.py`. Vale lembrar que as taxas de `dados/dados_painel.json` e do
`briefing/BRIEFING_DASH.md` (23,6% para 31,8%, por exemplo) foram calculadas com a janela
inteira e, portanto, carregam esse mesmo efeito de medida.

## Três coisas que o painel não pode errar

1. **Não afirmar causalidade.** O estudo mede associação condicional, em um período que
   contém muitas outras mudanças.
2. **Não tratar exposição como hierarquia.** AIOE menor significa menos exposição à IA, e
   não emprego pior ou salário menor.
3. **Não mostrar a direção do movimento sem explicação.** Quem está no quartil do topo só
   tem para onde descer e quem está no de baixo só tem para onde subir, então parte da
   divisão "foi para ocupação mais ou menos exposta" é mecânica. O painel já traz esse aviso
   embaixo das barras de direção.

## Procedência dos dados

Os CSV e o `dados/dashboard_data.json` vieram de `data/interim/exposicao_cod.parquet`,
`data/processed/pnadc_transicoes.parquet` e `output/tabelas/`, do mesmo repositório. As taxas
são médias ponderadas pelo peso amostral da origem. O número de trabalhadores nos CSV é a
soma dos pesos dividida pelos 27 trimestres, ou seja, uma média por trimestre, e não um total
acumulado.
