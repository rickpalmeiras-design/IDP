# Guia de estudo: da fonte aos desfechos (Seções 3.1 a 3.6)

Material de estudo, não texto da dissertação. Cobre o Capítulo 3 até a Seção 3.6, que é
tudo o que vem antes da estimação, mais uma explicação da regressão ao final, porque sem
ela as escolhas anteriores não fazem sentido.

Cada seção segue a mesma estrutura: **o que é**, **por que foi feito assim**, **números
para saber de cor** e **se a banca perguntar**. Os números vêm do texto atual da
dissertação e das saídas do pipeline; se algum deles mudar, o guia precisa ser refeito.

---

## Mapa do capítulo

| Seção | Pergunta que responde |
| --- | --- |
| 3.1 | Como isso roda e como alguém confere? |
| 3.2 | De onde vêm os dados e qual é a unidade analisada? |
| 3.3 | Como se sabe que é a mesma pessoa nos dois trimestres? |
| 3.4 | Quem entra na amostra e quem fica de fora, e por quê? |
| 3.5 | Como se mede exposição de uma ocupação brasileira a uma medida americana? |
| 3.6 | O que exatamente está sendo explicado? |

A ordem não é arbitrária: cada seção só pode ser justificada depois da anterior. Você
não define desfecho sem ter par, não tem par sem fonte, e não tem tratamento sem ponte
ocupacional.

---

## 3.1 Roteiro de execução e reprodutibilidade

**O que é.** O procedimento é uma cadeia de sete etapas numeradas, de 00 a 06, cada uma
com script próprio, saída própria e registro próprio. Nenhuma etapa recalcula o que a
anterior produziu, e nenhuma roda antes que a anterior tenha gravado seu artefato.

**Por que assim.** Três garantias, que a dissertação apresenta como parte do método e não
como detalhe de implementação:

1. **Restrição de dados.** Microdados individuais não são materializados na máquina local
   em nenhuma etapa, e a rotina recusa consulta sem agregação.
2. **Registro de execução.** Cada etapa grava início, fim, situação e resultado, de modo
   que etapa interrompida não se confunde com etapa concluída.
3. **Rastro criptográfico.** Cada modelo grava, junto dos coeficientes, a fórmula
   executada, o nível de agrupamento, a variável de ponderação, o número de grupos, o
   *hash* SHA-256 do arquivo que entrou na estimação e uma cópia congelada do script.

**Para saber de cor.** Sete etapas; a 04 constrói o painel, a 05 estima, a 06 consolida.
As etapas 05 e 06 podem ser refeitas sem reconstruir o painel.

**Se a banca perguntar.**
- *Por que não trabalhar com os microdados direto?* Porque a restrição elimina a
  possibilidade de manipulação inadvertida de dado individual identificável e obriga toda
  decisão de agregação a ser explícita, no código, antes de descer qualquer coisa.
- *Como eu reproduzo isso?* Rodando a cadeia na ordem. Se o *hash* do arquivo bater, os
  coeficientes são os mesmos.

---

## 3.2 Fonte e unidade de observação

**O que é.** PNAD Contínua trimestral do IBGE, acessada pelo repositório Base dos Dados.
Janela disponível de 2019T1 a 2025T4, o que dá **27 trimestres elegíveis como origem**,
de 2019T1 a 2025T3 (o último trimestre não pode ser origem porque não existe trimestre
seguinte para formar o par).

A unidade de observação é a **transição individual**: a entrevista de uma pessoa em `t`
ligada à entrevista da mesma pessoa em `t+1`. Exposição e covariáveis vêm da origem; os
desfechos vêm da comparação entre origem e destino.

Para estimar, as transições são agrupadas em **células**. Uma célula reúne os registros
que coincidem em tudo o que o modelo usa: trimestre, UF, UPA, ocupação de origem e de
destino, condição de ocupação e formalidade no destino, indicador de pareamento, mudanças
de código e todas as covariáveis. De cada célula guardam-se o número de pessoas, a soma
dos pesos e a soma dos quadrados dos pesos.

**Por que assim.** Porque, se todas as variáveis são constantes dentro da célula, estimar
sobre células ponderando pela soma dos pesos dá **exatamente os mesmos coeficientes** que
estimar sobre indivíduos. Essa é a equação (1) do capítulo. Não é aproximação nem atalho.

**Cuidado com o alcance.** A equivalência é de cálculo, não de identificação. Ela
justifica usar células; não diz nada sobre causalidade. E vale para os coeficientes: a
reprodução exata dos erros-padrão dependeria também das correções de amostra finita, que
contam células e não pessoas.

**Para saber de cor.** 4.014.438 células para 4.017.289 transições. 99,9% das células têm
uma única pessoa, e o máximo é quatro. Ou seja, a agregação quase não compacta nada.

**Se a banca perguntar.**
- *Agregar não perde informação?* Não, porque a célula é definida pela combinação exata
  das variáveis do modelo. Dentro dela, todo mundo tem o mesmo desfecho e o mesmo vetor
  de regressores.
- *E os erros-padrão?* Os escores por UPA são preservados, porque a UPA define a célula e
  portanto cada célula está inteira dentro de uma UPA. A igualdade numérica exata
  dependeria das correções de amostra finita; a comparação direta não é feita, porque
  exigiria os microdados que o desenho não usa.

---

## 3.3 Construção do par pessoa-trimestre

**O que é.** A PNADC pública não tem identificador longitudinal validado. O par é
construído por identidade reconstruída, exigindo **todas** estas condições ao mesmo
tempo:

| | Condição |
| --- | --- |
| a | mesma UPA, mesmo domicílio, mesmo número de ordem na família |
| b | trimestre seguinte e visita seguinte |
| c | mesmo sexo declarado |
| d | mesmo dia e mesmo mês de nascimento |
| e | ano de nascimento diferindo em no máximo um |
| f | idade avançando zero ou um ano |
| g | chave não duplicada no trimestre, dos dois lados |

**Por que assim.** A regra (g) é conservadora de propósito: havendo ambiguidade, o
registro não é pareado em direção nenhuma, em vez de resolvido por critério arbitrário. A
regra (b) tem duas consequências: a quinta visita nunca é origem, e o último trimestre
não entra no denominador de atrito.

**O que isso não é.** Não é identificação certa. São regras que produzem correspondência
plausível: admitem falso par e perdem par verdadeiro. Além disso, o painel segue quem é
reencontrado **no mesmo domicílio**; quem muda de casa entre as visitas some.

**Para saber de cor.** A taxa ponderada de pareamento fica entre **0,747 e 0,847** nos 27
trimestres, e os piores valores estão em 2020 e 2021, quando a coleta foi
majoritariamente por telefone por causa da pandemia.

**Se a banca perguntar.**
- *Por que não usar o identificador da pesquisa?* Porque ele não é validado
  longitudinalmente na base pública. Tratá-lo como se fosse geraria pares falsos sem
  qualquer controle.
- *Quem some do painel é aleatório?* Não se sabe, e é por isso que o pareamento virou
  desfecho: o teste de atrito da Seção 3.6 verifica se o gradiente de pareamento em
  relação à exposição mudou entre os períodos.

---

## 3.4 Filtragem da amostra

**O que é.** Uma sequência de cortes, cada um com regra de desenho declarada. O funil,
em pessoas-transições:

| Etapa | Quantidade | Regra do corte |
| --- | --- | --- |
| B. Origens elegíveis | 4.017.289 | ocupado, 18 a 65 anos, visitas 1 a 4, trimestre com seguinte disponível |
| C. Exposição atribuída | 3.963.359 (98,7% de B) | AIOE e teletrabalhabilidade disponíveis para a ocupação de origem |
| D. Par encontrado | 3.178.582 (80,2% de C) | as sete regras de identidade da Seção 3.3 |
| E. Destino ocupado | 2.882.225 (90,7% de D) | condição de ocupação no destino igual a ocupado |
| F. Domínio de mobilidade | 2.879.139 (99,9% de E) | código e AIOE observados na origem e no destino |
| G. Domínio de formalidade | 1.677.310 (52,8% de D) | ramo lateral a partir de D: origem formal e destino classificável |

**Por que assim.** Cada desfecho usa o domínio em que está definido. G não é continuação
de F: é um ramo que sai de D, porque para estudar informalização você precisa de origem
formal, e não de destino ocupado com código conhecido.

**Duas armadilhas de leitura.**
1. **Ausência nunca vira zero.** Destino não observado não é "não mudou de ocupação", é
   indefinido. Converter em zero criaria efeito onde só há falta de dado.
2. **São pessoas-transições, não pessoas.** O mesmo indivíduo contribui com até quatro
   pares ao longo do painel, então os pesos somados não são contagem de indivíduos
   independentes.

**Se a banca perguntar.**
- *Por que 20% dos casos não pareiam?* Combinação de mudança de domicílio, não resposta e
  a regra conservadora de duplicidade. A série por trimestre está na Figura 1, e a queda
  se concentra no período de coleta telefônica.
- *Esse corte não seleciona a amostra?* Seleciona, e é por isso que existe o teste de
  atrito. Ele não resolve o problema, apenas verifica uma forma específica dele.

---

## 3.5 Medida de exposição à inteligência artificial

**O que é.** O tratamento é o AIOE de Felten, Raj e Seamans, construído para a
classificação americana SOC2010. A PNADC usa a COD, adaptação brasileira da ISCO-08. Logo
é preciso uma ponte em duas etapas: **COD → ISCO-08 → SOC2010**.

**Regras da ponte.**

| | Regra |
| --- | --- |
| a | grupos civis comparados em quatro dígitos |
| b | grupo 6 (agropecuária) em dois dígitos, porque o IBGE reagrupa esse bloco |
| c | entradas agregadas de três dígitos da correspondência oficial são incorporadas |
| d | militares e o código 5168 não recebem exposição |
| e | entre os SOC ligados a um mesmo COD, peso uniforme |

A regra (e) é hipótese declarada, não probabilidade oficial de correspondência. Saber
disso é importante: é o primeiro lugar onde a banca vai bater.

**Como a exposição do código é calculada.** Média ponderada dos AIOE dos SOC ligados
àquele COD, com pesos uniformes, **ignorando** os elos sem valor observado em vez de
tratá-los como zero. Tratar como zero produziria atenuação mecânica proporcional à
incompletude da ponte. O mesmo procedimento vale para a teletrabalhabilidade de Dingel e
Neiman, usada como controle.

**Para saber de cor.**
- 434 códigos COD de quatro dígitos na estrutura oficial; **427 recebem ao menos um elo**;
  **1.148 elos** no total; no máximo **37 SOC** para um mesmo COD.
- **416 códigos** recebem exposição, **413** recebem também teletrabalhabilidade, e são
  esses 413 que entram na estimação.
- **1,08%** do peso amostral fica sem AIOE na origem, contra um limite de 15% fixado antes
  de estimar.
- Entre os 416 códigos: média **0,0053** e desvio-padrão **0,9445**. Ponderando por
  trabalhador, média **−0,221** e desvio-padrão **0,981**, ou seja, o emprego brasileiro
  se concentra em ocupações menos expostas que a média entre ocupações.
- Correlação entre AIOE e teletrabalhabilidade: **0,702**.

**Duas advertências que precisam acompanhar todo coeficiente.**
1. **Escala.** Os coeficientes são reportados por unidade de AIOE. Como uma unidade
   equivale a cerca de 1,06 desvio-padrão, o efeito por desvio-padrão é cerca de 5,5%
   menor que o número da tabela.
2. **Direção não é hierarquia.** AIOE menor significa menos exposição, não emprego pior,
   salário menor ou posição inferior.

**Se a banca perguntar.**
- *Por que peso uniforme entre os SOC?* Porque não existe distribuição oficial de emprego
  por elo COD-SOC que justificasse outro peso. A alternativa seria inventar pesos, o que
  seria menos transparente. A hipótese está declarada e é candidata a teste de
  sensibilidade.
- *A medida é de 2021, anterior aos modelos generativos. Isso não invalida o marco de
  2022?* É a limitação central da escolha, e está declarada na Seção 2.3. O AIOE mede
  exposição à inteligência artificial em sentido amplo; usá-la com um marco generativo
  supõe que a ordenação das ocupações por exposição ampla se aproxime da ordenação por
  exposição generativa.
- *Por que controlar teletrabalho?* Por causa da correlação de 0,702. Sem esse termo, o
  coeficiente de exposição absorveria a reorganização do trabalho remoto no pós-pandemia.

---

## 3.6 Definição dos desfechos

**O que é.** Sete desfechos binários, em três famílias, cada um com seu domínio:

**(i) Continuidade e vínculo**

| Desfecho | Vale 1 quando | Domínio |
| --- | --- | --- |
| Pareamento | a entrevista seguinte foi encontrada | todas as origens elegíveis |
| Saída do emprego | o destino não está ocupado | pares |
| Formal para informal | o destino está ocupado e é informal (0 se ocupado formal ou não ocupado) | origem formal e destino classificável |

**(ii) Mobilidade ocupacional**

| Desfecho | Vale 1 quando | Domínio |
| --- | --- | --- |
| Muda de ocupação (2 dígitos) | o código difere nos dois primeiros dígitos | destino ocupado e ambos os códigos observados |
| Muda de ocupação (3 dígitos) | o código difere nos três primeiros dígitos | idem |

**(iii) Deslocamento no gradiente**

| Desfecho | Vale 1 quando | Domínio |
| --- | --- | --- |
| Mobilidade descendente | o AIOE do destino é menor que o da origem | AIOE observado nos dois lados |
| Mobilidade ascendente | o AIOE do destino é maior que o da origem | idem |

**Formalidade, em detalhe.** Segue o dicionário oficial: carteira assinada, militar e
estatutário são formais; sem carteira e trabalhador familiar auxiliar são informais;
conta-própria e empregador são formais **apenas** com CNPJ declarado, e ficam indefinidos
sem declaração. Deixar indefinido, em vez de imputar informalidade, evita correlação
espúria entre informalidade medida e não resposta.

**Dois desfechos exigem cuidado especial.**

1. **Pareamento é teste de atrito, não resultado substantivo.** E o teste tem alcance
   limitado: o coeficiente verifica apenas se o **gradiente** de pareamento em relação à
   exposição mudou entre os períodos. Diferenças permanentes de retenção entre ocupações
   são absorvidas pelo efeito fixo e não são testadas. Não rejeitar é o desejável, mas não
   prova que a exposição seja irrelevante para quem fica no painel.

2. **As margens direcionais têm um canal mecânico.** Origens mais expostas têm mais
   destinos possíveis abaixo delas no gradiente, e vice-versa. Se `m` é a probabilidade de
   trocar de ocupação e `F_c` a fração de destinos menos expostos que a origem `c`, então
   descer tem probabilidade `m × F_c`. Um aumento geral de mobilidade eleva isso em
   `Δm × F_c`, mais nas origens com mais destinos abaixo. Esse componente varia com a
   exposição sem nada de específico sobre IA, e o desenho atual **não o separa** do
   gradiente estimado. Por isso as duas margens são lidas sempre em conjunto.

**Se a banca perguntar.**
- *Por que destino não ocupado entra como zero na informalização?* Porque o desfecho mede
  a probabilidade de passar a uma ocupação informal entre origens formais, e não a
  probabilidade de informalidade condicional a continuar ocupado. A definição está
  explícita no Quadro 3.
- *Por que dois níveis de dígitos para mudança de ocupação?* Porque a diferença entre eles
  informa se o movimento é dentro da mesma categoria ampla ou entre categorias.
- *Mobilidade descendente é ruim?* Não necessariamente. É movimento para ocupação menos
  exposta à IA, e exposição não é hierarquia salarial.

---

## A regressão, em linguagem simples

A equação estimada, para o par `i` com ocupação de origem `c`, UF `u` e trimestre `t`:

```
y = β·(AIOE_c × Pós_t) + γ·(Telework_c × Pós_t) + δ₁·idade + δ₂·idade²
    + α_c + λ_ut + (efeitos fixos categóricos) + erro
```

**1. O que a regressão faz.** Procura os números que, multiplicados pelas características
e somados, chegam o mais perto possível do desfecho observado, minimizando a soma dos
erros ao quadrado. Cada coeficiente responde: se essa variável subir uma unidade e o resto
ficar parado, quanto muda o desfecho, em média?

**2. O desfecho é 0 ou 1.** A média de uma variável assim é uma proporção, então o modelo
ajusta a probabilidade de o desfecho valer 1, e o coeficiente se lê em pontos percentuais.
É o modelo de probabilidade linear. Vantagem: leitura direta e milhares de efeitos fixos
sem problema de convergência. Custo: previsão pode sair de [0,1] e os erros são
heterocedásticos por construção, o que exige erro-padrão robusto e agrupado.

**3. Efeitos fixos são o coração do desenho.** Cada um dá uma média própria a cada grupo,
o que equivale a dizer ao modelo: compare apenas dentro do grupo.
- `α_c`, ocupação de origem: tira o nível permanente de cada ocupação. Programador troca
  de ocupação mais que porteiro por mil razões alheias à IA, e isso sai da conta.
- `λ_ut`, UF por trimestre: tira tudo o que atingiu igualmente todas as ocupações de um
  estado em um trimestre, inclusive o nível do ciclo macroeconômico.
- Categóricos: sexo, raça, escolaridade, tempo de emprego, tamanho do estabelecimento e
  setor, que tiram diferenças de composição.

**4. Por que o coeficiente é de uma interação.** O AIOE não varia no tempo dentro da
ocupação. Como `α_c` já dá um nível por ocupação, o AIOE sozinho seria redundante e não
seria identificado. O que sobra é `AIOE × Pós`, que vale zero antes de 2022T4 e vale o
próprio AIOE depois. Logo `β` responde: a mudança do pré para o pós foi diferente entre
ocupações com exposições diferentes? É daí que vem o nome diferenças em diferenças.

**5. Idade, idade ao quadrado e pesos.** Idade entra nos dois termos porque a relação com
mobilidade é curva, não reta. Os pesos são amostrais, da entrevista de origem, e fazem o
modelo responder sobre a população. São transversais, não longitudinais, porque a PNADC
não publica peso longitudinal, e isso é limite declarado.

**6. Erro-padrão agrupado por UPA.** O cálculo convencional supõe observações
independentes, o que é falso: pessoas do mesmo setor censitário vivem os mesmos choques.
Agrupar por UPA trata cada UPA como a unidade que varia de forma independente. São mais de
trinta mil grupos.

**7. Como ler um número da Tabela 4.** O coeficiente de transição para ocupação menos
exposta é +2,187 pontos percentuais, com erro-padrão 0,105 e intervalo de 1,982 a 2,393.
Em português: comparando o pós ao pré, e mantidos fixos ocupação de origem, par
UF-trimestre, teletrabalhabilidade interagida com o período e as demais características,
ocupações de origem com uma unidade a mais de AIOE tiveram aumento 2,19 pontos percentuais
maior na probabilidade de transitar para ocupação menos exposta. O intervalo não cruza
zero, então é distinguível de zero; isso não quer dizer que seja grande, já que equivale a
cerca de um oitavo da taxa pós daquela transição.

**8. O que a regressão não entrega.** Causalidade. Para ler `β` como efeito da IA seria
preciso que, sem o lançamento do ChatGPT, ocupações mais e menos expostas tivessem seguido
trajetórias paralelas. Isso é hipótese, não resultado da conta, e é o que a Seção 3.10
discute.

---

## As dez perguntas mais prováveis, com resposta curta

1. **Por que o AIOE, se ele é anterior aos modelos generativos?** Porque é a medida
   validada e publicada para exposição ocupacional à IA, e a hipótese de que a ordenação
   ampla se aproxima da generativa está declarada. A substituição pela medida de Eloundou
   et al. é a primeira robustez prevista.
2. **A ponte COD-ISCO-SOC não é arbitrária?** As regras estão declaradas elo a elo, com
   resolução diferente para grupos civis e agropecuária, e o peso uniforme é hipótese
   explícita. 427 dos 434 códigos recebem elo.
3. **Por que peso transversal e não longitudinal?** Porque a PNADC não publica peso
   longitudinal. Está declarado como limite.
4. **O pareamento não gera seleção?** Gera risco, e por isso o pareamento é desfecho. O
   teste tem alcance limitado, como o próprio texto registra.
5. **Por que modelo de probabilidade linear e não logit?** Interpretação direta em pontos
   percentuais e viabilidade com milhares de efeitos fixos. Os custos estão declarados.
6. **Por que agrupar os erros na UPA?** Porque é o nível de amostragem em que os choques
   são comuns. Agrupar na ocupação é alternativa defensável e está na agenda.
7. **O coeficiente é grande ou pequeno?** Cerca de 2,2 pontos percentuais por unidade de
   AIOE, contra base pós de 17,4% na transição para ocupação menos exposta, ou seja, algo
   como um oitavo.
8. **A quebra de 2020 e 2021 não contamina tudo?** A descontinuidade coincide com a
   mudança no modo de coleta, a causa não está demonstrada, e a estimação usa a série
   inteira. Isso está registrado como limite conhecido e encabeça a agenda.
9. **Por que não há robustez?** Porque esta versão apresenta um cenário único. A agenda do
   Capítulo 5 organiza o que falta.
10. **O resultado prova que a IA está deslocando trabalhadores?** Não. Mostra um gradiente
    condicional de mobilidade associado à exposição, em um período que contém outras
    mudanças, e sem adoção de IA observada.

---

## Como usar este guia

Uma sugestão de sequência, se o tempo for curto:

1. Leia a explicação da regressão primeiro. Sem ela, as seções anteriores parecem
   burocracia.
2. Depois volte para 3.5 e 3.6, que são onde estão as decisões que a banca questiona.
3. Por último 3.3 e 3.4, que são de execução e têm resposta objetiva.
4. Decore apenas os números marcados como "para saber de cor". São poucos e resolvem a
   maior parte das perguntas factuais.
