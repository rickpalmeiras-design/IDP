%%=============================================================================
%% idp.cls -- Classe LaTeX para trabalhos academicos do
%%            Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa (IDP)
%%
%% Reproduz o modelo "Template final_Monografia_Dissertacao_Tese_2026 uni IDP"
%% (Universidade IDP, 2026) publicado pela Biblioteca Ministro Moreira Alves
%% e atende as normas ABNT:
%%   NBR 14724 (trabalhos academicos)   NBR 6027 (sumario)
%%   NBR 6023  (referencias)            NBR 6028 (resumo)
%%   NBR 10520 (citacoes)               NBR 6024 (numeracao progressiva)
%%
%%
%% Licenca: LPPL 1.3c
%%=============================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{idp}[2026/11/03 v2.0 Trabalhos academicos da Universidade IDP (ABNT)]

%%-----------------------------------------------------------------------------
%% 1. OPCOES DA CLASSE
%%-----------------------------------------------------------------------------
\RequirePackage{iftex}

\newif\ifidp@novapagina   \idp@novapaginatrue   % secao primaria em nova pagina
\newif\ifidp@links        \idp@linksfalse       % colorir hiperlinks
\newif\ifidp@rascunho     \idp@rascunhofalse    % marca d'agua de rascunho
\newif\ifidp@autorrepetido \idp@autorrepetidotrue % autor repetido por extenso (modelo 2026)
\newif\ifidp@entrega      \idp@entregafalse       % aborta se faltar campo

% --- nivel do trabalho (define a natureza padrao e o grau) -------------------
\def\idp@nivel{bacharelado}
\DeclareOption{bacharelado}{\def\idp@nivel{bacharelado}}
\DeclareOption{especializacao}{\def\idp@nivel{especializacao}}
\DeclareOption{mestrado}{\def\idp@nivel{mestrado}}
\DeclareOption{doutorado}{\def\idp@nivel{doutorado}}

% --- comportamento -----------------------------------------------------------
\DeclareOption{secaonovapagina}{\idp@novapaginatrue}
\DeclareOption{secaocontinua}{\idp@novapaginafalse}
\DeclareOption{links}{\idp@linkstrue}
\DeclareOption{semlinks}{\idp@linksfalse}
\DeclareOption{rascunho}{\idp@rascunhotrue}
\DeclareOption{refautorrepetido}{\idp@autorrepetidotrue}
\DeclareOption{refautortraco}{\idp@autorrepetidofalse}   % volta ao travessao antigo
\DeclareOption{entrega}{\idp@entregatrue}

% --- repasse para a classe base ---------------------------------------------
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ExecuteOptions{bacharelado,secaonovapagina,semlinks}
\ProcessOptions\relax

\LoadClass[12pt,a4paper,oneside]{article}

%%-----------------------------------------------------------------------------
%% 2. CODIFICACAO, IDIOMA E FONTE (Times New Roman)
%%-----------------------------------------------------------------------------
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage{newtxtext}   % clone metrico de Times New Roman
  \RequirePackage{newtxmath}
\else
  \RequirePackage{fontspec}
  % TeX Gyre Termes e metricamente identico ao Times New Roman e sempre existe.
  % Se a fonte real estiver instalada no sistema, ela e preferida.
  \IfFontExistsTF{Times New Roman}
    {\setmainfont{Times New Roman}}
    {\setmainfont{TeX Gyre Termes}}
\fi

\RequirePackage[main=brazilian,english]{babel}
\RequirePackage{indentfirst}   % ABNT: o primeiro paragrafo tambem e indentado

%%-----------------------------------------------------------------------------
%% 3. GEOMETRIA DA PAGINA
%%    Medidas extraidas do PDF de referencia:
%%      margem esquerda 30 mm | direita 20 mm | superior 30 mm | inferior 20 mm
%%      numero de pagina com o topo a 20 mm da borda superior, alinhado a direita
%%-----------------------------------------------------------------------------
\RequirePackage[a4paper,
                left=30mm, right=20mm, top=30mm, bottom=20mm,
                headheight=14.5pt, headsep=4.89mm,
                footskip=10mm]{geometry}

%%-----------------------------------------------------------------------------
%% 4. ESPACAMENTO ENTRE LINHAS
%%    O template foi produzido no Word com Times New Roman 12 pt.
%%    Espacamento "simples" do Word  = 13,8 pt  -> stretch 0,9517
%%    Espacamento "1,5"     do Word  = 20,7 pt  -> stretch 1,4276
%%    (o LaTeX usa 14,5 pt como \baselineskip nativo em 12 pt)
%%-----------------------------------------------------------------------------
\RequirePackage{setspace}
\def\idp@stretchsimples{0.9517}
\def\idp@stretchumemeio{1.4276}

\newcommand{\espacosimples}{\setstretch{\idp@stretchsimples}}
\newcommand{\espacoumemeio}{\setstretch{\idp@stretchumemeio}}

% ATENCAO: \setstretch executa \@currsize, que reseleciona o TAMANHO corrente.
% Por isso todo bloco em corpo menor precisa mudar o espacamento ANTES do
% tamanho. \idpcorpo{tamanho}{entrelinha} faz isso na ordem certa.
\newcommand{\idpcorpo}[2]{\setstretch{1}\fontsize{#1}{#2}\selectfont}
\newcommand{\idpcorpodez}{\idpcorpo{10}{11.5}}   % legendas, fontes, notas, abstract
\newcommand{\idpcorpoonze}{\idpcorpo{11}{12.65}} % citacoes longas, numero da pagina

% Altura de uma linha com espacamento 1,5 -- usada nos espacamentos verticais
\newlength{\idplinha}      \setlength{\idplinha}{20.7pt}
\newlength{\idplinhasimp}  \setlength{\idplinhasimp}{13.8pt}

\espacoumemeio

% Recuo de primeira linha: 1,25 cm (ABNT / template)
\setlength{\parindent}{1.25cm}
\setlength{\parskip}{0pt}

% Em portugues nao se usa espaco extra depois do ponto final
\frenchspacing

% Justificado, sem "overfull" agressivo
\RequirePackage{microtype}
\tolerance=1500
\emergencystretch=1em
\hyphenpenalty=200

%%-----------------------------------------------------------------------------
%% 5. TABULACAO DOS TITULOS (emula os tabuladores padrao do Word: 0,635 cm)
%%    "1"     -> titulo comeca a 0,635 cm
%%    "1.1"   -> titulo comeca a 0,635 cm
%%    "1.1.1" -> titulo comeca a 1,270 cm
%%-----------------------------------------------------------------------------
\newlength{\idp@tabstop} \setlength{\idp@tabstop}{6.35mm}
\newlength{\idp@lw}
\newlength{\idp@nw}
\newcommand{\idptabbox}[1]{%
  \settowidth{\idp@nw}{#1}%
  \addtolength{\idp@nw}{0.6mm}% exige um espaco minimo antes do proximo tabulador
  \setlength{\idp@lw}{\idp@tabstop}%
  \@whiledim\idp@lw<\idp@nw\do{\addtolength{\idp@lw}{\idp@tabstop}}%
  \makebox[\idp@lw][l]{#1}%
}
% Modelo 2026: o titulo da secao vem logo depois do numero, a cerca de 4 mm
% ("1 INTRODUCAO" com o titulo a 7,7 mm da margem; "1.1 Objetivo" a 10,1 mm).
\newlength{\idp@distnum} \setlength{\idp@distnum}{4mm}
\newcommand{\idpnumtitulo}[1]{#1\hspace{\idp@distnum}}

%%-----------------------------------------------------------------------------
%% 6. TITULOS DE SECAO (NBR 6024 / NBR 14724)
%%    1  SECAO PRIMARIA .... caixa alta + negrito
%%    1.1  Secao secundaria . negrito
%%    1.1.1 Secao terciaria . sem destaque
%%    1.1.1.1 quaternaria ... italico
%%    1.1.1.1.1 quinaria .... negrito + italico
%%    Separados do texto por uma linha em branco de 1,5 (antes e depois).
%%-----------------------------------------------------------------------------
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{4}

\titleformat{\section}[block]
  {\normalfont\normalsize\bfseries\raggedright}
  {\idpnumtitulo{\thesection}}{0pt}{\MakeUppercase}
\titleformat{\subsection}[block]
  {\normalfont\normalsize\bfseries\raggedright}
  {\idpnumtitulo{\thesubsection}}{0pt}{}
\titleformat{\subsubsection}[block]
  {\normalfont\normalsize\raggedright}
  {\idpnumtitulo{\thesubsubsection}}{0pt}{}
\titleformat{\paragraph}[block]
  {\normalfont\normalsize\itshape\raggedright}
  {\idpnumtitulo{\theparagraph}}{0pt}{}
\titleformat{\subparagraph}[block]
  {\normalfont\normalsize\bfseries\itshape\raggedright}
  {\idpnumtitulo{\thesubparagraph}}{0pt}{}

\titlespacing{\section}      {0pt}{\idplinha}{\idplinha}
\titlespacing{\subsection}   {0pt}{\idplinha}{\idplinha}
\titlespacing{\subsubsection}{0pt}{\idplinha}{\idplinha}
\titlespacing{\paragraph}    {0pt}{\idplinha}{\idplinha}
\titlespacing{\subparagraph} {0pt}{\idplinha}{\idplinha}

% NBR 14724, 5.2.2: cada secao primaria comeca em folha propria.
\ifidp@novapagina
  \newcommand{\sectionbreak}{\clearpage}
\fi

% As secoes primarias aparecem em CAIXA ALTA tambem no sumario. Para isso o
% \section grava a entrada do sumario ja envolvida em \MakeUppercase (aplicar
% \MakeUppercase na leitura do .toc quebraria as ancoras do hyperref).
%
% O \texorpdfstring e OBRIGATORIO aqui, nao e refinamento: a mesma entrada vai
% para \addcontentsline, e o hyperref a converte em PDF string para montar o
% bookmark. Dentro do \pdfstringdef ele mapeia \MakeUppercase para
% \MakeUppercaseUnsupportedInPdfStrings, macro que so existe quando o kernel
% oferece \text_uppercase:n (LaTeX recente). Em kernel antigo esse macro NAO e
% definido e a compilacao morre com "undefined control sequence" ao gerar o
% bookmark. Com \texorpdfstring o \MakeUppercase nunca chega ao PDF string:
% o sumario sai em caixa alta e o bookmark sai em caixa normal.
\let\idp@origsection\section
\newcommand{\idp@sectionstar}[1]{\idp@origsection*{#1}}
\def\idp@sectionplain[#1]#2{%
  \idp@origsection[\texorpdfstring{\MakeUppercase{#1}}{#1}]{#2}}
\renewcommand{\section}{\@ifstar{\idp@sectionstar}{\@dblarg\idp@sectionplain}}

% Apelidos em portugues para quem preferir "capitulo"
\newcommand{\capitulo}{\section}
\newcommand{\subcapitulo}{\subsection}

%%-----------------------------------------------------------------------------
%% 7. CABECALHO: numero da pagina no canto superior direito
%%-----------------------------------------------------------------------------
\RequirePackage{fancyhdr}
\fancypagestyle{idp}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
  \fancyhead[R]{\normalfont\fontsize{11}{12.65}\selectfont\thepage}% modelo 2026: 11 pt
}
\fancypagestyle{idpsemnumero}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}
\pagestyle{idpsemnumero}

%%-----------------------------------------------------------------------------
%% 8. NOTAS DE RODAPE -- fonte 10, espacamento simples, alinhadas a margem
%%-----------------------------------------------------------------------------
\RequirePackage[bottom,flushmargin]{footmisc}
\renewcommand{\footnotesize}{\fontsize{10}{11.5}\selectfont}
\renewcommand{\footnoterule}{%
  \vspace{2pt}\hrule width 0.4\columnwidth height 0.4pt\vspace{4pt}}
% Chamada na margem, texto da primeira linha recuado (padrao do template)
\renewcommand{\@makefntext}[1]{%
  \idpcorpodez\noindent\@thefnmark\hspace{10.9mm}#1}

%%-----------------------------------------------------------------------------
%% 9. CITACOES (NBR 10520)
%%    Citacao direta com mais de 3 linhas: recuo de 4 cm, fonte 11 (regra e
%%    exemplo do modelo 2026), espacamento simples, sem aspas, justificada.
%%-----------------------------------------------------------------------------
\newenvironment{citacao}{%
  \par\vspace{\idplinha}%
  \begin{list}{}{%
    \setlength{\leftmargin}{4cm}%
    \setlength{\rightmargin}{0pt}%
    \setlength{\listparindent}{0pt}%
    \setlength{\itemindent}{0pt}%
    \setlength{\labelwidth}{0pt}%
    \setlength{\labelsep}{0pt}%
    \setlength{\topsep}{0pt}%
    \setlength{\partopsep}{0pt}%
    \setlength{\parsep}{0pt}%
    \setlength{\itemsep}{0pt}}%
  \item[]\idpcorpoonze\noindent\ignorespaces
}{%
  \end{list}\par\vspace{\idplinha}%
}
% Versao em lingua estrangeira (NBR 10520: destacar em italico)
\newenvironment{citacaoestrangeira}{\begin{citacao}\itshape}{\end{citacao}}

%%-----------------------------------------------------------------------------
%% 10. FIGURAS, QUADROS, GRAFICOS E TABELAS
%%     Legenda ACIMA ("Figura 1 - Titulo", em italico, como no modelo 2026),
%%     fonte ABAIXO ("Fonte: ...", sem negrito). Ambas em fonte 10, o tamanho
%%     menor e uniforme da NBR 14724, centralizadas, espacamento simples.
%%-----------------------------------------------------------------------------
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{booktabs}
\RequirePackage{caption}
\DeclareCaptionLabelSeparator{idphifen}{ - }
\captionsetup{labelsep=idphifen,justification=centering,skip=4pt,position=top}
\DeclareCaptionFont{idpcap}{\idpcorpodez\itshape}
\captionsetup{font=idpcap,labelfont=idpcap,textfont=idpcap}

\floatstyle{plaintop}          % legenda SEMPRE acima do elemento
\newfloat{quadro}{htbp}{loq}
\floatname{quadro}{Quadro}
\newfloat{gfc}{htbp}{lgr}
\floatname{gfc}{Gr\'afico}
% "grafico" e o nome amigavel do ambiente
\let\grafico\gfc
\let\endgrafico\endgfc

\captionsetup[quadro]{font=idpcap,labelfont=idpcap,position=top}
\captionsetup[gfc]{font=idpcap,labelfont=idpcap,position=top}
\captionsetup[figure]{position=top}
\captionsetup[table]{position=top}

% Linha "Fonte: ..." abaixo do elemento ilustrativo
\newcommand{\fonte}[1]{%
  \par\vspace{2pt}%
  {\centering\idpcorpodez Fonte:~#1\par}%
}
\newcommand{\nota}[1]{%
  \par\vspace{2pt}%
  {\centering\idpcorpodez Nota:~#1\par}%
}

%%-----------------------------------------------------------------------------
%% 11. LISTAS (itemize/enumerate) -- alinhadas com o recuo de paragrafo
%%-----------------------------------------------------------------------------
\RequirePackage{enumitem}
% Marcador a 1,25 cm da margem e texto a 1,88 cm (como no template)
\setlist{nosep,topsep=0pt,partopsep=0pt,parsep=0pt,itemsep=0pt,
         labelindent=1.25cm,leftmargin=1.88cm,labelwidth=0.63cm,
         labelsep=0pt,align=left}
\setlist[itemize,1]{label=\textbullet}

%%-----------------------------------------------------------------------------
%% 12. DADOS DO TRABALHO
%%-----------------------------------------------------------------------------
% --- Marcador de campo nao preenchido ---------------------------------------
% Os campos obrigatorios NAO tem valor padrao plausivel: eles nascem com um
% marcador que salta aos olhos no PDF e que a classe sabe reconhecer para
% avisar (ou abortar, com a opcao `entrega') se algo ficou por preencher.
% E texto puro de proposito -- assim sobrevive a \MakeUppercase e aos
% metadados do PDF sem quebrar nada.
% Nao use ">>>" nem "<<<": na codificacao T1 eles viram as ligaduras » e «.
\newcommand{\idp@campovazio}[1]{[[ PREENCHER: #1 ]]}

\newcount\idp@pendentes
% Marcador publico para dados que ainda faltam, usavel em config/dados.tex
% (ex.: \membrobanca[\pendente{SIGLA da IES}]{...}). Conta no aviso final.
\newcount\idp@pendentestexto
\newcommand{\pendente}[1]{%
  \global\advance\idp@pendentestexto by 1\relax
  \idp@campovazio{#1}}
\AtEndDocument{%
  \ifnum\idp@pendentestexto>0\relax
    \ifidp@entrega
      \ClassError{idp}{\the\idp@pendentestexto\space dado(s) marcado(s) com
        \string\pendente\space ainda sem valor}{Procure por "[[ PREENCHER" no PDF.}%
    \else
      \ClassWarningNoLine{idp}{\the\idp@pendentestexto\space dado(s) ainda
        sem valor aparecem como "[[ PREENCHER: ... ]]" no PDF}%
    \fi
  \fi}
\newcommand{\idp@confere}[2]{%
  \def\idp@tmp{\idp@campovazio{#1}}%
  \ifx#2\idp@tmp
    \global\advance\idp@pendentes by 1\relax
    \ClassWarningNoLine{idp}{Campo nao preenchido em config/dados.tex: #1}%
  \fi
}

% Nome oficial atual. O antigo ("Instituto Brasileiro de Ensino, Desenvolvimento
% e Pesquisa -- IDP") nao e mais usado; \instituicao{...} ainda permite trocar.
\def\idp@instituicao{Universidade IDP}
\def\idp@instituicaocurta{Universidade~IDP}   % capa, rosto e aprovacao (2026)
\babelhyphenation[brazilian]{Universidade}      % o nome nao se quebra no fim da linha
\def\idp@titulo{\idp@campovazio{titulo}}
\def\idp@subtitulo{}
\def\idp@autor{\idp@campovazio{autor}}
\def\idp@autorficha{\idp@campovazio{autorficha}}
\def\idp@orientador{\idp@campovazio{orientador}}
\def\idp@coorientador{}
\def\idp@curso{\idp@campovazio{curso}}
\def\idp@programa{\idp@campovazio{programa}}
\def\idp@area{}              % area de concentracao (mestrado/doutorado)
\def\idp@linhapesquisa{}     % linha de pesquisa
\def\idp@titulotraduzido{}   % titulo em lingua estrangeira (para o abstract)
\def\idp@local{Bras\'ilia-DF}   % capa e folha de rosto: "Brasilia-DF"
\def\idp@cidade{Bras\'ilia}  % so a cidade, usada na folha de aprovacao
\def\idp@data{\the\year}
\def\idp@datadefesa{\idp@campovazio{datadefesa}}
\def\idp@palavraschave{\idp@campovazio{palavraschave}}
\def\idp@keywords{\idp@campovazio{keywords}}
\def\idp@cdd{\idp@campovazio{cdd}}
\def\idp@assuntos{}   % "1. Assunto. 2. Assunto." -- se vazio usa \palavraschave
\def\idp@cutter{}
\def\idp@paginas{\idp@campovazio{numeropaginas}}
\def\idp@tipotrabalho{}
\def\idp@preambulo{}
\def\idp@logo{figuras/idp-universidade-logo.png}   % use \semlogo para omitir
\def\idp@arquivoficha{}   % PDF da ficha oficial, quando a Biblioteca enviar

% Um campo informado em branco (ex.: \programa{}) continua pendente, em vez
% de sair vazio no PDF ("pos-graduacao em , como parte...").
\newcommand{\idp@defcampo}[3]{%  #1 macro | #2 nome do campo | #3 valor
  \def\idp@tmpa{#3}%
  \ifx\idp@tmpa\@empty\def#1{\idp@campovazio{#2}}\else\def#1{#3}\fi}

\newcommand{\instituicao}[1]{\def\idp@instituicao{#1}}
\newcommand{\instituicaocurta}[1]{\def\idp@instituicaocurta{#1}}
\newcommand{\titulo}[1]{\def\idp@titulo{#1}}
\newcommand{\subtitulo}[1]{\def\idp@subtitulo{#1}}
\renewcommand{\author}[1]{\def\idp@autor{#1}}
\newcommand{\autor}[1]{\def\idp@autor{#1}}
\newcommand{\autorficha}[1]{\def\idp@autorficha{#1}}
\newcommand{\orientador}[1]{\def\idp@orientador{#1}}
\newcommand{\coorientador}[1]{\def\idp@coorientador{#1}}
\newcommand{\curso}[1]{\idp@defcampo\idp@curso{curso}{#1}}
\newcommand{\programa}[1]{\idp@defcampo\idp@programa{programa}{#1}}
\newcommand{\area}[1]{\def\idp@area{#1}}
\newcommand{\linhapesquisa}[1]{\def\idp@linhapesquisa{#1}}
\newcommand{\titulotraduzido}[1]{\def\idp@titulotraduzido{#1}}
\newcommand{\local}[1]{\def\idp@local{#1}}
\newcommand{\cidade}[1]{\def\idp@cidade{#1}}
\renewcommand{\date}[1]{\def\idp@data{#1}}
\newcommand{\data}[1]{\def\idp@data{#1}}
% \datadefesa recebe SO a data; a cidade vem de \cidade, para nao repetir o
% mesmo dado em dois campos. Use \datadefesacompleta para controlar a linha
% inteira (ex.: "Aprovada em 15 de dezembro de 2026.").
\newcommand{\datadefesa}[1]{%
  \def\idp@tmpa{#1}%
  \ifx\idp@tmpa\@empty\else\def\idp@datadefesa{\idp@cidade, #1.}\fi}
\newcommand{\datadefesacompleta}[1]{\def\idp@datadefesa{#1}}
\newcommand{\palavraschave}[1]{\def\idp@palavraschave{#1}}
\newcommand{\keywords}[1]{\def\idp@keywords{#1}}
\newcommand{\cdd}[1]{\def\idp@cdd{#1}}
\newcommand{\assuntos}[1]{\def\idp@assuntos{#1}}
\newcommand{\cutter}[1]{\def\idp@cutter{#1}}
\newcommand{\numeropaginas}[1]{\def\idp@paginas{#1}}
\newcommand{\tipotrabalho}[1]{\def\idp@tipotrabalho{#1}}
\newcommand{\preambulo}[1]{\def\idp@preambulo{#1}}
\newcommand{\logo}[1]{\def\idp@logo{#1}}
\newcommand{\arquivoficha}[1]{\def\idp@arquivoficha{#1}}
\newcommand{\semlogo}{\let\idp@logo\@empty}

% --- Acessores publicos ------------------------------------------------------
% Permitem reaproveitar os dados no corpo do texto sem redigita-los. Ex.:
%   "Ao meu orientador, \NomeOrientador, pela paciencia..."
% Se o nome mudar em config/dados.tex, muda em todo lugar de uma vez.
\newcommand{\TituloTrabalho}{\idp@titulo}
\newcommand{\SubtituloTrabalho}{\idp@subtitulo}
\newcommand{\TituloTraduzido}{\idp@titulotraduzido}
\newcommand{\NomeAutor}{\idp@autor}
\newcommand{\NomeOrientador}{\idp@orientador}
\newcommand{\NomeCoorientador}{\idp@coorientador}
\newcommand{\NomeCurso}{\idp@curso}
\newcommand{\NomePrograma}{\idp@programa}
\newcommand{\NomeInstituicao}{\idp@instituicao}
\newcommand{\AreaConcentracao}{\idp@area}
\newcommand{\LinhaPesquisa}{\idp@linhapesquisa}
\newcommand{\LocalTrabalho}{\idp@local}
\newcommand{\CidadeTrabalho}{\idp@cidade}
\newcommand{\AnoTrabalho}{\idp@data}

% --- Verificacao dos campos obrigatorios ------------------------------------
% Roda depois que config/dados.tex ja foi lido. Sem a opcao `entrega' apenas
% avisa; com ela, aborta a compilacao -- assim e impossivel gerar a versao
% final com um ">>> PREENCHER <<<" perdido no meio do documento.
\AtBeginDocument{%
  \idp@confere{titulo}{\idp@titulo}%
  \idp@confere{autor}{\idp@autor}%
  \idp@confere{autorficha}{\idp@autorficha}%
  \idp@confere{orientador}{\idp@orientador}%
  \idp@confere{datadefesa}{\idp@datadefesa}%
  \idp@confere{palavraschave}{\idp@palavraschave}%
  \idp@confere{keywords}{\idp@keywords}%
  % Modelo 2026: a ficha catalografica vem pronta da Biblioteca, por isso CDD
  % e numero de paginas deixaram de ser cobrados aqui.
  % curso e programa sao mutuamente exclusivos: cobra so o que o nivel usa.
  % Na pos-graduacao a folha de rosto tambem pede a area de concentracao.
  \ifx\idp@nivel\idp@n@mestrado
    \ifx\idp@area\@empty\def\idp@area{\idp@campovazio{area}}\fi
    \idp@confere{programa}{\idp@programa}%
    \idp@confere{area}{\idp@area}%
  \else\ifx\idp@nivel\idp@n@doutorado
    \ifx\idp@area\@empty\def\idp@area{\idp@campovazio{area}}\fi
    \idp@confere{programa}{\idp@programa}%
    \idp@confere{area}{\idp@area}%
  \else
    \idp@confere{curso}{\idp@curso}%
  \fi\fi
  \ifnum\idp@pendentes>0\relax
    \ifidp@entrega
      \ClassError{idp}{%
        \the\idp@pendentes\space campo(s) obrigatorio(s) nao preenchido(s) em
        config/dados.tex}{%
        Procure por "[[ PREENCHER" no PDF e pelas linhas "Campo nao
        preenchido" acima neste log.\MessageBreak
        Preencha config/dados.tex ou remova a opcao `entrega' da classe.}%
      \stop % aborta de fato: nao gera PDF de entrega incompleto
    \else
      \ClassWarningNoLine{idp}{%
        ATENCAO: \the\idp@pendentes\space campo(s) de config/dados.tex ainda
        nao preenchido(s).\MessageBreak
        Eles aparecem como "[[ PREENCHER: ... ]]" no PDF.\MessageBreak
        Use a opcao de classe `entrega' para transformar isto em erro}%
    \fi
  \fi
}

% Banca examinadora (modelo 2026), um comando por membro:
%   \membrobanca[Instituicao]{Nome}{Funcao}[ID Lattes ou ORCID]
% Sai como: traco | Nome | ID Lattes ou ORCID | "Funcao - Instituicao".
% A instituicao e opcional e vale "IDP" quando omitida; o examinador externo
% leva a sigla da IES dele. Sem o ID, sai "[[ PREENCHER: ID Lattes ou ORCID ]]".
\newcommand{\idp@banca}{}
\newcommand{\membrobanca}[3][IDP]{%
  \@ifnextchar[{\idp@membrobanca{#1}{#2}{#3}}{\idp@membrobanca{#1}{#2}{#3}[]}%
}
\def\idp@membrobanca#1#2#3[#4]{%
  \g@addto@macro\idp@banca{\idp@membro{#2}{#3}{#1}{#4}}%
}

% Titulo completo (Titulo: subtitulo) -- titulo em negrito, subtitulo nao
\newcommand{\idp@titulocompleto}{%
  \textbf{\idp@titulo}%
  \ifx\idp@subtitulo\@empty\else\textbf{:} \idp@subtitulo\fi
}

%%-----------------------------------------------------------------------------
%% 13. NATUREZA DO TRABALHO -- texto padrao por nivel
%%-----------------------------------------------------------------------------
% O modelo 2026 usa dois textos: um na folha de rosto (stricto sensu, area de
% concentracao) e outro, mais curto, na folha de aprovacao. O modelo ainda trazia
% o nome antigo ("Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa")
% na folha de aprovacao; os dois usam "Universidade IDP", o nome atual.
% \preambulo{...} substitui os dois.
\newcommand{\idp@preambulorosto}{%
  \ifx\idp@nivel\idp@n@bacharelado
    Trabalho de conclus\~ao de curso apresentado como requisito para
    obten\c{c}\~ao do t\'itulo de bacharel em \idp@curso\ pela
    \idp@instituicaocurta.%
  \else\ifx\idp@nivel\idp@n@especializacao
    Monografia apresentada como requisito para obten\c{c}\~ao do t\'itulo de
    especialista em \idp@curso\ pela \idp@instituicaocurta.%
  \else\ifx\idp@nivel\idp@n@mestrado
    Disserta\c{c}\~ao apresentada ao programa de p\'os-gradua\c{c}\~ao
    \textit{stricto sensu} em \idp@programa, \'area de concentra\c{c}\~ao
    \idp@area, como parte do requisito para a obten\c{c}\~ao do t\'itulo de
    Mestre em \idp@programa\ pela \idp@instituicaocurta.%
  \else
    Tese apresentada ao programa de p\'os-gradua\c{c}\~ao \textit{stricto
    sensu} em \idp@programa, \'area de concentra\c{c}\~ao \idp@area, como
    parte do requisito para a obten\c{c}\~ao do t\'itulo de Doutor em
    \idp@programa\ pela \idp@instituicaocurta.%
  \fi\fi\fi
}
\newcommand{\idp@preambuloaprovacao}{%
  \ifx\idp@nivel\idp@n@bacharelado
    Monografia apresentada como requisito para obten\c{c}\~ao do t\'itulo de
    bacharel em \idp@curso\ pela \idp@instituicaocurta.%
  \else\ifx\idp@nivel\idp@n@especializacao
    Monografia apresentada como requisito para obten\c{c}\~ao do t\'itulo de
    especialista em \idp@curso\ pela \idp@instituicaocurta.%
  \else\ifx\idp@nivel\idp@n@mestrado
    Disserta\c{c}\~ao apresentada ao programa de p\'os-gradua\c{c}\~ao em
    \idp@programa, como parte do requisito para a obten\c{c}\~ao do t\'itulo de
    Mestre em \idp@programa\ pela \idp@instituicaocurta.%
  \else
    Tese apresentada ao programa de p\'os-gradua\c{c}\~ao em \idp@programa,
    como parte do requisito para a obten\c{c}\~ao do t\'itulo de Doutor em
    \idp@programa\ pela \idp@instituicaocurta.%
  \fi\fi\fi
}
% Linha "Mestrado em ..." da capa. \habilitacao{...} substitui a linha inteira
% (ex.: "Mestrado Profissional em Administracao Publica").
\def\idp@habilitacao{}
\newcommand{\habilitacao}[1]{\def\idp@habilitacao{#1}}
\newcommand{\idp@cursocapa}{%
  \ifx\idp@habilitacao\@empty\idp@cursocapapadrao\else\idp@habilitacao\fi}
\newcommand{\idp@cursocapapadrao}{%
  \ifx\idp@nivel\idp@n@bacharelado Bacharelado em \idp@curso
  \else\ifx\idp@nivel\idp@n@especializacao Especializa\c{c}\~ao em \idp@curso
  \else\ifx\idp@nivel\idp@n@mestrado Mestrado em \idp@programa
  \else Doutorado em \idp@programa\fi\fi\fi}
\def\idp@n@bacharelado{bacharelado}
\def\idp@n@especializacao{especializacao}
\def\idp@n@mestrado{mestrado}
\def\idp@n@doutorado{doutorado}

% \tipotrabalho{} sobrepoe o tipo deduzido do nivel (util p/ "Trabalho de
% Conclusao de Curso", "Relatorio Tecnico" etc. na ficha catalografica)
\newcommand{\idp@tipopadrao}{%
  \ifx\idp@tipotrabalho\@empty
    \ifx\idp@nivel\idp@n@mestrado Disserta\c{c}\~ao%
    \else\ifx\idp@nivel\idp@n@doutorado Tese%
    \else Monografia\fi\fi
  \else\idp@tipotrabalho\fi
}

% Bloco da natureza do trabalho, justificado.
%   #1 recuo (7,5 cm na folha de rosto, 8 cm na de aprovacao)
%   #2 texto da natureza | #3 entrelinha do texto (o modelo usa 1,15 na folha
%   de rosto e simples na de aprovacao) | #4 mostra o coorientador?
\newcommand{\idp@blocopreambulo}[4]{%
  \hspace*{#1}%
  \begin{minipage}[t]{\dimexpr\textwidth-#1\relax}
    \setlength{\parindent}{0pt}\normalsize
    \exhyphenpenalty=10000 % nao quebra "pos-graduacao" no hifen, como no modelo
    {\setstretch{#3}%
     \ifx\idp@preambulo\@empty#2\else\idp@preambulo\fi\par}%
    \espacosimples
    \vspace{\idplinhasimp}%
    Orientador: \idp@orientador\par
    \if s#4\ifx\idp@coorientador\@empty\else Coorientador: \idp@coorientador\par\fi\fi
  \end{minipage}%
}

%%-----------------------------------------------------------------------------
%% 14. ELEMENTOS PRE-TEXTUAIS
%%-----------------------------------------------------------------------------
% #1 distancia ate o texto (uma linha de 1,5 por padrao) | #2 titulo
\newcommand{\idp@tituloelemento}[2][\idplinha]{%
  \clearpage
  \phantomsection
  {\centering\normalfont\normalsize\bfseries\MakeUppercase{#2}\par}%
  \vspace{#1}%
}

% As distancias abaixo reproduzem as linhas de base medidas no modelo 2026
% (em mm a partir da borda superior). Cada \vspace vale a distancia entre
% duas linhas de base menos a entrelinha da linha seguinte.
\newcommand{\idp@entrelinhadezesseis}{6.77mm}   % 19,2 pt, titulo em corpo 16

% --- CAPA (nao e contada na paginacao) ---------------------------------------
% logo 57,2 x 11,4 mm com o topo a 35,7 | "Universidade IDP" 54,1 |
% "Mestrado em ..." 59,7 | titulo (16 pt) 147,4 | autor 174,5 |
% orientador 179,3 | "Brasilia-DF" 242,6 | ano 248,2
\newcommand{\capa}{%
  \thispagestyle{empty}%
  \begingroup
  \centering\espacosimples\setlength{\parskip}{0pt}%
  \ifx\idp@logo\@empty
    \vspace*{12.5mm}%
  \else
    \vspace*{1.1mm}%  com o \topskip, poe o topo do logo a 35,7 mm
    \includegraphics[width=57.2mm]{\idp@logo}\par
  \fi
  \vspace{2.13mm}%
  \idp@instituicaocurta\par
  \vspace{0.73mm}%
  \idp@cursocapa\par
  \vspace{\dimexpr 87.7mm-\idp@entrelinhadezesseis\relax}%
  {\setstretch{1}\fontsize{16}{19.2}\selectfont\idp@titulocompleto\par}%
  \vspace{22.23mm}%
  \idp@autor\par
  Orientador: \idp@orientador\par
  \vfill
  \idp@local\par
  \vspace{0.73mm}%
  \idp@data\par
  \vspace{28.8mm}%
  \endgroup
  \clearpage
}

% --- FOLHA DE ROSTO (folha 1 da contagem) ------------------------------------
% autor (caixa alta, negrito) 34,0 | titulo (16 pt) 64,5 | natureza a 7,5 cm
% da margem, com a primeira linha a 98,9 | "Brasilia-DF" 267,6 | ano 273,2
\newcommand{\folhaderosto}{%
  \setcounter{page}{1}%
  \thispagestyle{idpsemnumero}%
  \begingroup
  \centering\espacosimples\setlength{\parskip}{0pt}%
  {\bfseries\MakeUppercase{\idp@autor}\par}%
  \vspace{\dimexpr 30.3mm-\idp@entrelinhadezesseis\relax}%
  {\setstretch{1}\fontsize{16}{19.2}\selectfont\idp@titulocompleto\par}%
  \vspace{29.0mm}%
  {\raggedright\noindent\idp@blocopreambulo{7.5cm}{\idp@preambulorosto}{1.097}{s}\par}%
  \vfill
  \idp@local\par
  \vspace{0.73mm}%
  \idp@data\par
  \vspace{3.8mm}%
  \endgroup
  \clearpage
}

% --- FICHA CATALOGRAFICA -----------------------------------------------------
% Modelo 2026: a folha fica reservada ("Espaco destinado a ficha
% catalografica.") ate a Biblioteca enviar a ficha oficial. Quando ela chegar,
% salve o PDF e informe \arquivoficha{figuras/ficha.pdf} em config/dados.tex:
% a ficha entra no pe da pagina, no lugar do aviso.
\newcommand{\fichacatalografica}{%
  \thispagestyle{idpsemnumero}%
  \ifx\idp@arquivoficha\@empty
    \null\vspace*{24.1mm}%
    {\centering\espacosimples Espa\c{c}o destinado \`a ficha catalogr\'afica.\par}%
  \else
    \null\vfill
    {\centering\includegraphics[width=\textwidth]{\idp@arquivoficha}\par}%
  \fi
  \clearpage
}

% --- FOLHA DE APROVACAO ------------------------------------------------------
% autor 43,7 | "Titulo: subtitulo" (12 pt) 58,3 | natureza a 8 cm, primeira
% linha a 72,9 | data 165,4 | "Banca Examinadora" 180,0 | cada membro: traco
% na largura do texto, nome, ID Lattes ou ORCID e "Funcao - Instituicao",
% um a cada 25 mm.
% #1 nome | #2 funcao | #3 instituicao | #4 ID Lattes ou ORCID
\newcommand{\idp@membro}[4]{%
  \vspace{6.3mm}%
  \noindent\rule{\linewidth}{0.4pt}\par
  \vspace{-0.77mm}%
  #1\par
  \if\relax\detokenize{#4}\relax\pendente{ID Lattes ou ORCID}\else #4\fi\par
  #2 - #3\par
}
\newcommand{\folhadeaprovacao}{%
  \thispagestyle{idpsemnumero}%
  \begingroup
  \centering\espacosimples\setlength{\parskip}{0pt}%
  \vspace*{4.6mm}%  com o \topskip, poe o nome a 43,7 mm
  {\bfseries\MakeUppercase{\idp@autor}\par}%
  \vspace{9.73mm}%
  \idp@titulocompleto\par
  \vspace{9.73mm}%
  {\raggedright\noindent\idp@blocopreambulo{8cm}{\idp@preambuloaprovacao}{\idp@stretchsimples}{n}\par}%
  % espaco flexivel: encolhe se o titulo ou a banca forem longos
  \vspace{48mm minus 40mm}%
  \idp@datadefesa\par
  \vspace{9.73mm}%
  {\bfseries Banca Examinadora\par}%
  \idp@banca
  \endgroup
  \clearpage
}

% --- DEDICATORIA / EPIGRAFE --------------------------------------------------
% Modelo 2026: dedicatoria em Times 12 normal (sem italico), no pe da pagina,
% alinhada a direita.
\newenvironment{dedicatoria}{%
  \clearpage\thispagestyle{idpsemnumero}%
  \null\vfill
  \noindent\hspace*{8cm}%
  \begin{minipage}{\dimexpr\textwidth-8cm\relax}
    \espacosimples\setlength{\parindent}{0pt}\ignorespaces
}{%
  \end{minipage}\par\vspace{20mm}\clearpage
}
\newenvironment{epigrafe}{%
  \clearpage\thispagestyle{idpsemnumero}%
  \null\vfill
  \noindent\hspace*{8cm}%
  \begin{minipage}{\dimexpr\textwidth-8cm\relax}
    \espacosimples\setlength{\parindent}{0pt}\itshape\raggedleft\ignorespaces
}{%
  \end{minipage}\par\vspace{20mm}\clearpage
}

% --- AGRADECIMENTOS ----------------------------------------------------------
% Modelo 2026: o texto comeca na linha logo abaixo do titulo.
\newenvironment{agradecimentos}{%
  \idp@tituloelemento[0pt]{Agradecimentos}\espacoumemeio
}{\clearpage}

% --- RESUMO / ABSTRACT (NBR 6028: paragrafo unico, sem recuo, simples) -------
\newenvironment{resumo}{%
  \idp@tituloelemento{Resumo}%
  \espacosimples\setlength{\parindent}{0pt}\noindent\ignorespaces
}{%
  \par\vspace{2\idplinhasimp}%
  \noindent\textbf{Palavras-chave:} \idp@palavraschave
  \clearpage
}
% Modelo 2026: abstract em Times 10, espacamento simples, justificado.
\renewenvironment{abstract}{%
  \idp@tituloelemento{Abstract}%
  \idpcorpodez\setlength{\parindent}{0pt}\selectlanguage{english}\noindent\ignorespaces
}{%
  \par\vspace{2\baselineskip}%
  \noindent\textbf{Keywords:} \idp@keywords\par
  \selectlanguage{brazilian}\clearpage
}
% Resumo em outro idioma qualquer
\newenvironment{resumoestrangeiro}[2]{%
  \idp@tituloelemento{#1}%
  \espacosimples\setlength{\parindent}{0pt}\noindent\ignorespaces
  \def\idp@kwtmp{#2}%
}{%
  \par\vspace{2\idplinhasimp}%
  \noindent\textbf{\idp@kwtmp}
  \clearpage
}

%%-----------------------------------------------------------------------------
%% 15. LISTAS DE ILUSTRACOES, TABELAS, QUADROS, GRAFICOS E SIGLAS
%%-----------------------------------------------------------------------------
% Entradas das listas: "Figura 1 - Titulo ......... 14"
\newcommand{\idp@entradalista}[2]{%
  \titlecontents{#1}[0pt]
    {\espacoumemeio}
    {#2~\thecontentslabel\ - }
    {}
    {\titlerule*[1.1mm]{.}\contentspage}%
}
\idp@entradalista{figure}{Figura}
\idp@entradalista{table}{Tabela}
\idp@entradalista{quadro}{Quadro}
\idp@entradalista{gfc}{Gr\'afico}

\newcommand{\idp@listaformato}[1]{%
  \begingroup
  \espacoumemeio
  \setlength{\parskip}{0pt}%
  #1%
  \endgroup
}
\newcommand{\listailustracoes}{%
  \idp@tituloelemento{Lista de Ilustra\c{c}\~oes}%
  \idp@listaformato{\@starttoc{lof}}\clearpage}
\newcommand{\listatabelas}{%
  \idp@tituloelemento{Lista de Tabelas}%
  \idp@listaformato{\@starttoc{lot}}\clearpage}
\newcommand{\listaquadros}{%
  \idp@tituloelemento{Lista de Quadros}%
  \idp@listaformato{\@starttoc{loq}}\clearpage}
\newcommand{\listagraficos}{%
  \idp@tituloelemento{Lista de Gr\'aficos}%
  \idp@listaformato{\@starttoc{lgr}}\clearpage}

% Lista de abreviaturas e siglas: sigla na margem, significado a 2,5 cm
\newenvironment{siglas}{%
  \idp@tituloelemento{Lista de Abreviaturas e Siglas}%
  \espacoumemeio
  \begin{list}{}{%
    \setlength{\labelwidth}{25mm}%
    \setlength{\leftmargin}{25mm}%
    \setlength{\labelsep}{0pt}%
    \setlength{\itemindent}{0pt}%
    \setlength{\topsep}{0pt}\setlength{\partopsep}{0pt}%
    \setlength{\parsep}{0pt}\setlength{\itemsep}{0pt}%
    \renewcommand{\makelabel}[1]{##1\hfill}}%
}{\end{list}\clearpage}
\newcommand{\sigla}[2]{\item[#1]#2}

% Glossario simples (mesma estrutura)
\newenvironment{glossario}{%
  \idp@tituloelemento{Gloss\'ario}\espacoumemeio
  \begin{description}[leftmargin=0pt,style=nextline,font=\normalfont\bfseries]
}{\end{description}\clearpage}

%%-----------------------------------------------------------------------------
%% 16. SUMARIO (NBR 6027)
%%-----------------------------------------------------------------------------
% NBR 6027, 5.4.1 e 5.4.2 (citadas no modelo 2026): os indicativos ficam
% alinhados a esquerda e os titulos alinhados pela margem do titulo do
% indicativo mais extenso. A largura do maior indicativo e medida a cada
% compilacao e gravada no .aux, para a compilacao seguinte. Entradas sem
% indicativo (REFERENCIAS, APENDICE, ANEXO) ficam rentes a margem.
% O modelo 2026 nao usa pontilhado entre o titulo e a pagina.
\newlength{\idp@tocatual}
\newdimen\idp@tocmaxrun   \idp@tocmaxrun=0pt
\def\idp@tocmax{10mm}
\newcommand{\idp@toclabel}[1]{%
  \settowidth{\idp@tocatual}{#1}%
  \ifdim\idp@tocatual>\idp@tocmaxrun\global\idp@tocmaxrun=\idp@tocatual\fi
  \ifdim\idp@tocatual>0pt
    \makebox[\dimexpr\idp@tocmax+\idp@distnum\relax][l]{#1}%
  \fi}
\AtEndDocument{%
  \ifdim\idp@tocmaxrun>0pt
    \immediate\write\@auxout{\gdef\string\idp@tocmax{\the\idp@tocmaxrun}}%
  \fi}
\contentsmargin{0pt}   % numero de pagina rente a margem direita

\titlecontents{section}[0pt]
  {\espacoumemeio\bfseries}
  {\idp@toclabel{\thecontentslabel}}
  {}
  {\hfill\contentspage}
\titlecontents{subsection}[0pt]
  {\espacoumemeio\bfseries}
  {\idp@toclabel{\thecontentslabel}}
  {}
  {\hfill\contentspage}
\titlecontents{subsubsection}[0pt]
  {\espacoumemeio}
  {\idp@toclabel{\thecontentslabel}}
  {}
  {\hfill\contentspage}
\titlecontents{paragraph}[0pt]
  {\espacoumemeio}
  {\idp@toclabel{\thecontentslabel}}
  {}
  {\hfill\contentspage}

\newcommand{\sumario}{%
  \idp@tituloelemento[2\idplinha]{Sum\'ario}%
  \begingroup
    \espacoumemeio
    \makeatletter\@starttoc{toc}\makeatother
  \endgroup
  \clearpage
}

% Entrada nao numerada no sumario (REFERENCIAS, APENDICES, ANEXOS...)
\newcommand{\idpaddtoc}[1]{%
  \phantomsection
  \addcontentsline{toc}{section}{\protect\numberline{}#1}%
}

%%-----------------------------------------------------------------------------
%% 17. PARTES DO DOCUMENTO
%%-----------------------------------------------------------------------------
\newcommand{\pretextual}{%
  \pagestyle{idpsemnumero}\pagenumbering{arabic}%
}
\newcommand{\textual}{%
  \clearpage
  \pagestyle{idp}\thispagestyle{idp}%
  \espacoumemeio
}
\newcommand{\postextual}{%
  \clearpage
  \pagestyle{idp}%
}

%%-----------------------------------------------------------------------------
%% 18. APENDICES E ANEXOS
%%-----------------------------------------------------------------------------
\newcounter{idp@apendice}
\newcounter{idp@anexo}
\newcommand{\apendice}[1]{%
  \clearpage\stepcounter{idp@apendice}%
  \idpaddtoc{AP\^ENDICE \Alph{idp@apendice} \textendash\ #1}%
  {\centering\bfseries AP\^ENDICE \Alph{idp@apendice} \textendash\
   \MakeUppercase{#1}\par}%
  \vspace{\idplinha}%
}
\newcommand{\anexo}[1]{%
  \clearpage\stepcounter{idp@anexo}%
  \idpaddtoc{ANEXO \Alph{idp@anexo} \textendash\ #1}%
  {\centering\bfseries ANEXO \Alph{idp@anexo} \textendash\
   \MakeUppercase{#1}\par}%
  \vspace{\idplinha}%
}

%%-----------------------------------------------------------------------------
%% 19. REFERENCIAS (NBR 6023) via biblatex-abnt
%%     - titulo destacado em negrito
%%     - autor repetido substituido por travessao
%%     - espacamento simples, alinhadas a esquerda, separadas por uma linha
%%-----------------------------------------------------------------------------
\RequirePackage[autostyle=true]{csquotes}
\RequirePackage[backend=biber,
                style=abnt,
                sorting=nyt,        % ordem alfabetica: nome, titulo, ano
                maxbibnames=99,     % NBR 6023: lista todos os autores
                minbibnames=99,
                maxcitenames=3,     % 4 ou mais autores -> "et al." na citacao
                mincitenames=1,
                giveninits=false,   % nomes por extenso (padrao do IDP)
                usedashes=true,     % autor repetido -> travessao (______.)
                repeatfields=false,
                accite=true,        % NBR 10520: autor em CAIXA ALTA entre parenteses
                ittitles=false,     % titulo em NEGRITO (como no template do IDP)
                natbib=true         % habilita \citeonline, \citet, \citep
               ]{biblatex}

\defbibheading{idpbib}[\refname]{}
\setlength{\bibitemsep}{\idplinhasimp}
\setlength{\bibhang}{0pt}

% Autor repetido: o modelo 2026 repete o nome por extenso em cada referencia
% (como as cinco entradas da ABNT no proprio modelo). A opcao de classe
% `refautortraco' volta ao travessao do modelo antigo ("_______.").
% A opcao precisa valer ja no preambulo: aplicada so no \begin{document} ela
% chegava tarde e o estilo abnt continuava trocando o autor pelo travessao.
% No estilo abnt quem decide e o toggle `repeatfields'.
\ifidp@autorrepetido
  \ExecuteBibliographyOptions{usedashes=false,repeatfields=true}
\else
  \AtBeginDocument{%
    \renewcommand*{\bibnameunderscore}{\underline{\hspace*{3.7em}}}%
    \renewcommand*{\bibnamedash}{\bibnameunderscore\addperiod\addspace}}
\fi

\newcommand{\referencias}{%
  \clearpage
  \idpaddtoc{REFER\^ENCIAS}%
  {\centering\normalfont\normalsize\bfseries REFER\^ENCIAS\par}%
  \vspace{2\idplinha}%   % modelo 2026: duas linhas entre o titulo e a 1a referencia
  \begingroup
    \espacosimples
    \raggedright
    \printbibliography[heading=idpbib]%
  \endgroup
}

% Aliases de citacao no estilo abntex2
\newcommand{\citeonline}[2][]{\textcite[#1]{#2}}
\newcommand{\citacaodireta}[3][]{(\textsc{#2}, #3)}

%%-----------------------------------------------------------------------------
%% 20. HIPERLINKS E METADADOS DO PDF
%%-----------------------------------------------------------------------------
\RequirePackage{xcolor}
\ifidp@links
  \RequirePackage[colorlinks=true,linkcolor=blue,citecolor=blue,
                  urlcolor=blue,breaklinks=true]{hyperref}
\else
  \RequirePackage[hidelinks,breaklinks=true]{hyperref}
\fi
\RequirePackage{url}
\urlstyle{same}

% Rede de seguranca: comandos da classe que porventura cheguem a um PDF string
% (bookmarks, \pdftitle, \pdfauthor) sao neutralizados aqui, em vez de
% dependerem do tratamento que cada versao do hyperref oferece.
% (\idp@campovazio nao precisa entrar aqui: ja produz texto puro.)
\pdfstringdefDisableCommands{%
  \let\idptabbox\@firstofone
  \let\idpnumtitulo\@firstofone
  \let\pendente\@firstofone
  \let\espacosimples\@empty
  \let\espacoumemeio\@empty
  \let\idpcorpodez\@empty
  \let\idpcorpoonze\@empty
}

\AtBeginDocument{%
  \hypersetup{%
    pdftitle={\idp@titulo},
    pdfauthor={\idp@autor},
    pdfsubject={\idp@instituicao},
    pdfkeywords={\idp@palavraschave},
    pdfcreator={LaTeX com a classe idp.cls}}%
}

%%-----------------------------------------------------------------------------
%% 21. MARCA D'AGUA DE RASCUNHO (opcional)
%%-----------------------------------------------------------------------------
\ifidp@rascunho
  \RequirePackage{draftwatermark}
  \SetWatermarkText{RASCUNHO}
  \SetWatermarkScale{0.8}
  \SetWatermarkLightness{0.93}
\fi

%%-----------------------------------------------------------------------------
%% 22. AJUSTES FINAIS
%%-----------------------------------------------------------------------------
% Nomes em portugues para os elementos flutuantes
\AtBeginDocument{%
  \renewcommand{\figurename}{Figura}%
  \renewcommand{\tablename}{Tabela}%
  \renewcommand{\contentsname}{Sum\'ario}%
  \renewcommand{\listfigurename}{Lista de Ilustra\c{c}\~oes}%
  \renewcommand{\listtablename}{Lista de Tabelas}%
  \renewcommand{\refname}{Refer\^encias}%
  \renewcommand{\bibname}{Refer\^encias}%
}

% Evita paginas com linhas orfas/viuvas
\widowpenalty=10000
\clubpenalty=10000

\endinput
%%============================== fim de idp.cls ===============================
