# Guia da regressão, do zero: o modelo, o erro-padrão e o valor-p

Material de estudo, fora da dissertação. Escrito para quem está começando: não supõe
econometria prévia, e cada conceito aparece antes de ser usado. Os números são os do
trabalho, e quase todos podem ser conferidos com uma calculadora comum, o que é a melhor
forma de aprender.

Companheiro do [GUIA_DE_ESTUDO.md](GUIA_DE_ESTUDO.md), que cobre as Seções 3.1 a 3.6.

**Ordem sugerida:** Partes 1 a 3 na sequência. A Parte 4 é o coração do guia (valor-p). A
Parte 5 é treino com a Tabela 4. As Partes 6 a 8 servem de consulta.

---

# Parte 1. O que uma regressão faz

## 1.1 O problema

Você tem uma coisa que quer explicar (o **desfecho**) e várias coisas que podem explicá-la
(as **variáveis explicativas**). No seu trabalho o desfecho é, por exemplo, "esta pessoa
passou para uma ocupação menos exposta à IA?", e uma das explicativas é a exposição da
ocupação de origem.

A regressão responde a uma pergunta bem específica:

> Quando essa variável explicativa sobe uma unidade, e todas as outras da equação ficam
> paradas, quanto muda o desfecho, em média?

Cada resposta dessas é um **coeficiente**.

## 1.2 A reta que erra menos

Imagine três ocupações, com exposição e taxa de mudança de ocupação:

| Ocupação | Exposição | Taxa de mudança |
| --- | --- | --- |
| A | 0 | 10% |
| B | 1 | 13% |
| C | 2 | 16% |

Traçando a reta que passa por esses pontos: começa em 10% e sobe 3 pontos percentuais a
cada unidade de exposição. O coeficiente é 3.

Na vida real os pontos nunca ficam alinhados. Sempre sobra uma diferença entre o que a
reta prevê e o que se observa: é o **erro** (ou resíduo). A regressão escolhe a reta que
torna a **soma dos erros ao quadrado** a menor possível. Daí o nome mínimos quadrados.

Por que ao quadrado, e não o erro simples? Por duas razões: erros positivos e negativos
não se cancelam, e errar muito em um ponto passa a custar desproporcionalmente mais do que
errar pouco em vários. A reta resultante fica, por isso, mais sensível a pontos distantes.

## 1.3 "Mantendo o resto constante"

Com mais de uma variável explicativa, a regressão deixa de ser uma reta e vira um plano,
mas a leitura de cada coeficiente permanece a mesma: é o efeito **parcial**, aquele que
sobra depois de descontar o que as outras variáveis já explicam.

Exemplo. Suponha que ocupações mais expostas sejam também ocupações de maior escolaridade,
e que gente com mais escolaridade mude mais de emprego. Sem controlar escolaridade, o
coeficiente de exposição captura as duas coisas misturadas. Colocando escolaridade na
equação, o coeficiente de exposição passa a comparar pessoas de mesma escolaridade.

Essa é a operação central da econometria aplicada, e também a sua maior fragilidade: ela
só desconta o que você colocou na equação. O que ficou de fora continua dentro do
coeficiente.

## 1.4 O que a regressão não faz

Ela não descobre causa. Ela mede associação condicional. Se duas coisas andam juntas
depois dos controles, o coeficiente aparece, não importa qual seja a causa de qual. Para
ler um coeficiente como efeito causal é preciso um argumento adicional, externo à conta.
No seu caso, esse argumento é o desenho de diferenças em diferenças, e a hipótese que ele
exige está na Seção 3.10.

---

# Parte 2. As peculiaridades do seu modelo

A equação estimada:

```
y = β·(AIOE_c × Pós_t) + γ·(Telework_c × Pós_t) + δ₁·idade + δ₂·idade²
    + α_c + λ_ut + (efeitos fixos categóricos) + erro
```

Cada pedaço tem uma razão de ser.

## 2.1 O desfecho vale 0 ou 1

Seus sete desfechos são binários: aconteceu (1) ou não aconteceu (0). A média de uma
variável assim é uma proporção. Se 100 pessoas têm desfecho 1 e 900 têm 0, a média é 0,10,
ou seja, 10%.

Como a regressão modela a média do desfecho, ela está modelando **a probabilidade de o
desfecho ser 1**. É o que se chama de **modelo de probabilidade linear**. A consequência
prática é a mais importante do guia:

> O coeficiente se lê em **pontos percentuais de probabilidade**.

Um coeficiente de 2,187 significa 2,187 pontos percentuais a mais de probabilidade, e não
2,187%. Se a probabilidade era 17,4%, ela passa a 19,6%, e não a 17,8%.

**Vantagens.** Leitura direta, e possibilidade de incluir milhares de efeitos fixos, coisa
que um logit não suportaria bem.

**Custos, que estão declarados na dissertação.** O modelo pode prever probabilidade menor
que 0 ou maior que 1, o que é logicamente impossível; e os erros são necessariamente
heterocedásticos, isto é, têm variância diferente conforme a probabilidade prevista. Por
isso o erro-padrão não pode ser o convencional, o que nos leva à Parte 3.

## 2.2 Efeitos fixos: comparar dentro do grupo

Um efeito fixo é, na prática, uma variável indicadora para cada categoria: uma para cada
ocupação, uma para cada combinação de estado e trimestre, e assim por diante. Cada uma
ganha seu próprio nível.

O efeito disso é uma frase só: **o modelo passa a comparar apenas dentro do grupo**.

- `α_c` (ocupação de origem): programador troca de ocupação mais que porteiro por razões
  que nada têm a ver com IA. Esse nível permanente sai da conta.
- `λ_ut` (UF por trimestre): tudo o que atingiu igualmente todas as ocupações de um estado
  em um trimestre sai também, inclusive o nível do ciclo econômico nacional.
- Categóricos (sexo, raça, escolaridade, tempo de emprego, tamanho do estabelecimento,
  setor): tiram diferenças de composição.

**O preço.** O coeficiente usa apenas a variação que sobra depois de remover tudo isso.
Não é a variação bruta dos dados. Por isso se diz que o coeficiente vem "de dentro" dos
grupos.

## 2.3 Por que o coeficiente é de uma interação

Aqui está o ponto que trava quase todo iniciante.

O AIOE é fixo dentro da ocupação: ele não muda ao longo do tempo. Como `α_c` já dá um
nível próprio a cada ocupação, colocar o AIOE sozinho seria repetir a mesma informação, e
o modelo não teria como separar os dois. Tecnicamente, o AIOE é **colinear** com o efeito
fixo de ocupação.

O que resta é o produto `AIOE × Pós`, que vale:

| Período | Valor do termo |
| --- | --- |
| Antes de 2022T4 | 0 (porque Pós = 0) |
| De 2022T4 em diante | o próprio AIOE da ocupação |

Então o coeficiente `β` responde:

> A mudança do período pré para o pós foi **diferente** entre ocupações com exposições
> diferentes?

É daí que vem o nome **diferenças em diferenças**: primeira diferença, entre pós e pré;
segunda diferença, entre ocupações mais e menos expostas.

**Ilustração numérica.** Imagine duas ocupações, uma com AIOE 0 e outra com AIOE 1:

| | Pré | Pós | Diferença |
| --- | --- | --- | --- |
| Ocupação com AIOE 0 | 15,0% | 17,0% | +2,0 |
| Ocupação com AIOE 1 | 15,5% | 19,7% | +4,2 |
| | | | **+2,2 = β** |

Note que β não olha para a diferença de nível entre as duas ocupações (0,5 ponto no pré).
Essa diferença é absorvida pelo efeito fixo. β olha só para o fato de uma ter subido 4,2 e
a outra 2,0.

Como o AIOE é contínuo, e não uma chave de tratado ou não tratado, esse é um DiD de
**tratamento contínuo**: o que se estima é um gradiente por unidade de exposição.

## 2.4 O termo de teletrabalhabilidade

Entra exatamente na mesma forma, `Telework × Pós`. A razão é empírica: a correlação entre
exposição à IA e teletrabalhabilidade entre ocupações é de **0,702**. São, em larga medida,
as mesmas ocupações. Como o período analisado contém a reorganização do trabalho remoto
pós-pandemia, sem esse termo o coeficiente de exposição absorveria parte dela.

## 2.5 Idade e idade ao quadrado

Mobilidade não cresce nem cai de forma constante com a idade: é alta na juventude, cai e
estabiliza. Com idade e idade² o modelo ajusta uma curva em vez de uma reta. É a forma
mais barata de acomodar uma relação não linear.

## 2.6 Pesos

Cada entrevista da PNADC representa um número diferente de brasileiros. A ponderação faz o
modelo responder sobre a população, e não sobre a amostra. O peso usado é o da entrevista
de origem, que é **transversal**, não longitudinal, porque a PNADC não publica peso
longitudinal. Isso é limitação declarada, não escolha de conveniência.

---

# Parte 3. De onde vem a incerteza

## 3.1 A ideia central

O coeficiente 2,187 não é "a verdade". É o que **esta** amostra produziu. Se o IBGE tivesse
sorteado outros domicílios, sairia um número um pouco diferente. Imagine repetir a pesquisa
mil vezes: você teria mil coeficientes, espalhados em torno de algum valor central. Esse
espalhamento é a incerteza.

Não dá para repetir mil vezes, então a estatística estima esse espalhamento a partir de uma
amostra só. O resultado dessa estimativa é o **erro-padrão**.

## 3.2 Erro-padrão

> **Erro-padrão** é o desvio-padrão que o coeficiente teria se você repetisse a pesquisa
> muitas vezes. Quanto menor, mais estável é a estimativa.

Na Tabela 4, o coeficiente de transição para menor AIOE é 2,187 com erro-padrão 0,105.
Leitura informal: se a pesquisa fosse refeita, o coeficiente ficaria tipicamente a menos de
0,1 ponto de distância do valor obtido.

Três coisas diminuem o erro-padrão: mais observações, menos variabilidade no desfecho e
mais variação na variável explicativa.

## 3.3 Por que agrupar por UPA

O cálculo convencional do erro-padrão supõe que cada observação traz informação nova e
independente. Isso é falso aqui: a PNADC sorteia setores censitários inteiros, as UPAs, e
pessoas do mesmo setor vivem os mesmos choques locais, o mesmo mercado de trabalho, a mesma
fábrica que fechou.

Se você ignora isso, o modelo pensa ter muito mais informação independente do que tem, e o
erro-padrão sai **pequeno demais**. Resultado: significância inflada, ou seja, você acredita
em coisa que os dados não sustentam.

Agrupar por UPA corrige isso, tratando cada UPA como a unidade que varia de forma
independente. No seu trabalho há entre **30.360 e 31.145 UPAs**, conforme o desfecho, o que
é bastante folga.

Detalhe técnico que está no código e no texto: os graus de liberdade são o número de grupos
menos um, e os intervalos usam a distribuição `t` com esses graus de liberdade. Com mais de
trinta mil grupos, `t` e normal são praticamente iguais, mas o texto registra o que o código
faz.

## 3.4 A estatística t

É a razão entre o coeficiente e seu erro-padrão:

```
t = coeficiente ÷ erro-padrão
```

Para o primeiro desfecho: 2,187 ÷ 0,105 = **20,8**. Ou seja, o coeficiente está a quase 21
erros-padrão de distância do zero. É muitíssimo longe.

Regra prática para memorizar: `|t|` acima de 2 corresponde, aproximadamente, a valor-p
abaixo de 0,05.

---

# Parte 4. O valor-p

## 4.1 A definição, com todas as palavras

> **Valor-p é a probabilidade de obter um resultado tão extremo quanto o observado, ou mais
> extremo, supondo que o efeito verdadeiro seja zero e que todas as suposições do modelo
> estejam corretas.**

Cada pedaço importa:

- **"tão extremo quanto o observado, ou mais"**: não é a probabilidade do valor exato, é a
  da cauda, tudo aquilo igual ou mais distante de zero.
- **"supondo que o efeito verdadeiro seja zero"**: essa suposição tem nome, **hipótese
  nula**. O valor-p é calculado dentro de um mundo imaginário em que não há efeito.
- **"e que todas as suposições estejam corretas"**: amostragem, forma funcional,
  agrupamento dos erros. Se o modelo estiver errado, o valor-p não conserta nada.

A definição oficial da American Statistical Association é equivalente: a probabilidade,
sob um modelo estatístico especificado, de que um resumo dos dados seja igual ou mais
extremo que o observado (Wasserstein e Lazar, 2016, *The American Statistician*, 70(2),
129-133).

## 4.2 Uma analogia

Você suspeita que uma moeda é viciada para cara. Joga 10 vezes e sai cara 9 vezes.

O valor-p pergunta: **se a moeda fosse honesta**, qual a chance de sair algo tão
desequilibrado quanto 9 caras, ou mais? A resposta é cerca de 2%. Como 2% é pouco, você
desconfia da hipótese de moeda honesta.

Repare no que essa conta **não** diz: ela não diz que há 2% de chance de a moeda ser
honesta. Ela diz que, se fosse honesta, um resultado assim seria raro. São coisas
diferentes, e confundi-las é o erro mais comum da área.

## 4.3 Como ele se relaciona com o t

Dado o `t`, o valor-p é a área nas caudas da distribuição além de `|t|`. Alguns pares que
vale a pena ter na cabeça:

| \|t\| | valor-p aproximado |
| --- | --- |
| 1,0 | 0,32 |
| 1,65 | 0,10 |
| 1,96 | 0,05 |
| 2,58 | 0,01 |
| 3,29 | 0,001 |
| 20,8 | muito menor que 0,001 |

É por isso que a Tabela 4 mostra `<0,001` em vários desfechos: o número é tão pequeno que
não vale a pena imprimir.

**Confira você mesmo.** Pareamento: coeficiente −0,261, erro-padrão 0,141. Divida:
−0,261 ÷ 0,141 = −1,85. Pela tabela acima, `|t|` de 1,85 fica entre 0,10 e 0,05, mais perto
de 0,06. A tabela informa p = 0,064. Bate.

## 4.4 O que muda o valor-p

Quatro coisas, e só elas:

1. **O tamanho do coeficiente.** Maior efeito, menor p.
2. **A variabilidade dos dados.** Mais ruído, maior p.
3. **O tamanho da amostra.** Mais observações, menor erro-padrão, menor p. **Este é o
   ponto perigoso**: com 4 milhões de observações, efeitos minúsculos ficam
   "significativos". Significância não é sinônimo de importância.
4. **O nível de agrupamento dos erros.** Agrupar na UPA dá p maior que ignorar o
   agrupamento; agrupar na ocupação daria p ainda maior, porque há menos grupos. Trocar o
   agrupamento muda o p sem mudar uma vírgula do coeficiente.

## 4.5 Os cinco erros clássicos

| Erro | Por que é errado |
| --- | --- |
| "p = 0,03 significa 3% de chance de a hipótese nula ser verdadeira" | O p é calculado **supondo** a nula verdadeira. Ele é a probabilidade dos dados dada a hipótese, não da hipótese dados os dados. |
| "p = 0,03 significa 3% de chance de o resultado ser por acaso" | Mesma inversão, em outras palavras. |
| "p menor quer dizer efeito maior" | O p mistura tamanho do efeito e precisão. Um efeito minúsculo com amostra gigante tem p minúsculo. |
| "p = 0,4 prova que não há efeito" | Ausência de evidência não é evidência de ausência. Pode ser só falta de precisão. O correto é olhar o intervalo: se ele vai de −5 a +5, o estudo não sabe nada. |
| "p pequeno valida o desenho" | O p não enxerga viés. Se houver variável omitida ou problema de medida, o p continua pequeno e o número continua errado. |

Os dois primeiros erros são exatamente os que a ASA destaca em seu comunicado de 2016.

## 4.6 O limiar de 0,05 é convenção, não lei da natureza

Não existe nada de especial em 5%. É um costume herdado. Um resultado com p = 0,049 e
outro com p = 0,051 são praticamente a mesma evidência, e tratá-los como categorias
opostas é arbitrário. Por isso a prática moderna prefere reportar o intervalo de confiança
e o tamanho do efeito, deixando o p como informação auxiliar.

## 4.7 Intervalo de confiança, que costuma ser mais útil

> Um intervalo de 95% é construído de tal modo que, repetindo o procedimento em muitas
> amostras, cerca de 95% dos intervalos conteriam o valor verdadeiro.

Na prática, ele responde direto à pergunta que interessa: **quais valores são compatíveis
com os meus dados?**

Regra de bolso: `coeficiente ± 1,96 × erro-padrão`.

**Confira você mesmo.** 2,187 ± 1,96 × 0,105 = 2,187 ± 0,206, o que dá [1,981; 2,393]. A
tabela mostra [1,982; 2,393]. A diferença mínima vem do uso da distribuição `t` em vez da
normal.

Relação com o valor-p: se o intervalo de 95% **não contém zero**, então p < 0,05. São a
mesma informação vista de dois ângulos. A vantagem do intervalo é mostrar a magnitude: no
caso, os dados são compatíveis com algo entre 1,98 e 2,39 pontos percentuais, e não com
qualquer valor.

## 4.8 Muitos testes ao mesmo tempo

Você estima **sete** desfechos. Cada teste a 5% tem 5% de chance de dar falso positivo. Se
os sete fossem independentes, a chance de pelo menos um falso positivo seria

```
1 − 0,95⁷ = 0,30
```

ou seja, cerca de 30%. Os seus desfechos são fortemente correlacionados, então o número
real é menor, mas o problema existe.

A dissertação não aplica correção formal e registra a ressalva no lugar dela. A consequência
prática está no texto: o coeficiente de mudança de ocupação em dois dígitos, com p = 0,030,
é o que menos resiste, e não deve ser citado isoladamente.

## 4.9 O caso especial do teste de atrito

Nos seis desfechos substantivos, rejeitar a nula é o achado. No teste de atrito é o
contrário: **não rejeitar é o resultado desejável**, porque rejeitar indicaria que a
exposição está associada a quem some do painel, o que contaminaria todo o resto.

E há uma sutileza que a dissertação faz questão de registrar: o coeficiente testa apenas se
o **gradiente** de pareamento mudou entre os períodos. Diferenças permanentes de retenção
entre ocupações são absorvidas pelo efeito fixo e não são testadas. Ou seja, p = 0,064 não
é um atestado de que não há seleção; é a ausência de um tipo específico de evidência de
seleção.

---

# Parte 5. Lendo a Tabela 4 linha a linha

Painel A, exposição interagida com o período. Todos os efeitos em pontos percentuais por
unidade de AIOE.

| Desfecho | Efeito | E.P. | IC 95% | p | Como ler |
| --- | --- | --- | --- | --- | --- |
| Transição para menor AIOE | +2,187 | 0,105 | [1,982; 2,393] | <0,001 | O resultado mais forte. Ocupações mais expostas passaram a mandar mais gente para ocupações menos expostas. Parte disso pode ser o canal mecânico da Seção 3.6. |
| Muda de ocupação (3 díg.) | +0,861 | 0,136 | [0,594; 1,128] | <0,001 | Mais troca de ocupação em resolução fina. |
| Muda de ocupação (2 díg.) | +0,278 | 0,128 | [0,027; 0,529] | 0,030 | O mais frágil da tabela. O intervalo quase toca o zero e não há correção para multiplicidade. Não citar sozinho. |
| Saída do emprego | −0,250 | 0,075 | [−0,398; −0,103] | <0,001 | Contraintuitivo: mais exposição, **menos** saída do emprego. |
| Pareamento (atrito) | −0,261 | 0,141 | [−0,536; +0,015] | 0,064 | Não rejeita, que é o desejável, mas fica perto do limiar e com sinal negativo. Não descarta seleção. |
| Formal para informal | −0,673 | 0,094 | [−0,858; −0,488] | <0,001 | Mais exposição, menos informalização. |
| Transição para maior AIOE | −1,364 | 0,103 | [−1,566; −1,161] | <0,001 | Espelho do primeiro: menos movimento para cima no gradiente. |

Painel B, teletrabalhabilidade interagida com o período, na mesma estimação. O destaque é
a transição de formal para informal: **+1,734**, com p < 0,001, contra −0,673 da exposição.
Os dois índices têm escalas diferentes, então as magnitudes não são diretamente
comparáveis, mas os sinais opostos são a razão de o Capítulo 4 relatar os dois gradientes
sem atribuir o aumento agregado a nenhum deles.

**Um exercício que ensina muito:** pegue qualquer linha, divida o efeito pelo erro-padrão e
compare com a tabela de `t` da Seção 4.3. Depois calcule o intervalo com ±1,96 e confira com
a coluna do IC. Em dez minutos você domina a mecânica da tabela inteira.

---

# Parte 6. Erros de leitura que a banca costuma cobrar

1. Dizer "2,19%" em vez de "2,19 pontos percentuais".
2. Dizer que a IA **causou** o movimento. O desenho dá associação condicional.
3. Dizer que o efeito é grande. São 2,19 pontos contra base de 17,4%, cerca de um oitavo.
4. Ler as margens direcionais separadamente, ignorando o canal mecânico.
5. Tratar p = 0,064 como "quase significativo" e usar isso como se fosse achado.
6. Esquecer que o coeficiente é por unidade de AIOE, que equivale a cerca de 1,06
   desvio-padrão.
7. Interpretar AIOE menor como emprego pior. É direção de exposição, não hierarquia.
8. Citar o desfecho de dois dígitos isoladamente.

---

# Parte 7. Glossário de bolso

| Termo | Em uma linha |
| --- | --- |
| Coeficiente | Quanto muda o desfecho quando a variável sobe uma unidade, mantido o resto |
| Resíduo | Diferença entre o observado e o previsto pelo modelo |
| Mínimos quadrados | Critério que escolhe a reta que minimiza a soma dos resíduos ao quadrado |
| Modelo de probabilidade linear | Regressão comum aplicada a desfecho 0/1; coeficiente em pontos percentuais |
| Heterocedasticidade | Variância do erro que muda conforme a observação |
| Efeito fixo | Nível próprio para cada categoria; faz o modelo comparar dentro do grupo |
| Colinearidade | Duas variáveis que carregam a mesma informação; o modelo não separa as duas |
| Interação | Produto de duas variáveis; deixa o efeito de uma depender da outra |
| Diferenças em diferenças | Comparar a mudança ao longo do tempo entre grupos diferentes |
| Tratamento contínuo | Intensidade de tratamento que varia em grau, e não em sim ou não |
| Erro-padrão | Desvio-padrão do coeficiente entre amostras hipotéticas |
| Agrupamento (cluster) | Reconhecer que observações do mesmo grupo não são independentes |
| Estatística t | Coeficiente dividido pelo erro-padrão |
| Hipótese nula | A suposição de que o efeito verdadeiro é zero |
| Valor-p | Probabilidade de um resultado tão extremo quanto o observado, se a nula fosse verdadeira |
| Intervalo de confiança | Faixa de valores compatíveis com os dados, sob o procedimento adotado |
| Significância estatística | Convenção de chamar de achado o que tem p abaixo de um limiar |
| Multiplicidade | Vários testes ao mesmo tempo aumentam a chance de falso positivo |
| Ponderação amostral | Fazer cada observação valer pelo número de pessoas que representa |
| Graus de liberdade | Quantidade de informação independente disponível para estimar a incerteza |

---

# Parte 8. Autoavaliação

Responda sem olhar, depois confira.

1. Por que o AIOE não entra sozinho na equação?
2. O que significa, em português, o coeficiente 2,187?
3. Um p de 0,03 quer dizer que há 3% de chance de não haver efeito. Certo ou errado?
4. O que acontece com o valor-p se você dobrar o tamanho da amostra e o efeito continuar o mesmo?
5. Por que agrupar os erros na UPA e não em cada pessoa?
6. No teste de atrito, qual resultado é o desejável e por quê?
7. O intervalo [−0,536; +0,015] permite afirmar que o efeito é zero?
8. Por que o desfecho de dois dígitos é o mais frágil da tabela?

**Respostas.**

1. Porque ele é constante dentro da ocupação e, com efeito fixo de ocupação na equação,
   seria colinear com esse efeito fixo. O que se identifica é a interação com o período.
2. Que a mudança do pré para o pós na probabilidade de transitar para ocupação menos
   exposta foi 2,187 pontos percentuais maior em ocupações com uma unidade a mais de AIOE,
   mantidos os controles e os efeitos fixos.
3. Errado. O p é calculado supondo que não há efeito; ele não dá a probabilidade dessa
   suposição.
4. Diminui, porque o erro-padrão cai. É por isso que, com amostra enorme, significância
   diz pouco sobre relevância.
5. Porque a amostragem sorteia setores censitários inteiros e pessoas do mesmo setor
   compartilham choques. Ignorar isso produz erro-padrão pequeno demais.
6. Não rejeitar, porque rejeitar indicaria que a exposição está associada a quem some do
   painel, o que contaminaria os demais desfechos. E mesmo não rejeitando, o teste só cobre
   mudança no gradiente, não seleção em geral.
7. Não. Permite dizer que os dados são compatíveis com valores entre −0,54 e +0,02, o que
   inclui zero, mas também inclui efeitos negativos de tamanho relevante.
8. Porque tem o maior valor-p dos significativos (0,030), intervalo quase tocando o zero, e
   porque são sete testes sem correção para multiplicidade.
