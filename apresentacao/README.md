# Apresentação da dissertação

Slides e roteiro de fala para uma apresentação de **15 minutos**, em **12 slides**, baseados nos
Capítulos 2 a 5 da dissertação. Tema em verde escuro (o verde do Palmeiras, o mesmo `006437` da
dissertação), títulos em Cambria e texto em Calibri.

## O que tem aqui

| Arquivo | Para que serve |
| --- | --- |
| `apresentacao_dissertacao.pptx` | **Os slides.** A leitura de cada slide está nas notas do orador. |
| `roteiro.md` | O mesmo texto falado, em um documento só, com o quadro de tempo e as referências. |
| `conteudo.js` | Fonte única do texto falado e do tempo de cada slide. |
| `gerar_apresentacao.js` | Gera o `.pptx`. |
| `gerar_roteiro.js` | Gera o `roteiro.md` a partir do `conteudo.js`. |
| `contar.js` | Confere se as leituras cabem nos 15 minutos. |
| `prepara_dados.py` | Lê as tabelas `.tex` da dissertação e o CSV do AIOE e grava `dados_slides.json`. |
| `dados_slides.json` | Os números que os slides usam, extraídos da dissertação. |
| `ferramentas/apply_theme.js` | Grava as cores do tema dentro do `.pptx`. |

## Como apresentar

Abra o `.pptx` no PowerPoint e use o **Modo Apresentador** (Apresentação de Slides, Modo de Exibição do
Apresentador): as notas de cada slide mostram o tempo previsto, o ponto de controle do relógio e a leitura.
Se preferir papel, imprima o `roteiro.md`.

## Os 12 slides e o tempo

| # | Slide | Tempo | Relógio |
| ---: | --- | ---: | ---: |
| 1 | Abertura | 0:30 | 0:30 |
| 2 | A pergunta de pesquisa | 1:15 | 1:45 |
| 3 | O que a literatura já mostra | 1:15 | 3:00 |
| 4 | Dados: a PNAD Contínua em painel | 1:15 | 4:15 |
| 5 | Como medir a exposição à IA | 1:15 | 5:30 |
| 6 | Sete desfechos de transição | 1:00 | 6:30 |
| 7 | Desenho: diferenças em diferenças contínuas | 1:30 | 8:00 |
| 8 | A mobilidade subiu em todas as faixas | 1:15 | 9:15 |
| 9 | Resultado principal: o gradiente de exposição | 1:45 | 11:00 |
| 10 | Vínculo no emprego e teste de atrito | 1:15 | 12:15 |
| 11 | O que o desenho permite e o que não permite | 1:15 | 13:30 |
| 12 | Conclusões e próximos passos | 1:30 | 15:00 |

As leituras foram calibradas para **125 palavras por minuto**. Somadas, ocupam cerca de 14:54 de fala, e cada
slide fica a até 3 segundos do tempo reservado a ele. Isso é uma estimativa: o ritmo de cada pessoa varia, e
só um ensaio com cronômetro garante os 15 minutos.

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
```

Para mudar o tempo de um slide ou o texto falado, edite `conteudo.js` e rode `contar.js`: ele mostra a folga de
cada slide e avisa se o total deixou de somar 900 segundos.
