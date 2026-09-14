# Metodologia

## Escopo desta versão

O desenho é o pipeline 00–06: um cenário único de estimação, com corte no trimestre
do choque, cluster de UPA e sete desfechos. 

## Passo a passo: cada etapa e o script que a executa

| Etapa | Entrada (script) | Módulo | Motor | Produz |
| --- | --- | --- | --- | --- |
| 00 | `scripts/00_ambiente.py` | `src/setup.py: stage00` | Python | versões e checagem de acesso ao BigQuery |
| 01 | `scripts/01_dicionarios.py` | `src/dictionaries.py: stage01` | BigQuery | dicionário oficial da PNADC validado por rótulo |
| 02 | `scripts/02_insumos.py` | `src/insumos.py: stage02` | Python | AIOE e teletrabalho por SOC, ponte COD→ISCO→SOC, exposição por COD |
| 03 | `scripts/03_cobertura_pnadc.py` | `src/pnadc/pareamento.py: stage03` | BigQuery | cobertura trimestral da fonte |
| 04 | `scripts/04_painel_pnadc.py` | `src/pnadc/pareamento.py: stage04` | BigQuery | autojunção e painel de células `pnadc_transicoes.parquet` |
| 05 | `scripts/05_estimacao.py` | `src/estimacao.py: stage05` | Python (pyfixest) | sete LPM e matriz de mobilidade com bootstrap de UPA |
| 06 | `scripts/06_tabelas_figuras.py` | `src/resultados.py: stage06` | Python | tabelas, figuras e `output/relatorio/RELATORIO.md` |
| 06 | `scripts/06_dissertacao.py` | `src/dissertacao.py: gera` | Python | tabelas LaTeX e figuras da dissertação, consumidas por `\input` no Capítulo 4 |

`scripts/executa_tudo.py --inicio 00 --fim 06` roda tudo em ordem; `make estimacao resultados`
refaz apenas 05 e 06 a partir do painel já construído.

Documento de referência do desenho. O que está aqui é o que o código faz; se divergirem, o código
manda e este arquivo é que está errado.

## 1. Fonte e unidade de observação

PNAD Contínua trimestral (IBGE), acessada em `basedosdados.br_ibge_pnadc.microdados`, de
`config.yaml: inicio_pnadc` em diante. A unidade é o **par pessoa-trimestre**: a entrevista de
origem `t` ligada à entrevista `t+1` da mesma pessoa.

Microdados individuais não são baixados. A autojunção acontece no BigQuery e o que desce são
**células agregadas** por trimestre, UF, UPA, ocupação de origem e destino, e as covariáveis do
modelo, com `COUNT(*)`, `SUM(peso)` e `SUM(peso²)`. Como todas as regressoras e todos os desfechos
são constantes dentro de cada célula, a estimação em células reproduz exatamente a estimação
individual — coeficientes e scores de cluster inclusive.

## 2. Construção do par

Duas entrevistas são a mesma pessoa quando coincidem:

- UPA, domicílio (`v1008`, `v1014`) e número de ordem na família (`v2003`);
- visita imediatamente seguinte (`v1016 → v1016 + 1`) e trimestre imediatamente seguinte;
- sexo, dia e mês de nascimento;
- ano de nascimento com diferença de no máximo 1, e idade que avança 0 ou 1 ano.

Restrições adicionais:

- chave duplicada dentro do trimestre (`duplicados > 1`) **não** pareia, dos dois lados;
- a quinta visita não entra como origem (não há visita seguinte);
- o último trimestre disponível não entra no denominador de atrito;
- a origem é **pessoa ocupada**, de `idade_minima_pnadc` a `idade_maxima_pnadc` anos.

A taxa de pareamento por trimestre fica registrada em `data/interim/pnadc_taxa_pareamento.parquet`
e na figura `fig_taxa_pareamento.pdf`. Os trimestres abaixo do limite de referência são os de
coleta atípica de 2020–2021, e a continuação está autorizada explicitamente em
`config.yaml: autorizacao_alertas_preparacao`.

## 3. Definição dos desfechos

| Desfecho | Definição | Domínio |
| --- | --- | --- |
| `pareado` | a entrevista seguinte foi encontrada | todas as origens |
| `sai_do_emprego` | destino não ocupado | pares |
| `formal_para_informal` | origem formal, destino ocupado e informal | pares com origem formal e destino observado |
| `muda_ocupacao_2` | COD de destino difere em 2 dígitos | pares com destino ocupado |
| `muda_ocupacao_3` | COD de destino difere em 3 dígitos | pares com destino ocupado |
| `mobilidade_descendente_aioe` | AIOE de destino menor que o de origem | pares com AIOE nos dois lados |
| `mobilidade_ascendente_aioe` | AIOE de destino maior que o de origem | pares com AIOE nos dois lados |

Formalidade: empregado com carteira, militar e estatutário são formais; sem carteira e trabalhador
familiar são informais; conta-própria e empregador são formais **apenas** com CNPJ declarado, e
ficam nulos sem declaração. Nenhum ausente vira zero: cada desfecho só existe no seu domínio.

## 4. Exposição à IA

O AIOE mede a exposição da ocupação à IA, por SOC2010. A PNADC classifica ocupação em COD, a
adaptação brasileira da ISCO-08. A ponte é **COD → ISCO-08 → SOC2010**:

- grupos civis: comparação em quatro dígitos;
- grupo 6 (agropecuária): dois dígitos, porque o IBGE reagrupa esse bloco e a repartição fina seria
  invenção;
- entradas agregadas de três dígitos da ponte BLS (211, 315) são incorporadas explicitamente;
- militares e o COD 5168 ficam **sem** exposição atribuída;
- entre os SOC de um mesmo COD o peso é uniforme — hipótese de construção declarada, não
  probabilidade oficial.

A exposição do COD é a média dos SOC ponderada por esse peso, ignorando elos sem valor em vez de
tratá-los como zero. O peso sem AIOE atribuído fica em `pnadc_cobertura_exposicao.json` e é
comparado com `config.yaml: limite_sem_match`.

**Escala**: o AIOE é padronizado entre ocupações, com desvio-padrão de 0,9445 entre os 416 códigos
com exposição. Os coeficientes são reportados por unidade de AIOE; como uma unidade equivale a cerca
de 1,06 desvio-padrão, o efeito por desvio-padrão é cerca de 5,5% menor que o coeficiente reportado.

## 5. Especificação

```
y ~ aioe_origem:pos + telework:pos + idade + idade_quadrado
    | cod_origem + sigla_uf^mes + sexo + raca + escolaridade
    + tempo_emprego_categoria + tamanho_empresa_categoria + setor
```

- `pos` marca o trimestre do choque (`config.yaml: choque`) e os seguintes.
- `cod_origem` absorve o nível permanente de cada ocupação: o coeficiente compara as **mudanças**
  entre pré e pós de ocupações com exposições diferentes, não os níveis entre ocupações.
- `sigla_uf^mes` absorve os componentes aditivos comuns a cada UF e mês, inclusive o nível do ciclo
  nacional; um choque nacional com incidência diferente por ocupação não é absorvido e pode covariar
  com a exposição.
- `telework:pos` está lá porque AIOE e teletrabalhabilidade são fortemente correlacionados entre
  ocupações; sem esse termo o coeficiente de AIOE recolhe a reorganização do trabalho remoto.
- Pesos: soma de V1028 da entrevista de **origem**. É peso transversal, não longitudinal.
- Cluster: UPA, o nível do desenho amostral.
- Modelo de probabilidade linear, não logit: com esse conjunto de efeitos fixos de alta dimensão o
  LPM é o que permite estimação e inferência viáveis, e o alvo é o efeito marginal médio.

O modelo de `pareado` é um **teste de atrito**: se a exposição previsse quem some do painel, os
demais desfechos estariam contaminados por seleção.

## 6. Matriz de mobilidade

Quintis de AIOE **fixos entre códigos ocupacionais** — e não entre pessoas —, de modo que a
composição do emprego não redefina as faixas entre os períodos. Para cada quintil de origem calcula-se
a distribuição ponderada dos quintis de destino, no pré e no pós, e a diferença entre eles.

A incerteza vem de um bootstrap multinomial **por UPA**, sorteando o cluster inteiro com suas
observações pré e pós juntas — o que preserva a correlação dentro da UPA e a dependência entre os
dois períodos. O teste de igualdade das matrizes é um Wald com a covariância do bootstrap e
pseudo-inversa, com graus de liberdade iguais ao posto da covariância.

## 7. Inferência

Erros-padrão agrupados por UPA, com graus de liberdade iguais ao número de clusters efetivamente
usados menos um, e intervalos de 95% pela t com esses graus de liberdade. Cada modelo grava
`clusters`, `n`, fórmula, pesos, versão do pyfixest e o SHA-256 do arquivo de dados que rodou.

Não há correção para testes múltiplos. São sete desfechos correlacionados: um p de 0,03 isolado não
deve ser lido como achado forte.

## 8. O que este desenho não identifica

1. **Adoção de IA não é observada.** O tratamento é um índice de exposição ocupacional construído
   nos EUA, aplicado à estrutura ocupacional brasileira. Nenhuma empresa ou trabalhador da amostra
   é observado adotando IA.
2. **O choque é único e nacional.** Os efeitos fixos de UF × mês absorvem o que é comum, mas qualquer
   fator que tenha atingido ocupações de alto AIOE de forma diferencial no mesmo período — retomada
   pós-pandemia, teletrabalho, ciclo setorial — entra no coeficiente.
3. **Seleção longitudinal permanece.** O peso é transversal e não há correção de atrito; o teste de
   `pareado` limita, mas não elimina, essa preocupação.
4. **Assimetria mecânica.** Quem parte de AIOE alto só pode descer no gradiente. O efeito fixo de
   ocupação absorve o nível, mas a leitura correta do par ascendente/descendente é a diferença pós
   menos pré, não o nível.
5. **Horizonte de um trimestre.** Realocação lenta, mudança de carreira e efeitos sobre entrada no
   mercado não aparecem nesta margem.
6. **Direção não é bem-estar.** AIOE menor é menos exposição, não salário menor nem emprego pior.
