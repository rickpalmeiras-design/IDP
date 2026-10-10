# Roteiro de fala · apresentação da dissertação

**Exposição ocupacional à inteligência artificial e transições no mercado de trabalho brasileiro**

Duração: **15 minutos exatos**, em 12 slides. O mesmo texto está nas notas do orador de cada slide do arquivo
`apresentacao_dissertacao.pptx` (no PowerPoint, modo Apresentador).

## Como usar

- O texto foi calibrado para **125 palavras por minuto**, um ritmo tranquilo de exposição acadêmica. Somadas, as leituras
  ocupam cerca de **14:54**, o que deixa uma folga curta para pausas e para a troca de slides.
- A coluna **Relógio** da tabela é o ponto de controle: ao terminar cada slide, o cronômetro deve marcar aquele tempo. Se
  estiver adiantado, respire e deixe o gráfico falar; se estiver atrasado, corte primeiro as ressalvas já ditas
  (o slide 9 e o slide 11 têm margem para isso).
- Ensaie com cronômetro. O ritmo de cada pessoa varia, e a estimativa acima é só um ponto de partida.

## Quadro de tempo

| Slide | Título | Tempo | Relógio | Palavras |
| ---: | --- | ---: | ---: | ---: |
| 1 | Abertura | 0:30 | 0:30 | 64 |
| 2 | A pergunta de pesquisa | 1:15 | 1:45 | 155 |
| 3 | O que a literatura já mostra | 1:15 | 3:00 | 151 |
| 4 | Dados: a PNAD Contínua em painel | 1:15 | 4:15 | 157 |
| 5 | Como medir a exposição à IA | 1:15 | 5:30 | 153 |
| 6 | Sete desfechos de transição | 1:00 | 6:30 | 126 |
| 7 | Desenho: diferenças em diferenças contínuas | 1:30 | 8:00 | 185 |
| 8 | A mobilidade subiu em todas as faixas | 1:15 | 9:15 | 153 |
| 9 | Resultado principal: o gradiente de exposição | 1:45 | 11:00 | 221 |
| 10 | Vínculo no emprego e teste de atrito | 1:15 | 12:15 | 156 |
| 11 | O que o desenho permite e o que não permite | 1:15 | 13:30 | 157 |
| 12 | Conclusões e próximos passos | 1:30 | 15:00 | 184 |
| | **Total** | **15:00** | | **1862** |

## Slide 1 · Abertura

> **Tempo:** 0:30 · **Ao terminar, o relógio marca:** 0:30

Agradeço a presença de todos e ao professor Danny, meu orientador. Sou Ricardo Carvalho e apresento, em quinze minutos, a minha dissertação: como a exposição das ocupações à inteligência artificial se relaciona com as transições de trabalho no Brasil depois do ChatGPT, com o painel da PNAD Contínua. São resultados preliminares, e vou dizer com clareza o que sustentam e o que ainda não.

## Slide 2 · A pergunta de pesquisa

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 1:45

Em 30 de novembro de 2022, o ChatGPT foi aberto ao público. Esse marco tem uma propriedade útil para quem estuda mercado de trabalho: é único, nacional, tem data certa e não depende de decisão de nenhum trabalhador ou empresa da amostra. A pergunta da dissertação é esta: trabalhadores em ocupações mais expostas à inteligência artificial passaram a apresentar transições de trabalho diferentes depois desse marco?

Três definições antes de seguir. Exposição é uma propriedade da ocupação, medida por um índice. Ela indica o quanto as habilidades da ocupação se aproximam do que a tecnologia faz, e não se alguém usa IA, nem se corre risco de demissão. Transição é o que acontece com a mesma pessoa entre duas entrevistas trimestrais consecutivas. O período vai de 2019 a 2025: quinze trimestres de origem antes do marco e doze depois. E o horizonte é curto, de um trimestre: mede-se o que acontece até a entrevista seguinte.

## Slide 3 · O que a literatura já mostra

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 3:00

A literatura tem três frentes. A primeira mede exposição. Felten, Raj e Seamans, em 2021, construíram o AIOE, que liga habilidades das ocupações a aplicações de inteligência artificial. Eloundou e coautores, em 2024, refazem o exercício tarefa a tarefa, para modelos de linguagem.

A segunda observa adoção e resultados. Brynjolfsson, Li e Raymond acompanham uma central de atendimento e medem ganho de produtividade. Humlum e Vestergaard, na Dinamarca, estimam efeitos nulos e precisos sobre rendimentos e horas dois anos após a adoção, com alguma recomposição de tarefas e troca de ocupação.

A terceira dá desenho e contexto. Acemoglu e Restrepo usam exposição diferencial para identificar efeitos. Ulyssea mostra que a informalidade é heterogênea, e Meghir e coautores, que a fronteira com o setor formal é atravessada com frequência.

A lacuna: não há, no Brasil, medida direta de adoção de IA em base representativa. Por isso uso exposição ocupacional num painel domiciliar.

## Slide 4 · Dados: a PNAD Contínua em painel

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 4:15

Os dados vêm da PNAD Contínua trimestral do IBGE, de 2019 a 2025. É um painel rotativo: cada domicílio é visitado cinco vezes, uma por trimestre. Isso permite tentar ligar a mesma pessoa entre dois trimestres seguidos, mas não existe identificador individual validado. Por isso reconstruí o par exigindo, ao mesmo tempo, mesma UPA, domicílio e número de ordem, mesmo sexo, mesmo dia e mês de nascimento e idade coerente.

O gráfico mostra a escala. São quase quatro milhões de pessoas-transições com exposição atribuída à origem. Dessas, 80,2% encontram o par na entrevista seguinte, e cada desfecho usa o seu próprio domínio, como o de destino ocupado, com 2,9 milhões. A taxa de pareamento varia entre 0,747 e 0,847 ao longo dos trimestres, com os valores mais baixos em 2020 e 2021, quando a coleta foi por telefone.

Um aviso: são pessoas-transições, e não pessoas únicas, e o próprio pareamento entra como desfecho, num teste de atrito.

## Slide 5 · Como medir a exposição à IA

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 5:30

O tratamento é o AIOE, publicado para a classificação ocupacional americana. Como a PNAD usa a classificação brasileira, construí uma ponte em duas etapas: da COD para a ISCO-08, e da ISCO-08 para a SOC. Quando uma ocupação brasileira se liga a várias americanas, o peso é uniforme, uma hipótese de construção que declaro como tal.

A cobertura é alta: 416 códigos recebem exposição, 413 entram na estimação, e só 1,08% do peso amostral fica sem valor. O índice é padronizado entre ocupações, com desvio-padrão de 0,9445. Uma unidade de AIOE equivale, portanto, a cerca de um desvio-padrão, e menor exposição não significa emprego pior. O histograma mostra uma distribuição ampla.

E há um cuidado: a exposição tem correlação de 0,702 com a teletrabalhabilidade. Por isso essa variável entra interagida com o período, para que a exposição não absorva a reorganização do trabalho remoto. Os coeficientes são sempre lidos por unidade de AIOE.

## Slide 6 · Sete desfechos de transição

> **Tempo:** 1:00 · **Ao terminar, o relógio marca:** 6:30

Estimo sete desfechos, em três famílias. A primeira é de continuidade e vínculo: o pareamento, que funciona como teste de atrito, a saída do emprego e a transição de formal para informal. A segunda é de mobilidade ocupacional: se a pessoa mudou de ocupação, em dois e em três dígitos da classificação. A terceira é de deslocamento no gradiente de exposição: a transição para uma ocupação menos exposta e para uma mais exposta.

Cada desfecho é estimado no seu próprio domínio, e ausência nunca vira zero: um destino não observado não quer dizer que a pessoa não mudou de ocupação. As duas margens direcionais só podem ser lidas juntas, porque têm uma assimetria mecânica: quem está numa ocupação muito exposta tem mais destinos possíveis abaixo dela.

## Slide 7 · Desenho: diferenças em diferenças contínuas

> **Tempo:** 1:30 · **Ao terminar, o relógio marca:** 8:00

O desenho é de diferenças em diferenças com tratamento contínuo. Não há grupo tratado e grupo de controle: há um marco temporal único e nacional, o lançamento do ChatGPT, e uma intensidade de tratamento que varia entre ocupações, dada pela exposição da ocupação de origem.

O período pré vai de 2019T1 a 2022T3, com quinze trimestres, e o pós, de 2022T4 a 2025T3, com doze. O trimestre do marco conta como pós, por convenção declarada antes da estimação. O parâmetro de interesse, beta, é o coeficiente da interação entre exposição e período pós. Ele compara a mudança entre pré e pós de ocupações com exposições diferentes, em pontos percentuais por unidade de AIOE.

A equação traz ainda a teletrabalhabilidade interagida com o pós, a idade, efeitos fixos de ocupação de origem e de UF por trimestre, e efeitos fixos de sexo, cor ou raça, escolaridade, tempo no emprego, tamanho do estabelecimento e setor.

A estimação é por modelo de probabilidade linear ponderado pelo peso da origem, com erros-padrão agrupados na UPA, em mais de trinta mil grupos. A mesma especificação vale para os sete desfechos.

## Slide 8 · A mobilidade subiu em todas as faixas

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 9:15

Antes de qualquer coeficiente, a descrição. À esquerda, as médias antes e depois do marco. A mudança de ocupação em três dígitos sobe de 23,6% para 31,8%, e em dois dígitos, de 20,9% para 28%. As duas margens direcionais sobem quase igual, de 12,8 e 12,9% para 17,4%. A transição de formal para informal vai de 5,2% a 8,8%, e a saída do emprego praticamente não se move. O pareamento também sobe, de 78,3% para 81,2%.

À direita, a matriz de mobilidade entre cinco faixas de exposição. A permanência na mesma faixa cai em todas elas, entre 3,6 e 8,1 pontos percentuais, e o teste de Wald rejeita a igualdade das matrizes.

A leitura é que houve um aumento generalizado das taxas medidas de rotatividade, e não uma mudança concentrada nas ocupações mais expostas. Um cuidado: a taxa medida de mudança de ocupação tem uma quebra em 2020 e 2021, que retomo adiante.

## Slide 9 · Resultado principal: o gradiente de exposição

> **Tempo:** 1:45 · **Ao terminar, o relógio marca:** 11:00

Este é o resultado principal. O gráfico mostra o coeficiente beta de cada desfecho, com intervalo de confiança de 95%, em pontos percentuais por unidade de AIOE.

O mais forte é o deslocamento no gradiente. Ocupações de origem com uma unidade a mais de exposição tiveram, do pré para o pós, um aumento 2,19 pontos percentuais maior na transição para ocupação menos exposta, e uma variação 1,36 ponto percentual menor na transição para ocupação mais exposta. Em magnitude, 2,19 corresponde a cerca de 12,6% da taxa pós, que é de 17,4%. A leitura é literal: compara mudanças entre pré e pós de ocupações com exposições diferentes, e não acompanha uma mesma ocupação cuja exposição aumente.

A mudança de ocupação também se associa à exposição: mais 0,86 ponto percentual em três dígitos e 0,28 em dois, o que sugere que parte do movimento adicional ocorre dentro das categorias de dois dígitos. Todos os intervalos excluem zero, exceto o do teste de atrito.

Duas ressalvas são essenciais. Primeira: nas margens direcionais, parte do resultado é mecânica, porque origens mais expostas têm mais destinos abaixo delas, e o desenho atual não separa isso do gradiente. Segunda: são sete desfechos correlacionados, sem correção para multiplicidade. O coeficiente de dois dígitos, com p de 0,030, é o que menos resiste e não deve ser citado isoladamente.

## Slide 10 · Vínculo no emprego e teste de atrito

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 12:15

Nas margens de vínculo, o sinal é contraintuitivo. Maior exposição se associa a menos saída do emprego, menos 0,25 ponto percentual, e a menos transição de formal para informal, menos 0,67. Ou seja, nesse período, quem está em ocupações mais expostas não mostrou deterioração relativa do vínculo.

Na informalização, o coeficiente da teletrabalhabilidade é positivo, mais 1,73 ponto percentual, enquanto o da exposição é negativo. Como os índices têm escalas diferentes, o desenho não identifica qual força explica o aumento agregado.

Esse padrão é compatível com a ideia, de Autor e Thompson, de que a automação pode preservar o vínculo e fazer o ajuste recair sobre o rendimento. Mas compatibilidade não é teste, e esta pesquisa só observa quantidades, não preços.

Por fim, o teste de atrito: o coeficiente do pareamento é menos 0,261, com p de 0,064. Não rejeito a estabilidade, mas está perto do limiar. Não posso dizer que a seleção longitudinal esteja descartada.

## Slide 11 · O que o desenho permite e o que não permite

> **Tempo:** 1:15 · **Ao terminar, o relógio marca:** 13:30

É por isso que o trabalho dedica tanto espaço aos limites. À esquerda, o que os resultados sustentam: houve aumento generalizado da rotatividade; há um gradiente condicional detectável, da ordem de dois pontos percentuais por unidade de exposição; e, nas margens de vínculo, o sinal é oposto ao da leitura alarmista.

À direita, o que não sustentam. Não é evidência causal: é um único cenário de estimação, sem estudo de evento, sem teste de tendências anteriores ao marco e sem bateria de sensibilidade. A adoção de IA não é observada, o tratamento é um índice de exposição potencial, e o marco é único e nacional.

E há uma descontinuidade de medida. A taxa de mudança de ocupação em três dígitos cai de 30% para 15% entre 2019T4 e 2020T1, fica entre 13% e 15% durante a coleta telefônica e volta a 34% em 2021T4. A causa não está demonstrada, e é o limite mais sério do trabalho.

## Slide 12 · Conclusões e próximos passos

> **Tempo:** 1:30 · **Ao terminar, o relógio marca:** 15:00

Resumindo, em três níveis. No descritivo, a mobilidade subiu para todos, e não só para os mais expostos. Como associação condicional, existe um gradiente detectável, da ordem de dois pontos percentuais por unidade de AIOE, e as margens de vínculo não mostram deterioração. No nível causal, o desenho atual não sustenta a afirmação. O que a pesquisa entrega, hoje, é uma descrição cuidadosa e uma agenda clara para chegar a uma resposta causal, se ela existir.

Por isso a agenda tem uma ordem. Primeiro, tratar a quebra de medida de 2020 e 2021 e definir a janela homogênea. Segundo, o estudo de evento, com teste conjunto dos coeficientes anteriores ao marco, que diz se existe desenho a defender. Terceiro, uma bateria mínima de sensibilidade: janelas, agrupamento, tendência por exposição e a especificação sem teletrabalhabilidade.

Quarto, trocar a medida pela específica para modelos de linguagem, de Eloundou e coautores, e rodar o placebo com teletrabalhabilidade. Depois, a sensibilidade a tendências não paralelas e os estimadores para tratamento contínuo. As extensões, como rendimentos, vêm por último.

Agradeço a atenção e fico à disposição para as perguntas.

## Referências citadas nos slides

- ACEMOGLU, D.; RESTREPO, P. Robots and jobs. Journal of Political Economy, v. 128, n. 6, p. 2188–2244, 2020. DOI 10.1086/705716.
- AUTOR, D.; THOMPSON, N. Expertise. Journal of the European Economic Association, v. 23, n. 4, p. 1203–1271, 2025. DOI 10.1093/jeea/jvaf023.
- BRYNJOLFSSON, E.; LI, D.; RAYMOND, L. Generative AI at work. The Quarterly Journal of Economics, v. 140, n. 2, p. 889–942, 2025. DOI 10.1093/qje/qjae044.
- DINGEL, J. I.; NEIMAN, B. How many jobs can be done at home? Journal of Public Economics, v. 189, p. 104235, 2020. DOI 10.1016/j.jpubeco.2020.104235.
- ELOUNDOU, T.; MANNING, S.; MISHKIN, P.; ROCK, D. GPTs are GPTs: labor market impact potential of LLMs. Science, v. 384, n. 6702, p. 1306–1308, 2024. DOI 10.1126/science.adj0998.
- FELTEN, E. W.; RAJ, M.; SEAMANS, R. Occupational, industry, and geographic exposure to artificial intelligence: a novel dataset and its potential uses. Strategic Management Journal, v. 42, n. 12, p. 2195–2217, 2021. DOI 10.1002/smj.3286.
- HUMLUM, A.; VESTERGAARD, E. Still waters, rapid currents: early labor market transformation under generative AI. NBER Working Paper 33777. Cambridge, MA: National Bureau of Economic Research, 2025. Disponível em: https://www.nber.org/papers/w33777.
- MEGHIR, C.; NARITA, R.; ROBIN, J.-M. Wages and informality in developing countries. American Economic Review, v. 105, n. 4, p. 1509–1546, 2015. DOI 10.1257/aer.20121110.
- ULYSSEA, G. Informality: causes and consequences for development. Annual Review of Economics, v. 12, p. 525–546, 2020. DOI 10.1146/annurev-economics-082119-121914.

As demais referências da dissertação ficam no arquivo `dissertacao/referencias.bib`.
