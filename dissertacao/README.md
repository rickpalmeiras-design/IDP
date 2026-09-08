# Template LaTeX IDP — monografia / TCC / dissertação / tese

Esta pasta reproduz a formatação oficial do IDP (Instituto Brasileiro de
Ensino, Desenvolvimento e Pesquisa) e implementa as normas ABNT para
trabalhos acadêmicos (monografias, TCCs, dissertações e teses), a partir do
template [**TemplateLatexIDP**](https://github.com/alexlopespereira/TemplateLatexIDP)
de Alex Lopes Pereira.

Leia **[TUTORIAL.md](TUTORIAL.md)** para o passo a passo completo de como
escrever o trabalho usando este layout — inclusive como usar o Claude Code
como copiloto de redação. O arquivo **[CLAUDE.md](CLAUDE.md)** contém as
instruções que o assistente segue automaticamente sempre que você pedir ajuda
dentro desta pasta.

## Estrutura

```
.
├── idp.cls                 ← a classe LaTeX (a formatação ABNT/IDP — não altere)
├── main.tex                ← documento principal: só inclui os outros arquivos
├── latexmkrc                ← configuração de compilação
├── referencias.bib          ← sua bibliografia (formato BibTeX)
├── config/
│   └── dados.tex            ← autor, título, orientador, banca, palavras-chave…
├── pretextual/
│   ├── dedicatoria.tex   agradecimentos.tex   epigrafe.tex
│   └── resumo.tex        abstract.tex         siglas.tex
├── capitulos/
│   ├── 01-introducao.tex
│   ├── 02-referencial-teorico.tex
│   ├── 03-procedimentos-metodologicos.tex
│   ├── 04-analise-e-discussao.tex
│   └── 05-consideracoes-finais.tex
├── postextual/
│   ├── apendices.tex
│   └── anexos.tex
├── figuras/                  ← suas imagens (adicione o logo idp-logo.png aqui)
├── CLAUDE.md                 ← instruções para o Claude Code
├── TUTORIAL.md                ← guia completo passo a passo
└── README.md                  ← este arquivo
```

> **Nota:** o repositório original também inclui `figuras/idp-logo.png` e o PDF
> oficial de referência `templateMonografia_ou_TCC.pdf` (para conferência
> visual). Como são arquivos binários, baixe-os diretamente do repositório
> original se precisar deles:
> <https://github.com/alexlopespereira/TemplateLatexIDP/tree/main/figuras> e
> <https://github.com/alexlopespereira/TemplateLatexIDP/raw/main/templateMonografia_ou_TCC.pdf>

## Como compilar

Requer uma distribuição LaTeX (MiKTeX, TeX Live ou MacTeX) com `biber`, ou use
o [Overleaf](https://overleaf.com) enviando um `.zip` desta pasta.

```bash
latexmk -pdf main.tex      # gera main.pdf
latexmk -c                 # limpa arquivos auxiliares
```

## Antes de escrever

1. Em `main.tex`, escolha a natureza do trabalho na opção da classe:
   `\documentclass[bacharelado]{idp}` — troque `bacharelado` por
   `especializacao`, `mestrado` ou `doutorado` conforme o caso. O texto
   "Monografia/Dissertação/Tese apresentada ao..." é gerado automaticamente a
   partir dessa opção.
2. Preencha `config/dados.tex` com os dados reais do seu trabalho — veja a
   seção 4 do [TUTORIAL.md](TUTORIAL.md#4-preencha-seus-dados).
3. Apague de `pretextual/` e `postextual/` os elementos opcionais que não se
   aplicam ao seu trabalho (dedicatória, epígrafe, apêndices, anexos…) e
   remova a linha correspondente de `main.tex`.

## Fonte

Template original: <https://github.com/alexlopespereira/TemplateLatexIDP>
(licença LPPL 1.3c para os arquivos da classe; conteúdo de exemplo em domínio
público).
