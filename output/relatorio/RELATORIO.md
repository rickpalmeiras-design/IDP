# Exposição ocupacional à IA e transições de trabalho na PNAD Contínua

Gerado pela etapa 06. Todos os números vêm de `output/modelos` e `output/tabelas`.

## Desenho

Painel de transições trimestrais da PNADC (2019 em diante), pessoas ocupadas de
18 a 65 anos. Diferenças-em-diferenças com tratamento
contínuo: o choque é 2022-11-30 e a intensidade é o AIOE da ocupação de origem.

Especificação comum aos 7 desfechos:

```
y ~ aioe_origem:pos + telework:pos + idade + idade_quadrado
    | cod_origem + sigla_uf^mes + sexo + raca + escolaridade
    + tempo_emprego_categoria + tamanho_empresa_categoria + setor
```

Pesos: soma de V1028 da entrevista de origem (transversal). Cluster: UPA.
AIOE é padronizado entre ocupações (desvio-padrão 0.945), então um ponto
equivale a aproximadamente um desvio-padrão de exposição.

## Qualidade do painel

- Taxa de pareamento por trimestre: 0.747 a 0.847
  (limite de referência 0.8; os trimestres abaixo são os de coleta atípica de 2020-2021).
- Peso sem AIOE atribuído: 1.08%.
- Correlação AIOE-teletrabalho entre ocupações: 0.702. Por isso o teletrabalho entra
  interagido com o pós em todos os modelos.

## Efeitos de AIOE x pós (pontos percentuais por desvio-padrão)

| Desfecho | Efeito | IC95 | p | N células |
| --- | --- | --- | --- | --- |
| transicao para ocupacao de menor AIOE | +2.187 | [+1.982; +2.393] | 4.43e-96 | 2.876.964 |
| mudanca de ocupacao (3 digitos) | +0.861 | [+0.594; +1.128] | 2.69e-10 | 2.880.049 |
| mudanca de ocupacao (2 digitos) | +0.278 | [+0.027; +0.529] | 0.0301 | 2.880.049 |
| saida do emprego | -0.250 | [-0.398; -0.103] | 0.000855 | 3.176.283 |
| pareamento entre entrevistas (teste de atrito) | -0.261 | [-0.536; +0.015] | 0.0641 | 3.960.584 |
| transicao formal para informal | -0.673 | [-0.858; -0.488] | 9.71e-13 | 1.676.862 |
| transicao para ocupacao de maior AIOE | -1.364 | [-1.566; -1.161] | 1.05e-39 | 2.876.964 |

## Matriz de mobilidade entre quintis de AIOE

Diferença pós menos pré na diagonal (permanência no mesmo quintil):
Q1 -3.6 p.p., Q2 -5.0 p.p., Q3 -6.4 p.p., Q4 -8.1 p.p., Q5 -5.8 p.p..

Teste de Wald de igualdade das matrizes pré e pós: qui-quadrado 3040.1,
20 graus de liberdade, p = 0.

## Como interpretar

1. Os coeficientes são gradientes por desvio-padrão de AIOE, por transição trimestral. Não são
   percentuais de trabalhadores afetados pela IA.
2. AIOE menor não significa emprego pior: é direção de exposição, não hierarquia salarial.
3. Parte da assimetria entre mobilidade ascendente e descendente é mecânica, porque quem parte de
   AIOE alto só pode descer. O contraste informativo é a diferença pós menos pré por quintil.
4. Não há adoção de IA observada. O tratamento é um índice ocupacional e o choque é único e nacional:
   qualquer fator que tenha atingido ocupações de alto AIOE de forma diferencial no mesmo período
   entra no coeficiente. A queda de permanência em todos os quintis mostra que parte do movimento é
   comum ao mercado de trabalho do período.
5. A seleção longitudinal não está resolvida. O peso é transversal da origem e não há correção de
   atrito; o modelo de `pareado` é um teste de atrito, não uma prova de ausência de seleção.

## Limites

Ponte COD-ISCO-SOC com repartição uniforme entre SOC, resolução de dois dígitos no grupo 6 e sem
atribuição a militares. AIOE e teletrabalho são medidas americanas aplicadas à estrutura ocupacional
brasileira. O horizonte de cada transição é de um trimestre: efeitos mais lentos não aparecem aqui.
