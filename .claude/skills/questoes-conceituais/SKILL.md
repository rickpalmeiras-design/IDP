---
name: questoes-conceituais
description: Gera questoes conceituais Verdadeiro/Falso (nivel 1 de Bloom - lembranca/reconhecimento) a partir de qualquer documento de estudo (aula, capitulo, artigo, manual, documentacao tecnica), agnostico de tema. Use quando o usuario pedir para gerar questoes, questoes verdadeiro/falso, quiz conceitual, questoes de lembranca ou de Bloom, revisar/testar conceitos de um material, ou invocar /questoes-conceituais.
argument-hint: "<arquivo> <quantidade> [--foco \"topicos\"] [--dominio \"tema/publico\"]"
---

# Questoes Conceituais (V/F)

Gera um conjunto de questoes Verdadeiro/Falso que testam **apenas reconhecimento**
de conceitos (nivel 1 da taxonomia de Bloom) ensinados em um documento de estudo,
qualquer que seja o tema. A relevancia dos conceitos escolhidos e ancorada no
tema/publico do proprio documento — nao existe uma lista fixa de "o que perguntar";
o que conta como central se extrai do material em maos.

## Quando usar

- Pedidos como: "gera questoes sobre este capitulo", "crie um quiz
  verdadeiro/falso sobre esse material", "quero testar se memorizei os
  conceitos desta aula", "/questoes-conceituais capitulo3.md 20".
- NAO usar para questoes de multipla escolha, dissertativas, estudos de caso,
  ou qualquer coisa que exija aplicar/analisar/avaliar — isso extrapola o
  nivel 1 de Bloom que esta skill cobre. Se pedirem isso, avise que a skill
  e limitada a V/F de lembranca e pergunte se querem prosseguir mesmo assim.

## Argumentos

Os argumentos chegam em `$ARGUMENTS` como texto livre — tanto na forma
posicional quanto em linguagem natural. Resolva assim:

1. **`<arquivo>`** (obrigatorio): o token que parece um caminho de arquivo
   (`.md`, `.txt`, `.pdf`, etc.), citado ou nao. Se o caminho informado nao
   existir, procure arquivos com nome parecido no mesmo diretorio (typo
   obvio) e confirme com o usuario antes de prosseguir — nunca assuma
   silenciosamente qual arquivo ele quis dizer.
2. **`<quantidade>`** (obrigatorio, default 10): o primeiro inteiro livre nos
   argumentos que nao faca parte de `--foco`/`--dominio`. Se nao houver
   nenhum inteiro, use 10 e avise no relatorio final que o default foi
   aplicado.
3. **`--foco "topicos"`** (opcional): conceitos/secoes a priorizar nesta
   rodada de geracao. Tambem aceite formas naturais como "focando em X" ou
   "sobre a parte de Y".
4. **`--dominio "tema/publico"`** (opcional): tema e publico-alvo, formato
   livre (ex.: "biologia celular / estudantes de medicina"). Se ausente,
   infira do proprio conteudo do documento no passo 3 do procedimento.

Exemplos de entrada equivalentes:
- `capitulo3.md 20`
- `gere 20 questoes a partir de capitulo3.md`
- `capitulo3.md 15 --foco "ciclo de Krebs" --dominio "bioquimica / graduacao em biomedicina"`

## Procedimento (ReAct)

1. **Resolver argumentos**: extraia caminho, quantidade, `--foco` e
   `--dominio` conforme acima. Se o caminho nao existir, confirme com o
   usuario antes de continuar.
2. **Ler o documento**: use Read. Para `.pdf`, use o parametro `pages` se o
   documento for extenso. Se o arquivo for `.pptx`/`.docx` e o Read falhar
   ou retornar conteudo nao-textual/ilegivel, **nao invente conteudo** —
   avise o usuario e sugira converter para `.md` ou `.pdf` primeiro.
3. **Identificar tema/publico**: use `--dominio` se informado; senao,
   infira do conteudo (titulo, introducao, vocabulario recorrente, nivel de
   profundidade). Declare esse tema explicitamente — ele ancora a heuristica
   do proximo passo. Se o documento misturar temas ou o tema nao ficar
   claro, priorize os conceitos mais recorrentes/estruturais do texto e
   declare no relatorio final qual tema foi assumido.
4. **Extrair conceitos candidatos** aplicando o teste-mestre, parametrizado
   pelo tema/publico identificado:

   > "Alguem que estuda [tema] precisa lembrar deste conceito para
   > raciocinar ou agir bem em [dominio]?"

   Se sim, e candidato a questao. Se e trivia periferica, descarte. Gere
   uma lista de candidatos **maior que a quantidade solicitada** — ela deve
   cobrir, quando presentes no material:

   - Frameworks, modelos e metodologias e suas caracteristicas distintivas.
   - Principios, leis e regras acionaveis do dominio.
   - Definicoes de conceitos centrais e termos tecnicos (o vocabulario que
     estrutura o tema).
   - Relacoes causais e trade-offs ("se X entao Y", "A difere de B
     porque...").
   - Classificacoes, taxonomias e categorias (tipos, niveis, camadas,
     fases).
   - Funcao/papel de componentes — quando o ponto e o que o componente faz
     ou qual problema resolve, nao seu nome ou data.

   **Excluir sempre** (trivia, em qualquer tema):
   - Datas especificas — salvo quando a data em si e o conceito ensinado.
   - Nomes proprios como item de memorizacao — so incluir quando associar
     autor <-> contribuicao (ou descobridor <-> descoberta) for o conceito
     ensinado.
   - Numeros/estatisticas pontuais como fim em si.
   - Anedotas e exemplos ilustrativos — importa o principio que ilustram,
     nao o exemplo em si.
   - Detalhes visuais/de formatacao do documento ou dos slides.

5. **Selecionar os N mais relevantes** para o tema identificado, respeitando
   `--foco` quando informado (priorize conceitos das secoes/topicos citados,
   sem excluir totalmente o resto do material). Se a quantidade solicitada
   for maior que o numero de conceitos de qualidade disponiveis, gere quantos
   der com qualidade e avise isso no relatorio final — **nunca infle com
   trivia so para bater o numero**.
6. **Redigir 1 afirmacao V/F por conceito**, seguindo as regras de redacao
   abaixo, alternando V/F em ordem embaralhada (nao agrupar todas as
   verdadeiras e depois todas as falsas).
7. **Montar o arquivo** (questoes + gabarito justificado) no formato de
   saida abaixo e salvar no caminho-irmao do documento fonte.
8. **Reportar** ao usuario: caminho do arquivo salvo, tema/publico
   detectado ou usado, quantidade final de questoes, quantas V e quantas F,
   e uma lista curta dos conceitos cobertos.

## Regras de redacao das afirmacoes

1. **Balanceamento ~50/50** entre Verdadeiro e Falso, em ordem embaralhada.
2. **Uma afirmacao, um conceito** — nunca misture dois conceitos na mesma
   frase (isso obrigaria o aluno a avaliar duas coisas ao mesmo tempo).
3. **Falsas sao equivocos plausiveis**, nao negacoes absurdas. Tecnicas
   preferidas:
   - Trocar um atributo entre dois conceitos do proprio material (dar a um
     modelo/termo uma caracteristica que pertence a outro).
   - Inverter a relacao causal ou a fronteira entre dois conceitos
     ("A causa B" quando na verdade e o contrario, ou "X inclui Y" quando na
     verdade sao categorias distintas).
   - Generalizar indevidamente um caso particular do texto para uma regra
     geral.
   Evite falsos obvios do tipo "o conceito X nao existe".
4. **Sem pistas artificiais**: evite palavras como "sempre", "nunca",
   "todos", "nenhum" quando elas denunciarem a resposta em vez de refletirem
   o que o material realmente afirma.
5. **Restricao de Bloom (obrigatoria)**: toda afirmacao deve ser verificavel
   apenas lendo o material — reconhecer se o que foi dito bate com o texto.
   Nunca exija aplicar o conceito a um caso novo, comparar cenarios
   hipoteticos, analisar consequencias nao explicitadas ou julgar/avaliar
   algo. Se uma afirmacao candidata exigir esse tipo de raciocinio,
   reescreva-a para testar so o reconhecimento do conceito, ou descarte-a.
6. **Nao alucinar**: toda afirmacao, verdadeira ou falsa, deve derivar de
   algo presente no documento. Uma afirmacao falsa e um equivoco *sobre um
   conceito que esta no material* — nunca invente um conceito que nao
   aparece no texto.
7. **Portugues (BR) com acentuacao correta obrigatoria** — acentos, til,
   cedilha sempre corretos ("servico" -> "serviço", "friccao" ->
   "fricção"). Excecao: se o documento fonte e o publico-alvo forem de
   outro idioma, redija as questoes nesse mesmo idioma.

## Formato de saida

Salve um arquivo `.md` ao lado do documento fonte, com o nome
`questoes-<nome-do-fonte>.md` (mesmo diretorio do arquivo original, mesmo
nome-base, sem extensao original, prefixado por `questoes-`). Exemplo: para
`/caminho/capitulo3.md`, salve em `/caminho/questoes-capitulo3.md`.

Estrutura do arquivo (ver `examples/exemplo-saida.md` para um exemplo
ilustrativo completo):

```markdown
# Questoes Conceituais (V/F) — <titulo do documento>

> Fonte: `<caminho>`
> Nivel Bloom: 1 (lembranca) · Tipo: Verdadeiro/Falso · Total: <N> (<n_V> V / <n_F> F)
> Gerado em: <AAAA-MM-DD>

## Questoes

1. ( ) <afirmacao 1>
2. ( ) <afirmacao 2>
...
N. ( ) <afirmacao N>

---

## Gabarito

| # | Resposta | Conceito | Justificativa |
|---|----------|----------|----------------|
| 1 | V | <conceito> | <por que e verdadeira, 1 linha> |
| 2 | F | <conceito> | <qual e o correto, 1 linha> |
...
```

Cada linha do gabarito com resposta F deve citar, na justificativa, qual e
o correto segundo o material — nunca deixe uma falsa sem a correcao.

## Checklist (Definition of Done)

Antes de reportar como concluido, verifique:

- [ ] Numero de questoes geradas == quantidade solicitada (ou, se o material
      nao sustentar isso, o relatorio explica por que gerou menos).
- [ ] Nenhuma questao exige aplicacao, analise, comparacao de cenarios
      hipoteticos ou avaliacao — so reconhecimento (Bloom nivel 1).
- [ ] Nenhuma questao testa data, nome proprio ou estatistica como fim em
      si (so quando o proprio conceito ensinado e essa associacao).
- [ ] Distribuicao V/F proxima de 50/50 e em ordem embaralhada.
- [ ] Toda afirmacao falsa tem, no gabarito, a informacao correta.
- [ ] Toda afirmacao (V ou F) deriva de conteudo realmente presente no
      documento — nada alucinado.
- [ ] Arquivo salvo em `<dir-do-fonte>/questoes-<nome-do-fonte>.md` e o
      caminho foi reportado ao usuario.

## Gotchas

- **`.pptx` nao e texto puro.** O Read pode falhar silenciosamente ou trazer
  so fragmentos. Nao tente adivinhar o conteudo que faltou — avise o
  usuario e sugira converter o arquivo para `.md` ou `.pdf` antes de rodar a
  skill novamente. O mesmo vale para `.docx` com conteudo nao-textual
  (imagens escaneadas, por exemplo).
- **Nao alucinar conceitos.** Toda questao, verdadeira ou falsa, tem que
  derivar de algo que esta escrito no documento. Uma falsa e sempre um
  equivoco sobre um conceito real do material, nunca um conceito inventado.
- **Quantidade pedida maior que conceitos disponiveis**: gere o maximo que
  o material sustentar com qualidade e diga isso claramente no relatorio —
  nao complete a diferenca com trivia so para bater o numero solicitado.
- **Dominio ambiguo ou documento com varios temas misturados**: priorize os
  conceitos mais recorrentes e estruturais do texto, e declare no relatorio
  final qual tema foi assumido como ancora da heuristica.
- **Skills antigas nao aparecem como slash command.** O formato antigo
  (`skill.json` + `instructions.md`) nao registra `/questoes-conceituais`
  no Claude Code atual — e preciso um `SKILL.md` com frontmatter (como
  este). Alem disso, **e preciso reiniciar a sessao do Claude Code** depois
  de criar ou alterar esta skill para o comando `/questoes-conceituais`
  aparecer na lista de skills disponiveis.
