# Briefing para o dashboard de storytelling

Material de apoio para construir um painel em HTML **em outra conversa**. Reúne o resumo
do trabalho, a tabela de-para das ocupações escolhidas, os números autorizados e um prompt
pronto para colar. Não é texto da dissertação.

Os dados estão nos CSV desta pasta, todos em UTF-8:

| Arquivo | Conteúdo |
| --- | --- |
| `dez_ocupacoes.csv` | as 10 ocupações da história, com exposição, tamanho e taxas pré e pós |
| `exposicao_por_ocupacao.csv` | as 416 ocupações com AIOE, teletrabalhabilidade e tamanho |
| `descritivas_desfechos.csv` | médias ponderadas de cada desfecho, no pré e no pós |
| `coeficientes.csv` | os coeficientes estimados dos sete desfechos |

---

## 1. O trabalho em cinco frases

1. A pergunta é se as ocupações mais expostas à inteligência artificial passaram a
   apresentar mais movimento de trabalhadores depois do lançamento público do ChatGPT, em
   30 de novembro de 2022.
2. A exposição de cada ocupação vem do índice AIOE, construído nos Estados Unidos ligando
   aplicações de IA às habilidades exigidas por cada ocupação, e transportado para a
   classificação brasileira por uma ponte declarada.
3. Os dados são da PNAD Contínua, entre 2019T1 e 2025T3, acompanhando a mesma pessoa em
   dois trimestres seguidos: são **4.017.289 transições** observadas.
4. O método compara a mudança entre o período pré e o pós **entre ocupações com exposições
   diferentes**, controlando ocupação, estado, trimestre, teletrabalhabilidade e
   características do trabalhador.
5. O achado principal é de recomposição, não de destruição: mais movimento entre
   ocupações, e nenhum sinal de que os mais expostos estejam perdendo o emprego.

## 2. As dez ocupações da história

Critério: as cinco de maior e as cinco de menor AIOE **entre as 140 ocupações com pelo
menos 100 mil trabalhadores**. O corte por tamanho existe para a história usar profissões
reconhecíveis; sem ele apareceriam bailarinos, juízes e telhadores, que são minúsculos na
amostra.

### Mais expostas

| Código | Ocupação | AIOE | Trabalhadores (média por trimestre) |
| --- | --- | --- | --- |
| 1211 | Dirigentes financeiros | +1,45 | 122.564 |
| 2619 | Profissionais em direito não classificados anteriormente | +1,43 | 106.582 |
| 2411 | Contadores | +1,43 | 393.230 |
| 2413 | Analistas financeiros | +1,42 | 124.972 |
| 2634 | Psicólogos | +1,42 | 237.704 |

### Menos expostas

| Código | Ocupação | AIOE | Trabalhadores (média por trimestre) |
| --- | --- | --- | --- |
| 9211 | Trabalhadores elementares da agricultura | −1,60 | 1.079.640 |
| 9122 | Lavadores de veículos | −1,63 | 206.338 |
| 9412 | Ajudantes de cozinha | −1,63 | 524.768 |
| 7131 | Pintores e empapeladores | −1,66 | 522.537 |
| 9313 | Trabalhadores elementares da construção de edifícios | −1,73 | 1.305.249 |

**Contraste que já conta uma história.** As cinco mais expostas somam 985 mil
trabalhadores, 1,3% do emprego da base. As cinco menos expostas somam 3,6 milhões, 5,0%.
E 62% dos trabalhadores brasileiros estão em ocupações com AIOE abaixo de zero, ou seja,
abaixo da média entre ocupações. A exposição à IA, no Brasil, é fenômeno de uma minoria
do emprego.

### As mesmas dez, com as taxas observadas

Taxas ponderadas, em porcentagem. "Pré" vai até 2022T3, "pós" começa em 2022T4.

| Ocupação | Muda de ocupação pré | pós | Sai do emprego pré | pós |
| --- | --- | --- | --- | --- |
| Dirigentes financeiros | 52,1 | 62,0 | 2,2 | 1,8 |
| Profissionais em direito | 20,2 | 29,7 | 0,9 | 2,3 |
| Contadores | 19,5 | 28,7 | 2,4 | 2,4 |
| Analistas financeiros | 37,2 | 46,5 | 1,9 | 2,9 |
| Psicólogos | 8,6 | 10,5 | 3,2 | 3,4 |
| Trab. elementares da agricultura | 25,4 | 36,4 | 18,5 | 19,9 |
| Lavadores de veículos | 22,5 | 30,5 | 10,7 | 8,7 |
| Ajudantes de cozinha | 29,1 | 43,8 | 12,6 | 13,6 |
| Pintores e empapeladores | 17,1 | 22,3 | 11,6 | 10,1 |
| Trab. elementares da construção | 29,8 | 39,4 | 17,9 | 17,3 |

Duas leituras seguras aqui: **todo mundo passou a mudar mais de ocupação**, expostos e não
expostos; e a taxa de saída do emprego dos menos expostos é várias vezes maior que
a dos mais expostos, de três a dez vezes conforme o par comparado, antes e depois, o que não tem nada a ver com IA e sim com
precariedade do vínculo.

## 3. Números agregados autorizados

Médias ponderadas de toda a amostra, pré e pós:

| Indicador | Pré | Pós | Variação |
| --- | --- | --- | --- |
| Muda de ocupação (3 dígitos) | 23,6% | 31,8% | +8,2 p.p. |
| Muda de ocupação (2 dígitos) | 20,9% | 28,0% | +7,1 p.p. |
| Vai para ocupação menos exposta | 12,8% | 17,4% | +4,6 p.p. |
| Vai para ocupação mais exposta | 12,9% | 17,4% | +4,6 p.p. |
| Sai do emprego | 7,9% | 8,1% | +0,2 p.p. |
| De formal para informal | 5,2% | 8,8% | +3,6 p.p. |
| Foi reencontrado no painel | 78,3% | 81,2% | +2,9 p.p. |

Efeito estimado, por unidade de AIOE, já descontados ocupação, estado, trimestre,
teletrabalhabilidade e características do trabalhador:

| Desfecho | Efeito (p.p.) | p |
| --- | --- | --- |
| Transição para ocupação menos exposta | +2,19 | <0,001 |
| Muda de ocupação (3 dígitos) | +0,86 | <0,001 |
| Muda de ocupação (2 dígitos) | +0,28 | 0,030 |
| Saída do emprego | −0,25 | <0,001 |
| Transição de formal para informal | −0,67 | <0,001 |
| Transição para ocupação mais exposta | −1,36 | <0,001 |

Outros números úteis: 27 trimestres, 413 ocupações na estimação, correlação de 0,702 entre
exposição à IA e possibilidade de trabalho remoto.

## 4. O que a história pode e não pode dizer

**Pode:**
- O mercado de trabalho brasileiro ficou mais móvel depois de 2022, em todas as faixas de
  exposição.
- Entre ocupações, quanto maior a exposição, mais o movimento pendeu para o lado das
  ocupações menos expostas.
- Não há sinal de que os mais expostos estejam perdendo emprego ou caindo na informalidade
  mais que os outros. O sinal é o contrário.
- A exposição alta atinge uma fatia pequena do emprego brasileiro.

**Não pode:**
- Dizer que a IA **causou** o movimento. O estudo mede associação, no período em que
  aconteceram muitas outras coisas.
- Dizer que ocupação menos exposta é ocupação pior. Exposição não é hierarquia salarial.
- Tratar o aumento geral de mobilidade como efeito da IA: ele aparece igualmente em quem
  não tem exposição nenhuma.
- Usar a série de 2020 e 2021 sem aviso: nesse período a PNADC foi coletada por telefone e
  a taxa medida de mudança de ocupação despenca, provavelmente por mudança de medida.
- Afirmar que o trabalho tem testes de robustez. Esta versão apresenta um cenário único.

**Uma armadilha que precisa de cuidado no gráfico.** Dirigentes financeiros aparecem com
70% de "foi para ocupação menos exposta", e trabalhadores da construção com 0,08%. Isso é
quase todo mecânico: quem está no topo do índice só tem para onde descer, e quem está na
base só tem para onde subir. Se o painel mostrar essa taxa sem explicar, conta uma história
falsa. O correto é mostrar as duas direções juntas, ou comparar a **mudança** entre
períodos, não o nível.

## 5. Roteiro narrativo sugerido, em seis telas

1. **A pergunta.** A IA vai acabar com empregos? Foto do debate público, com o marco de
   30 de novembro de 2022.
2. **Como medir exposição.** O AIOE, e as dez ocupações do contraste. Aqui entra a tabela
   de-para, que é visualmente forte: financeiro e jurídico de um lado, construção e cozinha
   do outro.
3. **Quem é exposto no Brasil.** Distribuição do AIOE ponderada por trabalhador: 62% está
   abaixo de zero. A exposição alta é de poucos.
4. **O que aconteceu depois de 2022.** Mobilidade subiu para todo mundo, de 23,6% para
   31,8%. Momento de tensão: parece que a IA mexeu com tudo.
5. **A virada.** O aumento é geral, inclusive entre quem não tem exposição. O que sobra
   quando se compara ocupações com exposições diferentes é um gradiente pequeno, de cerca
   de 2 pontos percentuais, e no sentido da recomposição, não da destruição.
6. **O que ainda não sabemos.** Não é causal, a medida é de 2021, a coleta mudou na
   pandemia, e o efeito pode estar no salário, que este trabalho não observa.

---

## 6. Prompt para colar na outra conversa

Copie daqui para baixo.

---

Quero construir um dashboard em HTML de página única para uma aula de storytelling com
dados. Vou colar os dados abaixo. O painel deve contar uma história em seis telas, com
rolagem vertical, e ser autoexplicativo para quem nunca viu o estudo.

**Contexto do estudo.** Dissertação de mestrado que investiga se as ocupações mais
expostas à inteligência artificial passaram a apresentar mais movimento de trabalhadores
depois do lançamento público do ChatGPT, em 30 de novembro de 2022. Usa a PNAD Contínua
entre 2019 e 2025, acompanhando a mesma pessoa em dois trimestres seguidos, num total de
4.017.289 transições. A exposição vem do índice AIOE, que liga aplicações de IA às
habilidades exigidas por cada ocupação. O método compara a mudança entre o período pré e o
pós entre ocupações com exposições diferentes, controlando ocupação, estado, trimestre,
possibilidade de trabalho remoto e características do trabalhador.

**As dez ocupações do contraste** (AIOE e trabalhadores, média por trimestre):

Mais expostas: Dirigentes financeiros (+1,45; 122.564), Profissionais em direito (+1,43;
106.582), Contadores (+1,43; 393.230), Analistas financeiros (+1,42; 124.972), Psicólogos
(+1,42; 237.704).

Menos expostas: Trabalhadores elementares da agricultura (−1,60; 1.079.640), Lavadores de
veículos (−1,63; 206.338), Ajudantes de cozinha (−1,63; 524.768), Pintores e empapeladores
(−1,66; 522.537), Trabalhadores elementares da construção (−1,73; 1.305.249).

As cinco mais expostas somam 985 mil trabalhadores, 1,3% do emprego da base; as cinco
menos expostas somam 3,6 milhões, 5,0%. E 62% dos trabalhadores estão em ocupações com
AIOE abaixo de zero.

**Taxas por ocupação**, em porcentagem, pré e pós:

| Ocupação | Muda de ocupação pré | pós | Sai do emprego pré | pós |
| --- | --- | --- | --- | --- |
| Dirigentes financeiros | 52,1 | 62,0 | 2,2 | 1,8 |
| Profissionais em direito | 20,2 | 29,7 | 0,9 | 2,3 |
| Contadores | 19,5 | 28,7 | 2,4 | 2,4 |
| Analistas financeiros | 37,2 | 46,5 | 1,9 | 2,9 |
| Psicólogos | 8,6 | 10,5 | 3,2 | 3,4 |
| Trab. elementares da agricultura | 25,4 | 36,4 | 18,5 | 19,9 |
| Lavadores de veículos | 22,5 | 30,5 | 10,7 | 8,7 |
| Ajudantes de cozinha | 29,1 | 43,8 | 12,6 | 13,6 |
| Pintores e empapeladores | 17,1 | 22,3 | 11,6 | 10,1 |
| Trab. elementares da construção | 29,8 | 39,4 | 17,9 | 17,3 |

**Agregados de toda a amostra**, pré e pós: muda de ocupação 23,6% para 31,8%; vai para
ocupação menos exposta 12,8% para 17,4%; vai para ocupação mais exposta 12,9% para 17,4%;
sai do emprego 7,9% para 8,1%; de formal para informal 5,2% para 8,8%.

**Efeito estimado por unidade de exposição**, já descontados os controles: transição para
ocupação menos exposta +2,19 pontos percentuais; muda de ocupação +0,86; saída do emprego
−0,25; de formal para informal −0,67; transição para ocupação mais exposta −1,36.

**Estrutura narrativa desejada, seis telas:** 1) a pergunta e o marco temporal; 2) como se
mede exposição e as dez ocupações do contraste; 3) quem é exposto no Brasil, com os 62%
abaixo de zero; 4) a mobilidade subiu para todo mundo depois de 2022; 5) a virada, em que
o aumento é geral e o que sobra de gradiente é pequeno e no sentido da recomposição; 6) o
que ainda não sabemos.

**Regras que o painel precisa respeitar:**
- Nunca afirmar que a IA causou o movimento. O estudo mede associação condicional.
- Nunca sugerir que ocupação menos exposta é ocupação pior. Exposição não é hierarquia.
- Não apresentar o nível da taxa "foi para ocupação menos exposta" por ocupação sem
  explicar que ele é em boa parte mecânico: quem está no topo do índice só tem para onde
  descer. Prefira mostrar as duas direções juntas ou a variação entre períodos.
- Incluir uma tela ou caixa final de limitações: não é causal, a medida de exposição é de
  2021, a coleta da PNADC mudou na pandemia e afeta a série de 2020 e 2021, e o estudo não
  observa salários.
- Usar sempre "pontos percentuais" quando a diferença for entre porcentagens.

**Preferências visuais:** linguagem simples em português do Brasil, tipografia grande,
paleta sóbria com no máximo duas cores de destaque, gráficos simples (barras horizontais
para o contraste entre ocupações, setas ou inclinação para pré e pós), e um número grande
por tela. Nada de 3D, nada de gráfico de pizza. Responsivo para celular.

---

## 7. Se quiser refazer os números

Os CSV desta pasta vieram de `data/interim/exposicao_cod.parquet`,
`data/processed/pnadc_transicoes.parquet` e `output/tabelas/`. As taxas por ocupação são
médias ponderadas pelo peso amostral, calculadas sobre o domínio em que cada desfecho está
definido. O número de trabalhadores é a soma dos pesos dividida pelos 27 trimestres, isto
é, uma média por trimestre, e não um total acumulado.
