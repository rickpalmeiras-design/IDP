# Migração da estimação: de R para Python

A etapa 05, que estima os sete modelos de probabilidade linear, começou em R com o pacote
`fixest` e passou para Python com o `pyfixest` no commit `0bca695`, de 08/09/2026. Esta pasta
mostra o de-para entre os dois motores e guarda a verificação numérica de que eles entregam o
mesmo resultado.

O script em R não foi apagado: está em [`R/legado/modelos.R`](../R/legado/modelos.R), e é ele
que roda na verificação. O motor em Python é a função `estimar_pyfixest` de
[`src/estimacao.py`](../src/estimacao.py).

## Por que trocar

O motor em R rodava como subprocesso: a etapa 05 gravava um arquivo de job em JSON, chamava
`Rscript`, e lia de volta os CSV que o R escrevia. Isso obrigava a manter R instalado, uma
biblioteca de pacotes separada e um contrato de arquivos entre as duas linguagens. Com o
`pyfixest`, a estimação acontece dentro do mesmo processo que prepara os dados e monta as
tabelas, e o projeto passa a ter uma dependência a menos.

## O de-para, linha a linha

| O que precisa acontecer | R, com `fixest` | Python, com `pyfixest` |
| --- | --- | --- |
| Ler os dados da estimação | `fread(j$dados, na.strings = c('', 'NA', 'NaN'))` | `pd.read_csv(job['dados'], low_memory=False)` |
| Tratar `pos` como número | `as.numeric(as.logical(pos))` | `d['pos'].astype(float)` |
| Categoria ausente vira `ignorado` | `d[is.na(get(v)), (v) := 'ignorado']` e `as.factor` | `.astype('string').fillna('ignorado').astype('category')` |
| Estimar | `feols(fml, data = d, weights = ~peso_total, vcov = ~id_upa)` | `pf.feols(formula, data=d, weights='peso_total', vcov={'CRV1': 'id_upa'})` |
| Pegar os coeficientes | `coeftable(m)` | `modelo.tidy()` |
| Saber quais linhas entraram no modelo | `fixest::obs(m)` | `modelo._data.index` |
| Graus de liberdade conservadores | `length(unique(upa[used_obs])) - 1` | `used_upa.nunique() - 1` |
| Valor-p conservador | `2 * pt(-abs(t), df)` | `2 * stats.t.sf(abs(t), df)` |
| Intervalo de 95% | `qt(.975, df)` | `stats.t.ppf(1 - alpha/2, df)` |
| Matriz de variância | `vcov(m)` | `modelo._vcov` |
| Gravar resultado e metadados | `write.csv` e `write_json` | `to_csv` e `json_write` |

Fórmula, pesos, variável de cluster e efeitos fixos são escritos exatamente igual nos dois
motores: o `pyfixest` aceita a mesma sintaxe de fórmula do `fixest`, com a barra separando os
efeitos fixos e o acento circunflexo para a interação `sigla_uf^mes`. Por isso o arquivo de
job da etapa 05 serve aos dois sem nenhuma tradução.

### A única diferença de nome

O `fixest` escreve a interação na ordem em que ela aparece no modelo, `pos:telework`; o
`pyfixest` escreve `telework:pos`. Os dois são o mesmo termo. Essa diferença quebrou o Painel
B da Tabela 4 na migração, porque `resultados.py` procurava o nome antigo em um literal fixo;
o commit da migração corrigiu isso. Na comparação desta pasta os termos são reordenados antes
de parear, e as duas grafias ficam registradas nas colunas `termo_no_r` e `termo_no_python`.

## A verificação

[`comparar_motores.py`](comparar_motores.py) refaz a conferência do zero:

```
uv run python migracao-r-python/comparar_motores.py
```

1. Confere o sha256 de `data/interim/estimacao/05_pnadc.csv` contra o que está registrado no
   job da etapa 05. Sem isso, a comparação não teria valor: os dois motores precisam ter lido
   o mesmo arquivo, byte a byte.
2. Roda `R/legado/modelos.R` com uma cópia do job apontando a saída para
   `resultados/motor-r/`. A estimação oficial, em `output/modelos/`, não é tocada.
3. Pareia os dois conjuntos termo a termo e grava as diferenças.

### O que a verificação produziu

<!-- RESULTADOS -->

## O que tem em `resultados/`

| Arquivo | Conteúdo |
| --- | --- |
| `comparacao_coeficientes.csv` | Uma linha por modelo e termo, com estimativa, erro-padrão, valor-p conservador e intervalo nos dois motores, e a diferença entre eles. |
| `resumo.json` | As diferenças máximas, a versão de cada pacote e a confirmação de que a amostra e o número de clusters batem. |
| `motor-r/` | A saída bruta do motor R: coeficientes, matriz de variância e metadados dos sete modelos. |
| `job_motor_r.json` | O job usado na reestimação em R, igual ao da etapa 05 com a pasta de saída trocada. |

## Duas coisas que a verificação não cobre

A igualdade entre os motores não diz nada sobre a identificação: se a especificação estiver
errada, os dois estarão igualmente errados. E a comparação parte do arquivo já preparado pela
etapa 04; tudo o que acontece antes dele, do pareamento à construção dos desfechos, nunca
passou por R e por isso não entra neste de-para.
