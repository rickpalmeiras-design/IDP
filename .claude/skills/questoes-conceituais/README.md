# questoes-conceituais

Skill do Claude Code que gera **questoes conceituais Verdadeiro/Falso** a
partir de qualquer documento de estudo — uma aula, um capitulo de livro, um
artigo, um manual, uma documentacao tecnica. Funciona para qualquer tema ou
disciplina: o assunto e o publico-alvo sao inferidos do proprio documento
(ou informados via `--dominio`), e essa informacao ancora a heuristica que
decide o que vale a pena perguntar.

## O que faz

As questoes treinam exclusivamente o **nivel 1 da taxonomia de Bloom**
(lembranca/reconhecimento): o aluno so precisa reconhecer se uma afirmacao
sobre um conceito ensinado no material e verdadeira ou falsa. Nada de
aplicar o conceito a um caso novo, analisar, comparar cenarios hipoteticos
ou avaliar — isso fica fora do escopo desta skill.

O nucleo da skill e uma heuristica de relevancia: para cada conceito
candidato, a skill se pergunta "alguem que estuda este tema precisa lembrar
disso para raciocinar ou agir bem no dominio?". Se sim, vira questao; se e
trivia periferica (data solta, nome proprio decorativo, estatistica pontual,
detalhe visual do documento), e descartado.

## Como usar

Invoque via slash command ou em linguagem natural:

```
/questoes-conceituais capitulo3.md 20
/questoes-conceituais capitulo3.md 15 --foco "ciclo de Krebs" --dominio "bioquimica / graduacao em biomedicina"
```

Ou em texto livre:

```
gere 20 questoes verdadeiro/falso a partir de capitulo3.md
crie um quiz conceitual sobre esse material, focando na parte de riscos
```

### Argumentos

| Argumento | Obrigatorio | Descricao |
|---|---|---|
| `<arquivo>` | sim | Caminho do documento de estudo (`.md`, `.txt`, `.pdf`). |
| `<quantidade>` | nao (default 10) | Numero de questoes a gerar. |
| `--foco "topicos"` | nao | Conceitos/secoes a priorizar nesta rodada. |
| `--dominio "tema/publico"` | nao | Tema e publico-alvo (ex.: "direito tributario / concurseiros"). Se omitido, e inferido do conteudo do documento. |

## Output

Um arquivo `.md` salvo ao lado do documento fonte, chamado
`questoes-<nome-do-fonte>.md`, contendo:

- Uma lista numerada de afirmacoes V/F, em ordem embaralhada (~50% V, ~50% F).
- Um gabarito em tabela, com o conceito testado e uma justificativa de uma
  linha por questao — nas falsas, a justificativa traz a informacao correta.

Veja `examples/exemplo-saida.md` para um exemplo ilustrativo completo do
formato.

## Principio de design

A dificuldade da skill nao esta em gerar frases com "verdadeiro" ou "falso"
— esta em **decidir o que merece virar questao**. Qualquer documento tem
muito mais frases do que conceitos que valem a pena testar. A skill filtra
agressivamente trivia (datas, nomes decorativos, estatisticas soltas,
anedotas, formatacao) e mantem o foco na espinha conceitual do material:
definicoes, principios, classificacoes, relacoes causais e o papel de cada
componente no dominio. Essa espinha conceitual e sempre extraida do
documento em maos — a skill nao tem uma lista fixa de "temas importantes",
ela se adapta ao assunto e ao publico declarados ou inferidos a cada
execucao.

As falsas tambem seguem um principio: um equivoco plausivel (trocar um
atributo entre dois conceitos do proprio material, inverter uma relacao
causal, generalizar demais um caso particular) ensina mais do que uma
negacao absurda, porque forca o aluno a realmente saber o conceito certo
para nao cair na pegadinha.

## Limitacoes conhecidas

- `.pptx` e `.docx` nao-textuais podem falhar na leitura — a skill avisa e
  sugere converter para `.md`/`.pdf` em vez de inventar conteudo.
- Se o documento nao sustentar a quantidade de questoes pedida com
  qualidade, a skill gera menos e avisa, em vez de completar com trivia.
- Apos criar ou alterar esta skill, **reinicie a sessao do Claude Code**
  para que o comando `/questoes-conceituais` apareca na lista de skills.
