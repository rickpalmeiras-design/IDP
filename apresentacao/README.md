# Apresentações da dissertação

Slides e roteiro de fala para uma apresentação de **15 minutos**, em **12 slides**, baseados nos
Capítulos 2 a 5 da dissertação. Tema em verde escuro (o verde do Palmeiras, o mesmo `006437` da
dissertação). São **dez opções numeradas de 01 a 10**, com variações acadêmicas de layout,
paleta e títulos em Cambria ou Times New Roman, com texto em Calibri. Todas mantêm os mesmos
12 slides, números, leituras nas notas e cronograma de 15 minutos.

| Número | Arquivo | Composição |
| ---: | --- | --- |
| 01 | `apresentacao_01.pptx` | Verde acadêmico, composição original. |
| 02 | `apresentacao_02.pptx` | Gráficos à esquerda, caixas retangulares. |
| 03 | `apresentacao_03.pptx` | Títulos clássicos centralizados. |
| 04 | `apresentacao_04.pptx` | Composição editorial, gráficos à esquerda. |
| 05 | `apresentacao_05.pptx` | Verde profundo, composição plana, títulos centralizados. |
| 06 | `apresentacao_06.pptx` | Verde institucional, gráficos à esquerda, títulos centralizados. |
| 07 | `apresentacao_07.pptx` | Títulos clássicos, composição plana. |
| 08 | `apresentacao_08.pptx` | Editorial, gráficos à esquerda, títulos clássicos centralizados. |
| 09 | `apresentacao_09.pptx` | Fundo verde suave, caixas retangulares, títulos centralizados. |
| 10 | `apresentacao_10.pptx` | Composição plana, evidências à esquerda, títulos clássicos. |

`apresentacao_dissertacao.pptx` permanece disponível como arquivo original sem numeração.
As opções variam a apresentação visual, preservando o argumento da dissertação.

## O que tem aqui

| Arquivo | Para que serve |
| --- | --- |
| `apresentacao_dissertacao.pptx` | **Os slides.** A leitura de cada slide está nas notas do orador. |
| `roteiro.md` | O mesmo texto falado, em um documento só, com o quadro de tempo e as referências. |
| `conteudo.js` | Fonte única do texto falado e do tempo de cada slide. |
| `gerar_apresentacao.js` | Gera o `.pptx`. |
| `gerar_todas.js` | Gera os dez `.pptx` numerados. |
| `variantes.js` | Define os layouts e temas das dez opções. |
| `gerar_roteiro.js` | Gera o `roteiro.md` a partir do `conteudo.js`. |
| `contar.js` | Confere se as leituras cabem nos 15 minutos. |
| `prepara_dados.py` | Lê as tabelas `.tex` da dissertação e o CSV do AIOE e grava `dados_slides.json`. |
| `dados_slides.json` | Os números que os slides usam, extraídos da dissertação. |
| `ferramentas/apply_theme.js` | Grava as cores do tema dentro do `.pptx`. |

## Como apresentar

Abra o `.pptx` no PowerPoint e use o **Modo Apresentador** (Apresentação de Slides, Modo de Exibição do
Apresentador): as notas de cada slide mostram o tempo previsto, o ponto de controle do relógio e a leitura.
Se preferir papel, imprima o `roteiro.md`.

## A história em três atos

Todas as opções contam a mesma história, e cada slide mostra no alto em que ato está.

| Ato | Slides | Carta | O que diz |
| --- | --- | --- | --- |
| **Contexto** | 2 e 3 | slide 2 | O ChatGPT chegou ao público em 30/11/2022; a pergunta; o que a literatura sabe e a lacuna. |
| **Tensão** | 4 a 8 | slide 8 | Os obstáculos para responder (dados, medida, desenho) e o achado de que a mobilidade subiu para todos: então, a IA explica alguma parte? |
| **Resolução** | 9 a 12 | slide 12 | O gradiente, o vínculo preservado, os limites e a resposta em três níveis. |

## Os 12 slides e o tempo

Cada título diz a conclusão do slide, e não só o assunto.

| # | Título | Ato | Tempo | Relógio |
| ---: | --- | --- | ---: | ---: |
| 1 | Abertura | | 0:30 | 0:30 |
| 2 | A IA chegou para todos no mesmo dia. O trabalho mudou? | Contexto | 1:40 | 2:10 |
| 3 | A literatura mede a exposição; o Brasil não mede o uso | Contexto | 1:15 | 3:25 |
| 4 | A PNAD Contínua segue a mesma pessoa por cinco trimestres | Tensão | 1:10 | 4:35 |
| 5 | A exposição à IA varia muito entre as ocupações | Tensão | 1:20 | 5:55 |
| 6 | Sete desfechos: vínculo, mobilidade e direção | Tensão | 1:00 | 6:55 |
| 7 | Sem grupo de controle, comparo intensidades de exposição | Tensão | 1:20 | 8:15 |
| 8 | A mobilidade subiu em todas as faixas de exposição | Tensão | 1:15 | 9:30 |
| 9 | Mais exposição, mais mudança para ocupações menos expostas | Resolução | 1:30 | 11:00 |
| 10 | Mais exposição veio com o vínculo no emprego preservado | Resolução | 1:20 | 12:20 |
| 11 | Os dados mostram associação, ainda não causalidade | Resolução | 1:20 | 13:40 |
| 12 | Mudou a direção, não o vínculo; a causa segue em aberto | Resolução | 1:20 | 15:00 |

As leituras foram escritas para serem faladas: frases curtas, poucos números lidos em voz alta e o jargão
explicado na primeira vez. A **125 palavras por minuto**, somam cerca de **13:19** de fala, e cada slide tem
de 3 a 11 segundos de folga para pausas e troca de slide. Isso é uma estimativa: o ritmo de cada pessoa varia,
e só um ensaio com cronômetro garante que a fala fique abaixo de 15 minutos.

Os trechos entre colchetes nas notas, como *[Aponte para o histograma.]*, são marcas de gesto: indicam para
onde apontar, para narrar o gráfico em vez de ler o slide, e não entram na contagem de tempo.

## Cores com intenção

| Cor | Significa | Onde aparece |
| --- | --- | --- |
| Verde claro | **antes** do ChatGPT | barras "pré" (slide 8) e faixa "antes" das linhas do tempo (slides 2 e 7) |
| Verde Palmeiras | **depois** do ChatGPT e o efeito principal | barras "pós", o β, os números de resultado |
| Verde profundo | as cartas da história e as sínteses | cartas de contexto, tensão e resolução; faixas de lacuna e síntese |
| Dourado | **o marco e os alertas** | a linha do ChatGPT (slides 2 e 7) e o "✕ causal" (slide 12) |
| Cinza-esverdeado | o que é secundário ou não se sustenta | fontes, teste de atrito, "o que não sustentam" |

## Critérios de avaliação

| Critério | Onde está |
| --- | --- |
| Clareza narrativa | Três atos marcados em todos os slides, com uma carta para cada ato (slides 2, 8 e 12): pergunta, desenvolvimento e conclusão. |
| Escolha dos gráficos | Barras agrupadas para comparar antes e depois (8); colunas para a variação por faixa (8); histograma para a distribuição do índice (5); gráfico de pontos com intervalo de confiança para sete coeficientes (9); barras para o tamanho de cada amostra (4). |
| Relevância | Slide 2 (notas) e faixa "Lacuna e relevância" (slide 3): mudar de trabalho afeta renda, informalidade e qualificação, e o Brasil, com tanta informalidade, pode reagir diferente dos países ricos. |
| Uso intencional de cores | Tabela acima, aplicada igual nas dez opções. |
| Qualidade dos títulos | Títulos de slide e de gráfico dizem a conclusão (tabela acima). |
| Apresentação oral | Notas em fala simples, com marcas de gesto para narrar os gráficos. |

## O que é de onde

- **Números:** todos vêm da dissertação. Os valores dos gráficos e dos cartões de resultado são lidos das
  tabelas (`dissertacao/tabelas/`) por `prepara_dados.py`. Alguns números que aparecem só em texto
  (os 416 e 413 códigos, o 1,08% do peso, a correlação de 0,702, o χ² de 3.040,1, os valores-p, a queda de
  30,0% para 15,3%) estão digitados em `gerar_apresentacao.js` e foram conferidos contra o texto dos
  Capítulos 3 e 4. Se a dissertação mudar, rode `prepara_dados.py` e revise esses.
- **Gráficos:** são nativos do PowerPoint, editáveis (clique no gráfico e use *Editar dados*), exceto o
  gráfico de pontos do slide 9, desenhado com formas. Não reaproveitam as figuras da dissertação, que estão no
  azul padrão do matplotlib.
- **Histograma do AIOE:** refeito a partir de `storytelling-de-dados/dados/exposicao_por_ocupacao.csv`, que
  reproduz os 416 códigos, a média de 0,0053 e o desvio-padrão de 0,9445 declarados na dissertação.
- **Resultados de robustez:** não há nenhum. O slide 12 trata a bateria de sensibilidade como agenda, do jeito
  que o Capítulo 5 a descreve.

## Como regenerar

```
uv run --with pandas --with numpy python apresentacao/prepara_dados.py
cd apresentacao
npm install
node contar.js                  # confere o tempo das leituras
node gerar_apresentacao.js      # gera o .pptx
node gerar_roteiro.js           # gera o roteiro.md
node gerar_todas.js             # gera apresentacao_01.pptx até apresentacao_10.pptx
```

Para regenerar apenas uma opção, use `node gerar_apresentacao.js --versao 2`, por exemplo.

Para mudar o tempo de um slide ou o texto falado, edite `conteudo.js` e rode `contar.js`: ele mostra a folga de
cada slide e avisa se o total deixou de somar 900 segundos.
