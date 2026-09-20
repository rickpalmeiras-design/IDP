# Artigos de referência

Cópias locais dos textos citados na dissertação, para leitura e conferência de citações.

`referencias_citadas.xlsx` é o índice completo: autores, ano, título, veículo, DOI, link, em quais
capítulos a obra é citada, quantas vezes, o papel que cumpre no trabalho, qual versão está guardada
aqui e a situação de acesso. A planilha é gerada por `scripts/bibliografia.py`, que lê
`dissertacao/referencias.bib` e as chaves de citação nos arquivos `.tex`:

```
uv run python scripts/bibliografia.py
```

Sempre que uma referência nova for citada, basta rodar o script de novo.

## O que está na pasta

15 dos 17 itens da planilha têm PDF aqui. Cada arquivo tem o nome da chave usada no `.bib`.

| Arquivo | Obra | Versão guardada |
| --- | --- | --- |
| `acemoglu2019.pdf` | Acemoglu e Restrepo, *Automation and new tasks* | NBER WP 25684; publicado no JEP |
| `acemoglu2020.pdf` | Acemoglu e Restrepo, *Robots and jobs* | NBER WP 23285; publicado no JPE |
| `brynjolfsson2025.pdf` | Brynjolfsson, Li e Raymond, *Generative AI at work* | NBER WP 31161; publicado no QJE |
| `callaway2024.pdf` | Callaway, Goodman-Bacon e Sant'Anna, *DiD with a continuous treatment* | Pré-print arXiv, dez. 2025 |
| `dingel2020.pdf` | Dingel e Neiman, *How many jobs can be done at home?* | NBER WP 26948 |
| `eloundou2024.pdf` | Eloundou et al., *GPTs are GPTs* | Pré-print arXiv de 2023; publicado na Science |
| `higano2023.pdf` | Higano et al., mobilidade ocupacional e diferenças salariais | Publicada (RBE) |
| `humlum2025.pdf` | Humlum e Vestergaard, *Still waters, rapid currents* | NBER WP 33777 |
| `ibge2022tratamento.pdf` | IBGE, *O tratamento das informações da PNAD Contínua* | Publicada |
| `massenkoff_mccrory_2026_labor_market_impacts_ai.pdf` | Massenkoff e McCrory, *Labor market impacts of AI* | Publicada (Anthropic) |
| `meghir2015.pdf` | Meghir, Narita e Robin, *Wages and informality* | NBER WP 18347; publicado na AER |
| `osorio2022.pdf` | Osório, painéis da PNAD Contínua | Publicada (Ipea) |
| `rambachan2023.pdf` | Rambachan e Roth, *A more credible approach to parallel trends* | Publicada (ReStud) |
| `ulyssea2020.pdf` | Ulyssea, *Informality* | Versão aceita (repositório da UCL) |
| `wroblevski2024.pdf` | Wroblevski et al., transição no mercado informal | Publicada (anais da ANPEC) |

Faltam dois itens, por motivo declarado na planilha:

- **`felten2021`**, a fonte do AIOE. O artigo está no *Strategic Management Journal*, restrito, e o
  acesso público disponível não entrega o PDF. Baixar pelo acesso institucional do IDP.
- **`basedosdados_pnadc`**, que é a base de microdados usada na estimação e não tem PDF.

Onde o periódico é restrito, o arquivo guardado é a versão de trabalho, que pode divergir da
publicada em números e redação. As citações do texto seguem a versão publicada, que é a que está no
`.bib`, então confira números pela versão publicada antes de citar página.

## Massenkoff e McCrory (2026)

Relatório técnico da Anthropic, 17 páginas, publicado em 5 de março de 2026.
Link: https://www.anthropic.com/research/labor-market-impacts
Dados de cobertura por tarefa e por ocupação: https://huggingface.co/datasets/Anthropic/EconomicIndex

BibTeX fornecido pelos autores:

```bibtex
@online{massenkoffmccrory2026labor,
  author = {Maxim Massenkoff and Peter McCrory},
  title  = {Labor market impacts of AI: A new measure and early evidence},
  date   = {2026-03-05},
  year   = {2026},
  url    = {https://www.anthropic.com/research/labor-market-impacts},
}
```

### O que o texto faz

- Propõe a **exposição observada**: parte da capacidade teórica de Eloundou et al. (2023), mantém
  apenas as tarefas que aparecem com frequência suficiente no uso profissional do Claude
  (Anthropic Economic Index, uso de agosto e novembro de 2025), dá peso cheio ao uso automatizado
  e meio peso ao uso de apoio, e agrega para a ocupação pela fração de tempo de cada tarefa.
- Liga a medida às ocupações da Current Population Survey (CPS) dos Estados Unidos pelo
  cruzamento O*NET-SOC para occ1990 de Eckhardt e Goldschlag (2025).
- Estima diferenças em diferenças comparando o quartil mais exposto com os 30% sem exposição,
  antes e depois do lançamento do ChatGPT, tendo o **desemprego** como desfecho principal.

### Resultados

- A cobertura observada é uma fração da teórica: em Computação e Matemática, 94% das tarefas são
  teoricamente viáveis, mas só 33% aparecem no uso real.
- Ocupações mais expostas: programador (75%), atendente de suporte e digitador (67%). Sem
  exposição: 30% dos trabalhadores (cozinheiro, barman, salva-vidas).
- Cada 10 pontos percentuais a mais de cobertura correspondem a 0,6 ponto percentual a menos na
  projeção de crescimento do emprego do BLS para 2024-2034. A medida de Eloundou et al. sozinha
  não tem essa correlação.
- Trabalhadores expostos ganham 47% mais, têm mais escolaridade (17,4% com pós-graduação, contra
  4,5% no grupo sem exposição) e são mais frequentemente mulheres.
- **Nenhum aumento sistemático do desemprego** no grupo exposto desde o fim de 2022. Pelos
  intervalos de confiança, o desenho detectaria diferenças da ordem de 1 ponto percentual.
- Entre jovens de 22 a 25 anos, a taxa de entrada em ocupações expostas cai cerca de 14% depois do
  ChatGPT, resultado no limite da significância e ausente acima dessa idade.

### Por que interessa a esta dissertação

- Mesmo desenho geral: índice de exposição por ocupação, marco no lançamento do ChatGPT,
  diferenças em diferenças em pesquisa domiciliar rotativa (CPS lá, PNAD Contínua aqui).
- Mesma limitação de identificação: a exposição é atributo da ocupação, não adoção observada, e o
  choque é único e nacional. Os autores são explícitos ao dizer que um aumento paralelo do
  desemprego em todos os grupos não seria atribuído à inteligência artificial.
- Dá um contraponto direto ao AIOE: exposição potencial contra exposição observada.
- Os dados de cobertura por ocupação são públicos e estão em SOC, a mesma âncora do cruzamento
  COD-ISCO-SOC já construído aqui.

### Ressalvas de uso

- É relatório de empresa, sem revisão por pares.
- A exposição observada vem só do tráfego do Claude, o que levanta seleção de plataforma.
- A capacidade teórica de base é de Eloundou et al. (2023) e reflete modelos do início de 2023.
