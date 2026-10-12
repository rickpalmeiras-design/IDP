// Conteúdo falado de cada slide: ato da história, tempo previsto e leitura.
//
// É a fonte única do roteiro. O gerador copia daqui as notas do orador de cada
// slide, e o gerador do roteiro.md também. Todo número vem da dissertação
// (capítulos 3 a 5 e tabelas em dissertacao/tabelas/).
//
// A história tem três atos: contexto (slides 2 e 3), tensão (4 a 8) e
// resolução (9 a 12).
//
// Trechos entre colchetes, como [Aponte para o histograma.], são
// marcas de gesto: não se leem em voz alta e não entram na contagem de tempo.
//
// Tempo: 15 minutos reservados, 900 segundos. As leituras foram escritas para
// caber em cerca de 13 minutos e meio a 125 palavras por minuto, o que deixa
// folga para pausas e troca de slides. `node contar.js` mostra o tempo de cada uma.

const RITMO_PALAVRAS_POR_MINUTO = 125;

const ATOS = ['Contexto', 'Tensão', 'Resolução'];

const SLIDES = [
  {
    id: 'titulo', secao: 'Abertura', ato: null, segundos: 30,
    titulo: 'Exposição ocupacional à inteligência artificial e transições no mercado de trabalho brasileiro',
    leitura:
`Obrigado a todos pela presença, e obrigado ao professor Danny, meu orientador. Sou Ricardo Carvalho. Nos próximos quinze minutos, vou contar uma história em três partes: o contexto, a tensão e a resposta. A pergunta é simples. Depois do ChatGPT, o trabalho no Brasil mudou mais para quem está nas ocupações mais expostas à inteligência artificial?`,
  },
  {
    id: 'pergunta', secao: 'Abertura', ato: 'Contexto', segundos: 100, titulo: 'A IA chegou para todos no mesmo dia. O trabalho mudou?',
    leitura:
`Começo pelo contexto. Em 30 de novembro de 2022, o ChatGPT foi aberto ao público. De um dia para o outro, uma ferramenta que escreve, resume e programa ficou ao alcance de qualquer pessoa.

Para quem estuda o mercado de trabalho, esse marco é útil. Ele tem data certa, vale para o país inteiro e não depende da decisão de nenhum trabalhador da pesquisa.

Daí vem a pergunta da dissertação: quem trabalha em ocupações mais expostas à IA passou a mudar de trabalho de um jeito diferente depois desse marco?

Por que isso importa? Porque mudar de trabalho mexe com renda, com informalidade e com o tipo de qualificação que o país precisa oferecer. E quase tudo o que se sabe vem de países ricos.

Duas palavras são importantes. Exposição é uma característica da ocupação, e não da pessoa. Ela mede o quanto as tarefas da ocupação se parecem com o que a IA faz. Não diz se a pessoa usa IA, nem se ela vai perder o emprego. E transição é o que acontece com a mesma pessoa de um trimestre para o seguinte.`,
  },
  {
    id: 'literatura', secao: 'Abertura', ato: 'Contexto', segundos: 75, titulo: 'A literatura mede a exposição; o Brasil não mede o uso',
    leitura:
`O que já se sabe sobre isso? A literatura anda em três frentes.

A primeira mede a exposição. Felten, Raj e Seamans criaram o índice que eu uso, chamado AIOE. Ele liga as habilidades de cada ocupação ao que a IA consegue fazer. Eloundou e coautores fizeram algo parecido para os modelos de linguagem.

A segunda observa quem já adotou a IA. Numa central de atendimento, a produtividade subiu. Na Dinamarca, dois anos depois, salários e horas praticamente não mudaram.

A terceira me dá o método e o contexto brasileiro, em que as pessoas entram e saem da informalidade com frequência.

E aqui está a lacuna. No Brasil, não existe uma pesquisa grande que pergunte quem usa IA no trabalho. Então eu uso o que existe: a exposição da ocupação, numa pesquisa feita nos domicílios.`,
  },
  {
    id: 'dados', secao: 'Dados e método', ato: 'Tensão', segundos: 70, titulo: 'A PNAD Contínua segue a mesma pessoa por cinco trimestres',
    leitura:
`Agora começa a tensão, porque responder a essa pergunta não é simples. O primeiro obstáculo está nos dados.

Uso a PNAD Contínua do IBGE, de 2019 a 2025. Cada domicílio é entrevistado cinco vezes, uma por trimestre. Isso permite acompanhar a mesma pessoa. O problema é que a pesquisa não traz um número de identificação confiável para cada pessoa. Então eu reconstruí os pares: mesmo domicílio, mesmo sexo, mesma data de aniversário e idade coerente.

O gráfico mostra o tamanho da base. São quase quatro milhões de pares possíveis, e cerca de oitenta por cento encontram a entrevista seguinte. Cada desfecho usa a sua própria parte da base, por isso as barras têm tamanhos diferentes.

Um detalhe: eu conto transições, e não pessoas. A mesma pessoa pode aparecer até quatro vezes.`,
  },
  {
    id: 'exposicao', secao: 'Dados e método', ato: 'Tensão', segundos: 80, titulo: 'A exposição à IA varia muito entre as ocupações',
    leitura:
`O segundo obstáculo é a medida. O índice de exposição foi feito para as ocupações dos Estados Unidos, e a PNAD usa a classificação brasileira. Por isso construí uma ponte em duas etapas: da classificação brasileira para a internacional, e da internacional para a americana. Quando uma ocupação brasileira corresponde a várias americanas, cada uma recebe o mesmo peso. É uma escolha minha, e eu a declaro.

A cobertura ficou boa: 416 ocupações recebem o índice, e só cerca de um por cento da amostra fica de fora. [Aponte para o histograma.] O gráfico mostra que as ocupações se espalham por toda a escala.

E há um terceiro obstáculo. As ocupações mais expostas à IA também são as que mais podem ser feitas de casa. A correlação é de 0,7. Por isso o teletrabalho entra no modelo, para que a IA não leve o crédito pelo que foi efeito da pandemia.`,
  },
  {
    id: 'desfechos', secao: 'Dados e método', ato: 'Tensão', segundos: 60, titulo: 'Sete desfechos: vínculo, mobilidade e direção',
    leitura:
`Para saber se o trabalho mudou, olho para sete desfechos, em três grupos.

O primeiro é o vínculo. A pessoa saiu do emprego? Passou do emprego formal para o informal? E, como controle, ela foi encontrada de novo na entrevista seguinte?

O segundo é a mobilidade: a pessoa mudou de ocupação?

O terceiro é a direção: ela foi para uma ocupação menos exposta à IA, ou para uma mais exposta?

Duas regras. Quando não vejo o destino, não conto como se a pessoa tivesse ficado parada. E as duas direções sempre se leem juntas, porque quem está no topo da exposição tem mais espaço para descer do que para subir.`,
  },
  {
    id: 'desenho', secao: 'Dados e método', ato: 'Tensão', segundos: 80, titulo: 'Sem grupo de controle, comparo intensidades de exposição',
    leitura:
`O último obstáculo é o desenho. Não existe um grupo que recebeu a IA e outro que não recebeu. O ChatGPT chegou para todos no mesmo dia. O que muda é a intensidade: algumas ocupações estão mais expostas do que outras.

Por isso uso diferenças em diferenças com tratamento contínuo. Em palavras simples: comparo o antes e o depois do marco, e pergunto se essa mudança foi maior nas ocupações mais expostas. O antes tem quinze trimestres, e o depois tem doze.

O número que importa é o beta, em destaque na equação. Ele diz quantos pontos percentuais a mais cada desfecho mudou, para cada unidade a mais de exposição.

O modelo também leva em conta o teletrabalho, a idade, a ocupação de origem, o estado em cada trimestre e características como sexo, escolaridade e setor. E os erros são calculados por área de coleta, em mais de trinta mil grupos.`,
  },
  {
    id: 'descritivo', secao: 'Resultados', ato: 'Tensão', segundos: 75, titulo: 'A mobilidade subiu em todas as faixas de exposição',
    leitura:
`Antes de qualquer modelo, vamos olhar os dados brutos. E aqui a tensão aumenta.

[Aponte para o gráfico de barras deitadas.] Aqui estão as médias antes e depois do marco. Mudar de ocupação ficou bem mais comum: passou de cerca de 24 para 32 por cento. Ir para uma ocupação menos exposta subiu, mas ir para uma mais exposta subiu na mesma medida. A passagem do formal para o informal também subiu. Só a saída do emprego ficou praticamente parada.

[Aponte para o gráfico das cinco faixas, Q1 a Q5.] Agora, as cinco faixas de exposição, da menor para a maior. Em todas elas, ficar na mesma faixa ficou menos comum.

Ou seja: a mobilidade subiu para todo mundo, e não só para quem está mais exposto à IA. Essa é a tensão do trabalho. Se tudo se mexeu, a IA explica alguma parte desse movimento? É isso que o modelo vai responder.`,
  },
  {
    id: 'resultado', secao: 'Resultados', ato: 'Resolução', segundos: 90, titulo: 'Mais exposição, mais mudança para ocupações menos expostas',
    leitura:
`E esta é a resposta principal. Cada ponto do gráfico é o beta de um desfecho, e a linha em volta é a margem de erro.

[Aponte para o primeiro ponto do gráfico.] O resultado mais forte é a direção. Quanto mais exposta a ocupação de origem, mais as pessoas passaram a ir para ocupações menos expostas. Para cada unidade a mais de exposição, essa transição subiu cerca de 2,2 pontos percentuais a mais. Não é pouco: equivale a cerca de um oitavo da taxa do período depois do marco. [Aponte para o último ponto do gráfico.] E o movimento contrário, ir para uma ocupação mais exposta, ficou 1,4 ponto menor.

Mudar de ocupação também ficou um pouco mais comum nas ocupações mais expostas, quase um ponto a mais.

Agora, duas ressalvas, para ser honesto. A primeira: parte do resultado de direção é mecânica, porque quem já está no topo tem mais espaço para descer. A segunda: são sete testes ao mesmo tempo, sem correção para isso. O resultado mais fraco, o de mudança de ocupação em dois dígitos, não deve ser citado sozinho.`,
  },
  {
    id: 'vinculo', secao: 'Resultados', ato: 'Resolução', segundos: 80, titulo: 'Mais exposição veio com o vínculo no emprego preservado',
    leitura:
`E o emprego? Aqui está a surpresa. [Aponte para os dois primeiros números.] Era de se esperar que os mais expostos perdessem o emprego ou caíssem na informalidade. Não foi o que apareceu. Mais exposição veio junto com um pouco menos de saída do emprego e menos passagem do formal para o informal.

O terceiro número mostra que, na informalidade, quem aparece associado a mais informalização é o teletrabalho, e não a IA. Como os dois índices têm escalas diferentes, não dá para dizer qual força pesa mais.

Uma explicação possível vem de Autor e Thompson: a tecnologia pode manter o emprego e mudar o salário. Mas eu não observo salários. Então isso é uma hipótese, e não um teste.

Por fim, o controle. A chance de reencontrar a pessoa quase variou com a exposição, perto do limite de significância. Por isso não posso descartar que as perdas de entrevista influenciem o resultado.`,
  },
  {
    id: 'limites', secao: 'Conclusão', ato: 'Resolução', segundos: 80, titulo: 'Os dados mostram associação, ainda não causalidade',
    leitura:
`Então, o que esses resultados permitem dizer, e o que não permitem?

Eles permitem dizer três coisas. A mobilidade subiu para todos. Existe um gradiente: quanto mais exposta a ocupação, mais as pessoas foram para ocupações menos expostas, cerca de dois pontos por unidade de exposição. E o vínculo dos mais expostos não piorou.

Eles não permitem dizer que a IA causou isso. Ainda falta o estudo de evento, que testa se as ocupações já se comportavam de forma diferente antes do marco. Eu não observo quem usa IA, só quem está exposto. E o marco é um só, para o país inteiro.

E há o limite mais sério. No começo de 2020, justamente quando a entrevista passou a ser por telefone, a taxa medida de mudança de ocupação caiu pela metade, de 30 para 15 por cento. Ela só voltou no fim de 2021. A causa dessa quebra ainda não está demonstrada.`,
  },
  {
    id: 'conclusao', secao: 'Conclusão', ato: 'Resolução', segundos: 80, titulo: 'Mudou a direção, não o vínculo; a causa segue em aberto',
    leitura:
`Para fechar, a resposta em três níveis.

Primeiro, o que os dados mostram: depois do ChatGPT, a mobilidade subiu para todos, e não só para os mais expostos.

Segundo, a associação: existe um gradiente de cerca de dois pontos por unidade de exposição, em direção a ocupações menos expostas. E o vínculo não piorou.

Terceiro, a causalidade: o desenho atual ainda não permite afirmá-la.

O que eu entrego hoje é uma descrição cuidadosa e um caminho claro para chegar à resposta causal, se ela existir. Esse caminho tem cinco passos, em ordem. Primeiro, tratar a quebra de 2020 e 2021. Segundo, o estudo de evento. Terceiro, os testes de sensibilidade. Quarto, uma medida feita para modelos de linguagem e um placebo com o teletrabalho. Quinto, métodos próprios para tratamento contínuo. Salários e outras extensões vêm depois.

Muito obrigado. Fico à disposição para as perguntas.`,
  },
];

module.exports = { SLIDES, ATOS, RITMO_PALAVRAS_POR_MINUTO };
