// Gera apresentacao_dissertacao.pptx.
//
//   uv run --with pandas --with numpy python prepara_dados.py   (uma vez, lê as tabelas .tex)
//   npm install
//   node gerar_apresentacao.js
//
// Os números vêm de dados_slides.json (extraídos da dissertação) e o texto falado
// vem de conteudo.js. Nada é digitado à mão aqui.
const path = require('path');
const fs = require('fs');
const pptxgen = require('pptxgenjs');
const { applyTheme } = require('./ferramentas/apply_theme.js');
const { SLIDES, RITMO_PALAVRAS_POR_MINUTO } = require('./conteudo.js');
const { VARIANTES, configurarLayouts } = require('./variantes.js');
const argumento = process.argv.indexOf('--versao');
const numeroVersao = argumento === -1 ? 1 : Number(process.argv[argumento + 1]);
const variante = VARIANTES.find(v => v.numero === numeroVersao);
if (!variante) throw new Error('Use --versao com um número de 1 a 10.');

const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'dados_slides.json'), 'utf8'));
const ARQUIVO = path.join(__dirname, argumento === -1 ? 'apresentacao_dissertacao.pptx' : `apresentacao_${String(numeroVersao).padStart(2, '0')}.pptx`);

// ------------------------------------------------------------------ tema ----
// O verde do Palmeiras é o mesmo da dissertação (verdepalmeiras, 006437).
const THEME = {
  name: 'Verde Acadêmico',
  headFontFace: 'Cambria',   // títulos e números de destaque: serifada, de texto acadêmico
  bodyFontFace: 'Calibri',   // corpo
  colors: {
    dk1: '10281D',      // texto
    lt1: 'FFFFFF',
    dk2: '0B3B2A',      // verde profundo: fundos escuros e títulos
    lt2: 'EEF4F0',      // verde-gelo: cartões
    accent1: '006437',  // verde Palmeiras
    accent2: '0B3B2A',
    accent3: '3F8F68',  // verde médio
    accent4: 'A9CDB8',  // verde claro
    accent5: 'B08A22',  // dourado escuro: contraste de 3:1 ou mais sobre branco e sobre o verde
    accent6: '5F7367',  // cinza-esverdeado: legendas e fontes
    hlink: '006437',
    folHlink: '4E6A5C',
  },
};
THEME.name = variante.nome;
THEME.headFontFace = variante.titulo || 'Cambria';
Object.assign(THEME.colors, {
  accent1: variante.verde, dk2: variante.profundo, accent2: variante.profundo,
  lt2: variante.claro, lt1: variante.fundo || 'FFFFFF', hlink: variante.verde,
});
const H = THEME.colors;   // hex, para os gráficos (que não aceitam cor de tema)

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';   // 13,33" x 7,5"
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Exposição ocupacional à inteligência artificial e transições no mercado de trabalho brasileiro';
pres.author = 'Ricardo Carvalho';
pres.subject = 'Apresentação da dissertação de mestrado, resultados preliminares';
pres.company = 'IDP';
const C = pres.SchemeColor;
configurarLayouts(pres, variante);

// ------------------------------------------------------------- utilidades ----
const L = 0.6, R = 12.73, LARG = R - L;          // margens laterais da área útil
const MENOS = '−';
const f = (v, d = 2) => v.toFixed(d).replace('.', ',');
const sg = (v, d = 2) => (v > 0 ? '+' : v < 0 ? MENOS : '') + f(Math.abs(v), d);
const mmss = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
const FOOT = 'Exposição ocupacional à IA e transições no mercado de trabalho brasileiro · IDP · 2026';

// ------------------------------------------------------------------ layouts ---
pres.defineSlideMaster({
  title: 'CONTEUDO',
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: L, y: 0.4, w: LARG, h: 0.95, fontSize: 34, bold: true, color: C.text2, align: variante.centralizar ? 'center' : 'left', valign: 'middle', margin: 0 }, text: 'Título do slide' } },
    { text: { text: FOOT, options: { x: L, y: 7.0, w: 10.5, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.1, y: 7.0, w: 0.63, h: 0.3, fontSize: 10, color: C.accent6, align: 'right' },
});
pres.defineSlideMaster({
  title: 'ABERTURA',
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.9, y: 1.55, w: 9.6, h: 2.5, fontSize: 38, bold: true, color: C.background1, align: variante.centralizar ? 'center' : 'left', valign: 'top', margin: 0 }, text: 'Título' } },
    { placeholder: { options: { name: 'subtitulo', type: 'body', x: 0.9, y: 4.2, w: 9.6, h: 0.9, fontSize: 20, color: C.accent4, align: 'left', valign: 'top', margin: 0 }, text: 'Subtítulo' } },
  ],
});
pres.defineSlideMaster({
  title: 'FECHO',
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: L, y: 0.4, w: LARG, h: 0.95, fontSize: 34, bold: true, color: C.background1, align: variante.centralizar ? 'center' : 'left', valign: 'middle', margin: 0 }, text: 'Título do slide' } },
    { text: { text: FOOT, options: { x: L, y: 7.0, w: 10.5, h: 0.3, fontSize: 10, color: C.accent4, margin: 0 } } },
  ],
  slideNumber: { x: 12.1, y: 7.0, w: 0.63, h: 0.3, fontSize: 10, color: C.accent4, align: 'right' },
});

// ------------------------------------------------------- blocos reutilizáveis ----
// Cartão com fundo verde-gelo; o texto entra como sequência de trechos.
function cartao(slide, x, y, w, h, runs, nome, extra = {}) {
  slide.addText(runs, Object.assign({
    shape: pres.ShapeType.roundRect, rectRadius: 0.1, x, y, w, h,
    fill: { color: C.background2 }, line: { type: 'none' },
    margin: [0.14, 0.2, 0.14, 0.2], valign: 'top', fontSize: 14, color: C.text1,
    objectName: nome,
  }, extra));
}
// Número, ícone ou letra dentro de um círculo.
function disco(slide, x, y, d, txt, fill, cor, nome, tam = 16) {
  slide.addText(txt, {
    shape: pres.ShapeType.ellipse, x, y, w: d, h: d, fill: { color: fill }, line: { type: 'none' },
    align: 'center', valign: 'middle', bold: true, fontSize: tam, color: cor, margin: 0, objectName: nome,
  });
}
// Linha de fonte, no pé do slide.
function fonte(slide, txt) {
  slide.addText(txt, { x: L, y: 6.66, w: LARG, h: 0.28, fontSize: 11, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Fonte' });
}
// Rótulo pequeno em caixa alta.
function rotulo(slide, txt, x, y, w, cor = C.accent1) {
  slide.addText(txt, { x, y, w, h: 0.3, fontSize: 12, bold: true, color: cor, charSpacing: 2, margin: 0, isTextBox: true, objectName: 'Rótulo' });
}
// Título de gráfico, em texto (o gráfico em si fica sem título interno).
function tituloGrafico(slide, txt, x, y, w) {
  slide.addText(txt, { x, y, w, h: 0.4, fontSize: 16, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: 'Título do gráfico' });
}
// Opções comuns a todos os gráficos, para que tenham a mesma cara no deck inteiro.
function opcoesGrafico(extra) {
  return Object.assign({
    catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', dataLabelFontFace: '+mn-lt', legendFontFace: '+mn-lt',
    catAxisLabelFontSize: 13, valAxisLabelFontSize: 12, dataLabelFontSize: 13, legendFontSize: 13,
    catAxisLabelColor: H.dk1, valAxisLabelColor: H.accent6, dataLabelColor: H.dk1, legendColor: H.dk1,
    catGridLine: { style: 'none' }, valGridLine: { color: 'DCE6E0', size: 0.75 },
    showTitle: false,
  }, extra);
}

const NOTAS = {};
for (const s of SLIDES) NOTAS[s.id] = s;
let relogio = 0;
function notas(slide, id, n) {
  const s = NOTAS[id];
  relogio += s.segundos;
  const cab = `[Slide ${n} de ${SLIDES.length} · tempo previsto ${mmss(s.segundos)} · deve terminar em ${mmss(relogio)} do relógio]`;
  slide.addNotes(`${cab}\n\n${s.leitura}`);
}

// ====================================================================== 1 ====
pres.addSection({ title: 'Abertura' });
{
  const s = pres.addSlide({ masterName: 'ABERTURA', sectionTitle: 'Abertura' });
  // Duas circunferências ao fundo: o círculo central de um campo, sem apelo de torcida.
  s.addShape(pres.ShapeType.ellipse, { x: 9.9, y: 3.0, w: 6.4, h: 6.4, fill: { color: C.accent1, transparency: 70 }, line: { color: C.accent3, width: 1.5, transparency: 40 }, objectName: 'Circunferência maior' });
  s.addShape(pres.ShapeType.ellipse, { x: 11.2, y: 4.5, w: 4.0, h: 4.0, fill: { color: C.accent1, transparency: 60 }, line: { color: C.accent4, width: 1, transparency: 50 }, objectName: 'Circunferência menor' });
  rotulo(s, 'DISSERTAÇÃO DE MESTRADO · RESULTADOS PRELIMINARES', 0.9, 0.95, 9, C.accent4);
  s.addText(SLIDES[0].titulo, { placeholder: 'title' });
  s.addText('evidências de painel da PNAD Contínua após o lançamento público do ChatGPT', { placeholder: 'subtitulo' });
  s.addText([
    { text: 'Ricardo Carvalho', options: { bold: true, fontSize: 20, color: C.background1, breakLine: true } },
    { text: 'Orientador: Prof. Dr. Danny de Castro Soares', options: { fontSize: 16, color: C.accent4, breakLine: true } },
    { text: 'Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa · Brasília · 2026', options: { fontSize: 14, color: C.accent4 } },
  ], { x: 0.9, y: 5.55, w: 9.6, h: 1.2, margin: 0, valign: 'top', isTextBox: true, objectName: 'Autoria' });
  notas(s, 'titulo', 1);
}

// ====================================================================== 2 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Abertura' });
  s.addText(SLIDES[1].titulo, { placeholder: 'title' });

  // A pergunta
  cartao(s, L, 1.55, LARG, 1.65, [
    { text: 'Trabalhadores em ocupações mais expostas à inteligência artificial passaram a apresentar transições de trabalho distintas depois do lançamento do ChatGPT?', options: { fontFace: '+mj-lt', fontSize: 28, color: C.text2, italic: true } },
  ], 'Pergunta de pesquisa', { margin: [0.12, 0.3, 0.12, 0.3], valign: 'middle' });

  // Linha do tempo: 15 trimestres pré, 12 pós
  const wPre = LARG * 15 / 27, xMarco = L + wPre;
  s.addText('PRÉ · 15 trimestres de origem', { shape: pres.ShapeType.rect, x: L, y: 4.05, w: wPre, h: 0.55, fill: { color: C.accent3 }, line: { type: 'none' }, color: C.background1, bold: true, fontSize: 14, align: 'center', valign: 'middle', margin: 0, objectName: 'Período pré' });
  s.addText('PÓS · 12 trimestres de origem', { shape: pres.ShapeType.rect, x: xMarco, y: 4.05, w: LARG - wPre, h: 0.55, fill: { color: C.accent1 }, line: { type: 'none' }, color: C.background1, bold: true, fontSize: 14, align: 'center', valign: 'middle', margin: 0, objectName: 'Período pós' });
  s.addShape(pres.ShapeType.line, { x: xMarco, y: 3.68, w: 0, h: 1.08, line: { color: C.accent5, width: 2.5 }, objectName: 'Marco' });
  s.addText('30/11/2022 · lançamento público do ChatGPT', { x: xMarco - 2.6, y: 3.4, w: 5.2, h: 0.3, fontSize: 14, bold: true, color: C.text2, align: 'center', margin: 0, isTextBox: true, objectName: 'Rótulo do marco' });
  s.addText('2019T1', { x: L, y: 4.66, w: 1.5, h: 0.28, fontSize: 12, color: C.accent6, margin: 0, isTextBox: true });
  s.addText('2022T3 | 2022T4', { x: xMarco - 1.2, y: 4.66, w: 2.4, h: 0.28, fontSize: 12, color: C.accent6, align: 'center', margin: 0, isTextBox: true });
  s.addText('2025T3', { x: R - 1.5, y: 4.66, w: 1.5, h: 0.28, fontSize: 12, color: C.accent6, align: 'right', margin: 0, isTextBox: true });

  // Três definições
  const defs = [
    ['Exposição', 'Propriedade da ocupação, medida por um índice. Não é adoção de IA nem risco de demissão.'],
    ['Transição', 'O que acontece com a mesma pessoa entre duas entrevistas trimestrais consecutivas.'],
    ['Marco', 'Lançamento do ChatGPT: único, nacional e exterior às decisões de quem está na amostra.'],
  ];
  const w3 = (LARG - 2 * 0.22) / 3;
  defs.forEach(([t, d], i) => cartao(s, L + i * (w3 + 0.22), 5.15, w3, 1.45, [
    { text: t, options: { bold: true, fontSize: 18, color: C.accent1, breakLine: true } },
    { text: d, options: { fontSize: 15 } },
  ], 'Definição: ' + t));
  notas(s, 'pergunta', 2);
}

// ====================================================================== 3 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Abertura' });
  s.addText(SLIDES[2].titulo, { placeholder: 'title' });
  const colunas = [
    ['1', 'Medir a exposição', [
      ['Felten, Raj e Seamans (2021)', 'AIOE: liga as habilidades de cada ocupação a aplicações de IA.'],
      ['Eloundou et al. (2024)', 'Exposição tarefa a tarefa, específica para modelos de linguagem.'],
    ]],
    ['2', 'Observar adoção e resultados', [
      ['Brynjolfsson, Li e Raymond (2025)', 'Ganho de produtividade numa central de atendimento.'],
      ['Humlum e Vestergaard (2025)', 'Dinamarca: efeitos nulos e precisos sobre rendimentos e horas.'],
    ]],
    ['3', 'Desenho e contexto brasileiro', [
      ['Acemoglu e Restrepo (2020)', 'Identificação por exposição diferencial.'],
      ['Ulyssea (2020); Meghir, Narita e Robin (2015)', 'Informalidade heterogênea; fronteira com o setor formal atravessada com frequência.'],
    ]],
  ];
  const w3 = (LARG - 2 * 0.22) / 3;
  colunas.forEach(([n, titulo, itens], i) => {
    const x = L + i * (w3 + 0.22);
    cartao(s, x, 1.55, w3, 3.75, [], 'Coluna ' + n);
    disco(s, x + 0.2, 1.75, 0.5, n, C.accent1, C.background1, 'Número ' + n, 18);
    s.addText(titulo, { x: x + 0.82, y: 1.75, w: w3 - 1.0, h: 0.5, fontSize: 18, bold: true, color: C.text2, valign: 'middle', margin: 0, isTextBox: true, objectName: 'Título da coluna ' + n });
    const runs = [];
    itens.forEach(([autor, desc], k) => {
      runs.push({ text: autor, options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true } });
      runs.push({ text: desc, options: { fontSize: 16, color: C.text1, breakLine: k < itens.length - 1, paraSpaceAfter: 14 } });
    });
    s.addText(runs, { x: x + 0.2, y: 2.45, w: w3 - 0.4, h: 2.7, valign: 'top', margin: 0, isTextBox: true, objectName: 'Itens da coluna ' + n });
  });
  s.addText([
    { text: 'LACUNA  ', options: { bold: true, fontSize: 13, color: C.accent5, charSpacing: 2 } },
    { text: 'Não há, no Brasil, medida direta de adoção de IA em base representativa. Por isso: exposição ocupacional aplicada a um painel domiciliar rotativo.', options: { fontSize: 17, color: C.background1 } },
  ], { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y: 5.55, w: LARG, h: 1.0, fill: { color: C.accent2 }, line: { type: 'none' }, margin: [0.1, 0.3, 0.1, 0.3], valign: 'middle', objectName: 'Lacuna' });
  notas(s, 'literatura', 3);
}

// ====================================================================== 4 ====
pres.addSection({ title: 'Dados e método' });
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Dados e método' });
  s.addText(SLIDES[3].titulo, { placeholder: 'title' });
  const esc = D.escala;
  const grandes = [
    ['27', 'trimestres de origem, de 2019T1 a 2025T3'],
    [String(esc[0].ocupacoes), 'ocupações na estimação'],
    [esc[0].upas.toLocaleString('pt-BR'), 'unidades primárias de amostragem (UPAs)'],
  ];
  grandes.forEach(([n, t], i) => {
    const y = 1.55 + i * 1.28;
    cartao(s, L, y, 3.9, 1.15, [], 'Número-chave ' + (i + 1));
    s.addText(n, { x: L + 0.2, y: y + 0.08, w: 3.5, h: 0.62, fontFace: '+mj-lt', fontSize: 38, bold: true, color: C.accent1, margin: 0, isTextBox: true, objectName: 'Valor ' + (i + 1) });
    s.addText(t, { x: L + 0.2, y: y + 0.7, w: 3.5, h: 0.38, fontSize: 14, color: C.text1, margin: 0, isTextBox: true, objectName: 'Rótulo ' + (i + 1) });
  });
  cartao(s, L, 5.45, 3.9, 1.1, [
    { text: 'Par pessoa-trimestre reconstruído: ', options: { bold: true, color: C.accent1 } },
    { text: 'UPA, domicílio, ordem, sexo, dia e mês de nascimento e idade coerentes.', options: {} },
  ], 'Regra do par', { fontSize: 14, margin: [0.12, 0.2, 0.1, 0.2] });

  const x0 = 4.85;
  tituloGrafico(s, 'Pessoas-transições por domínio de estimação', x0, 1.5, R - x0);
  const rot = ['Pareamento (todas as origens)', 'Saída do emprego (pares)', 'Muda de ocupação (destino ocupado)', 'Margens direcionais (AIOE nos dois lados)', 'Informalização (origem formal)'];
  s.addChart(pres.charts.BAR, [{ name: 'Pessoas-transições', labels: rot, values: esc.map(r => r.pessoas_transicoes) }], opcoesGrafico({
    x: x0, y: 1.95, w: R - x0, h: 4.55, barDir: 'bar', barGapWidthPct: 45, chartColors: [H.accent1], catAxisOrientation: 'maxMin',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '#,##0', valAxisHidden: true, valGridLine: { style: 'none' },
    valAxisMinVal: 0, valAxisMaxVal: 5000000, showLegend: false, altText: 'Barras horizontais com as pessoas-transições de cada domínio de estimação, de 3,96 milhões a 1,68 milhão.',
  }));
  fonte(s, 'Fonte: elaboração própria a partir da PNADC/IBGE. São pessoas-transições, e não pessoas únicas: o mesmo indivíduo contribui com até quatro pares.');
  notas(s, 'dados', 4);
}

// ====================================================================== 5 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Dados e método' });
  s.addText(SLIDES[4].titulo, { placeholder: 'title' });
  const caixas = [['COD', 'classificação da PNAD Contínua'], ['ISCO-08', 'classificação internacional'], ['SOC 2010 → AIOE', 'índice de Felten, Raj e Seamans (2021)']];
  caixas.forEach(([t, d], i) => {
    const y = 1.6 + i * 1.1;
    s.addText([
      { text: t, options: { bold: true, fontSize: 18, color: i === 2 ? C.background1 : C.text2, breakLine: true } },
      { text: d, options: { fontSize: 13, color: i === 2 ? C.accent4 : C.accent6 } },
    ], { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y, w: 4.9, h: 0.82, fill: { color: i === 2 ? C.accent1 : C.background2 }, line: { type: 'none' }, margin: [0.06, 0.25, 0.06, 0.25], valign: 'middle', objectName: 'Etapa da ponte ' + (i + 1) });
    if (i < 2) s.addShape(pres.ShapeType.downArrow, { x: L + 2.2, y: y + 0.84, w: 0.5, h: 0.24, fill: { color: C.accent3 }, line: { type: 'none' }, objectName: 'Seta ' + (i + 1) });
  });
  s.addText('Entre os códigos SOC ligados a um mesmo COD, o peso é uniforme: hipótese de construção, declarada como tal.', { x: L, y: 4.92, w: 4.9, h: 0.62, fontSize: 14, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Nota da ponte' });
  const chips = [['416', 'códigos com AIOE'], ['413', 'na estimação'], ['1,08%', 'do peso sem AIOE']];
  const wc = (4.9 - 2 * 0.15) / 3;
  chips.forEach(([n, t], i) => {
    const x = L + i * (wc + 0.15);
    cartao(s, x, 5.6, wc, 0.98, [], 'Cobertura ' + (i + 1));
    s.addText(n, { x, y: 5.64, w: wc, h: 0.5, fontFace: '+mj-lt', fontSize: 24, bold: true, color: C.accent1, align: 'center', margin: 0, isTextBox: true });
    s.addText(t, { x, y: 6.14, w: wc, h: 0.36, fontSize: 12, color: C.text1, align: 'center', margin: 0, isTextBox: true });
  });

  const x0 = 5.9;
  tituloGrafico(s, 'Distribuição do AIOE entre os códigos ocupacionais', x0, 1.5, R - x0);
  const a = D.aioe;
  const labels = a.contagens.map((_, i) => (i % 4 === 0 ? f(a.bordas[i], 1) : ''));   // só um rótulo a cada quatro faixas
  s.addChart(pres.charts.BAR, [{ name: 'Ocupações', labels, values: a.contagens }], opcoesGrafico({
    x: x0, y: 1.95, w: R - x0, h: 3.55, barDir: 'col', barGapWidthPct: 6, chartColors: [H.accent1], showValue: false, showLegend: false,
    catAxisLabelRotate: 0, valAxisMinVal: 0, valAxisMaxVal: 45, valAxisMajorUnit: 15, catAxisLabelFontSize: 12,
    altText: 'Histograma do AIOE entre 416 códigos ocupacionais, com valores de cerca de menos 2,1 a 1,4 e pico de 42 ocupações perto de menos 1.',
  }));
  s.addText([
    { text: '← menos exposta', options: { color: C.accent6 } },
    { text: '                                                                          ', options: {} },
    { text: 'mais exposta →', options: { color: C.accent6 } },
  ], { x: x0, y: 5.5, w: R - x0, h: 0.3, fontSize: 12, align: 'center', margin: 0, isTextBox: true, objectName: 'Sentido do eixo' });
  s.addText(`média ${f(a.media, 4)} · desvio-padrão ${f(a.dp, 4)} · correlação com a teletrabalhabilidade: 0,702`, { x: x0, y: 5.82, w: R - x0, h: 0.3, fontSize: 13, bold: true, color: C.text2, align: 'center', margin: 0, isTextBox: true, objectName: 'Estatísticas do AIOE' });
  s.addText('Menor AIOE quer dizer menos exposição, e não emprego pior.', { x: x0, y: 6.2, w: R - x0, h: 0.34, fontSize: 14, italic: true, color: C.text2, align: 'center', margin: 0, isTextBox: true, objectName: 'Aviso de leitura' });
  fonte(s, 'Fonte: elaboração própria a partir de Felten, Raj e Seamans (2021), Dingel e Neiman (2020) e da PNADC/IBGE. Distribuição entre códigos, e não entre trabalhadores.');
  notas(s, 'exposicao', 5);
}

// ====================================================================== 6 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Dados e método' });
  s.addText(SLIDES[5].titulo, { placeholder: 'title' });
  const fam = [
    ['I', 'Continuidade e vínculo', [
      ['Pareamento (teste de atrito)', '1 se a entrevista seguinte foi encontrada'],
      ['Saída do emprego', '1 se o destino não está ocupado'],
      ['De formal para informal', '1 se o destino é ocupado e informal, entre origens formais'],
    ]],
    ['II', 'Mobilidade ocupacional', [
      ['Muda de ocupação (2 dígitos)', '1 se o código muda nos dois primeiros dígitos'],
      ['Muda de ocupação (3 dígitos)', '1 se o código muda nos três primeiros dígitos'],
    ]],
    ['III', 'Deslocamento no gradiente de exposição', [
      ['Menos exposta (descendente)', '1 se o AIOE do destino é menor que o da origem'],
      ['Mais exposta (ascendente)', '1 se o AIOE do destino é maior que o da origem'],
    ]],
  ];
  const w3 = (LARG - 2 * 0.22) / 3;
  fam.forEach(([n, t, itens], i) => {
    const x = L + i * (w3 + 0.22);
    cartao(s, x, 1.55, w3, 3.95, [], 'Família ' + n);
    disco(s, x + 0.2, 1.75, 0.55, n, C.accent1, C.background1, 'Família ' + n + ' (número)', 16);
    s.addText(t, { x: x + 0.9, y: 1.7, w: w3 - 1.1, h: 0.7, fontSize: 18, bold: true, color: C.text2, valign: 'middle', margin: 0, isTextBox: true, objectName: 'Título da família ' + n });
    const runs = [];
    itens.forEach(([nome, def], k) => {
      runs.push({ text: nome, options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true } });
      runs.push({ text: def, options: { fontSize: 15, color: C.text1, breakLine: k < itens.length - 1, paraSpaceAfter: 14 } });
    });
    s.addText(runs, { x: x + 0.25, y: 2.6, w: w3 - 0.5, h: 2.75, valign: 'top', margin: 0, isTextBox: true, objectName: 'Desfechos da família ' + n });
  });
  s.addText([
    { text: 'Domínio próprio. ', options: { bold: true, color: C.accent4 } },
    { text: 'Cada desfecho é estimado onde está definido, e ausência nunca vira zero. ', options: { color: C.background1 } },
    { text: 'Margens direcionais. ', options: { bold: true, color: C.accent4 } },
    { text: 'Leem-se juntas: origens mais expostas têm mais destinos possíveis abaixo delas.', options: { color: C.background1 } },
  ], { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y: 5.7, w: LARG, h: 0.9, fill: { color: C.accent2 }, line: { type: 'none' }, fontSize: 16, margin: [0.1, 0.3, 0.1, 0.3], valign: 'middle', objectName: 'Observação' });
  notas(s, 'desfechos', 6);
}

// ====================================================================== 7 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Dados e método' });
  s.addText(SLIDES[6].titulo, { placeholder: 'title' });
  const eq = { fontFace: '+mj-lt', fontSize: 23, color: C.text1 };
  const em = Object.assign({}, eq, { bold: true, color: C.accent1 });
  s.addText([
    { text: 'y  =  ', options: Object.assign({}, eq, { italic: true }) },
    { text: 'β', options: em }, { text: ' (AIOE × Pós)  +  ', options: eq },
    { text: 'γ', options: Object.assign({}, eq, { bold: true }) }, { text: ' (Teletrabalho × Pós)  +  idade  +  idade²', options: Object.assign({}, eq, { breakLine: true }) },
    { text: '        +  α', options: eq }, { text: 'ocupação', options: Object.assign({}, eq, { subscript: true }) },
    { text: '  +  λ', options: eq }, { text: 'UF×trimestre', options: Object.assign({}, eq, { subscript: true }) },
    { text: '  +  efeitos fixos categóricos  +  ε', options: eq },
  ], { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y: 1.55, w: LARG, h: 1.75, fill: { color: C.background2 }, line: { type: 'none' }, margin: [0.2, 0.35, 0.2, 0.35], valign: 'middle', lineSpacingMultiple: 1.25, objectName: 'Equação estimada' });

  const blocos = [
    ['β: parâmetro de interesse', 'Mudança entre pré e pós, em pontos percentuais por unidade de AIOE (cerca de um desvio-padrão entre ocupações).'],
    ['Efeitos fixos', 'Ocupação de origem · UF × trimestre · sexo, cor ou raça, escolaridade, tempo no emprego, tamanho do estabelecimento e setor.'],
    ['Estimação e inferência', 'Modelo de probabilidade linear ponderado pelo peso da origem. Erros-padrão por UPA, de 30.360 a 31.145 grupos.'],
  ];
  const w3 = (LARG - 2 * 0.22) / 3;
  blocos.forEach(([t, d], i) => cartao(s, L + i * (w3 + 0.22), 3.55, w3, 1.85, [
    { text: t, options: { bold: true, fontSize: 17, color: C.accent1, breakLine: true } },
    { text: d, options: { fontSize: 15 } },
  ], 'Bloco: ' + t));

  const wPre = LARG * 15 / 27, xMarco = L + wPre;
  s.addText('Pré · 2019T1 a 2022T3 · 15 trimestres', { shape: pres.ShapeType.rect, x: L, y: 5.7, w: wPre, h: 0.5, fill: { color: C.accent3 }, line: { type: 'none' }, color: C.background1, bold: true, fontSize: 14, align: 'center', valign: 'middle', margin: 0, objectName: 'Período pré' });
  s.addText('Pós · 2022T4 a 2025T3 · 12 trimestres', { shape: pres.ShapeType.rect, x: xMarco, y: 5.7, w: LARG - wPre, h: 0.5, fill: { color: C.accent1 }, line: { type: 'none' }, color: C.background1, bold: true, fontSize: 14, align: 'center', valign: 'middle', margin: 0, objectName: 'Período pós' });
  s.addShape(pres.ShapeType.line, { x: xMarco, y: 5.55, w: 0, h: 0.8, line: { color: C.accent5, width: 2.5 }, objectName: 'Marco' });
  s.addText('Tratamento contínuo: não há grupo tratado e grupo de controle, e sim uma intensidade de exposição que varia entre ocupações.', { x: L, y: 6.42, w: LARG, h: 0.4, fontSize: 13, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Nota do desenho' });
  notas(s, 'desenho', 7);
}

// ====================================================================== 8 ====
pres.addSection({ title: 'Resultados' });
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Resultados' });
  s.addText(SLIDES[7].titulo, { placeholder: 'title' });
  const d = nome => D.descritivas.find(r => r.desfecho.startsWith(nome));
  const ordem = [
    ['Muda de ocupação (3 dígitos)', 'Muda de ocupação (3 dígitos)'], ['Muda de ocupação (2 dígitos)', 'Muda de ocupação (2 dígitos)'],
    ['Transição para menor AIOE', 'Transição para menor AIOE'], ['Transição para maior AIOE', 'Transição para maior AIOE'],
    ['Transição de formal para informal', 'De formal para informal'], ['Saída do emprego', 'Saída do emprego'],
  ];
  const xl = L, wl = 6.5;
  tituloGrafico(s, 'Médias ponderadas antes e depois do marco (%)', xl, 1.5, wl);
  s.addChart(pres.charts.BAR, [
    { name: 'Pré (2019T1 a 2022T3)', labels: ordem.map(o => o[1]), values: ordem.map(o => Math.round(d(o[0]).pre * 1000) / 10) },
    { name: 'Pós (2022T4 a 2025T3)', labels: ordem.map(o => o[1]), values: ordem.map(o => Math.round(d(o[0]).pos * 1000) / 10) },
  ], opcoesGrafico({
    x: xl, y: 1.9, w: wl, h: 4.7, barDir: 'bar', barGrouping: 'clustered', barGapWidthPct: 40, chartColors: [H.accent4, H.accent1], catAxisOrientation: 'maxMin',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.0', valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMinVal: 0, valAxisMaxVal: 38,
    showLegend: true, legendPos: 'b', altText: 'Barras agrupadas com as médias de seis desfechos antes e depois do marco; todas aumentam, exceto a saída do emprego, que quase não muda.',
  }));

  const xr = 7.55, wr = R - xr;
  tituloGrafico(s, 'Permanência na mesma faixa: pós − pré (p.p.)', xr, 1.5, wr);
  const diag = D.matriz.map((m, i) => m.valores[i]);
  s.addChart(pres.charts.BAR, [{ name: 'Pós − pré', labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], values: diag }], opcoesGrafico({
    x: xr, y: 2.2, w: wr, h: 2.85, barDir: 'col', barGapWidthPct: 40, chartColors: [H.accent1], invertedColors: [H.accent1], catAxisLabelPos: 'low',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.0', valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMinVal: -10, valAxisMaxVal: 0,
    showLegend: false, altText: 'Colunas com a variação da permanência na mesma faixa de exposição: negativa nas cinco faixas, de menos 3,6 a menos 8,1 pontos percentuais.',
  }));
  s.addText('Q1 = menor exposição · Q5 = maior exposição', { x: xr, y: 1.9, w: wr, h: 0.3, fontSize: 12, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Legenda das faixas' });
  cartao(s, xr, 5.2, wr, 1.35, [
    { text: 'Cai em todas as cinco faixas', options: { bold: true, fontSize: 17, color: C.accent1, breakLine: true } },
    { text: 'Entre 3,6 e 8,1 p.p. Teste de Wald de igualdade das matrizes: χ² = 3.040,1, com 20 graus de liberdade.', options: { fontSize: 15 } },
  ], 'Teste de Wald', { margin: [0.12, 0.2, 0.1, 0.2] });
  fonte(s, 'Fonte: elaboração própria a partir da PNADC/IBGE. Médias ponderadas pelo peso da origem, cada uma no domínio do desfecho.');
  notas(s, 'descritivo', 8);
}

// ====================================================================== 9 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Resultados' });
  s.addText(SLIDES[8].titulo, { placeholder: 'title' });
  const A = D.principal.A;
  const nomes = ['Transição para menor AIOE', 'Muda de ocupação (3 dígitos)', 'Muda de ocupação (2 dígitos)', 'Saída do emprego', 'Pareamento (teste de atrito)', 'Formal → informal', 'Transição para maior AIOE'];
  const grupo = [0, 1, 1, 2, 3, 2, 0];
  const GR = [
    { nome: 'Deslocamento no gradiente', cor: H.accent1 }, { nome: 'Mobilidade ocupacional', cor: H.accent3 },
    { nome: 'Vínculo', cor: H.accent5 }, { nome: 'Teste de atrito', cor: H.accent6 },
  ];
  // geometria do gráfico de pontos: eixo de -2 a +3 p.p.
  const px0 = 4.25, px1 = 8.55, vmin = -2, vmax = 3, u = (px1 - px0) / (vmax - vmin);
  const X = v => px0 + (v - vmin) * u;
  const y0 = 2.05, dy = 0.55, yAxis = y0 + 7 * dy;
  // legenda
  let xl = L;
  GR.forEach(g => {
    s.addShape(pres.ShapeType.ellipse, { x: xl, y: 1.62, w: 0.16, h: 0.16, fill: { color: g.cor }, line: { type: 'none' }, objectName: 'Legenda: ' + g.nome });
    s.addText(g.nome, { x: xl + 0.22, y: 1.55, w: 2.1, h: 0.3, fontSize: 12, color: C.text1, margin: 0, isTextBox: true });
    xl += g.nome.length * 0.083 + 0.55;
  });
  // grade vertical e eixo
  for (let v = vmin; v <= vmax; v++) {
    s.addShape(pres.ShapeType.line, { x: X(v), y: y0 - 0.1, w: 0, h: yAxis - y0 + 0.1, line: { color: v === 0 ? H.dk1 : 'DCE6E0', width: v === 0 ? 1.5 : 0.75 }, objectName: 'Grade ' + v });
    s.addText(v === 0 ? '0' : (v > 0 ? '+' : MENOS) + Math.abs(v), { x: X(v) - 0.3, y: yAxis + 0.05, w: 0.6, h: 0.26, fontSize: 12, color: C.accent6, align: 'center', margin: 0, isTextBox: true });
  }
  s.addText('Efeito de AIOE × pós (p.p. por unidade de AIOE), com IC de 95%', { x: px0 - 0.9, y: yAxis + 0.32, w: px1 - px0 + 1.8, h: 0.28, fontSize: 12, color: C.accent6, align: 'center', margin: 0, isTextBox: true, objectName: 'Título do eixo' });
  A.forEach((r, i) => {
    const yc = y0 + i * dy + dy / 2, cor = GR[grupo[i]].cor, vazio = grupo[i] === 3;
    s.addText(nomes[i], { x: L, y: yc - 0.2, w: px0 - L - 0.2, h: 0.4, fontSize: 14, color: C.text1, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Rótulo: ' + nomes[i] });
    s.addShape(pres.ShapeType.line, { x: X(r.lo), y: yc, w: X(r.hi) - X(r.lo), h: 0, line: { color: cor, width: 2.5 }, objectName: 'IC 95%: ' + nomes[i] });
    [r.lo, r.hi].forEach(v => s.addShape(pres.ShapeType.line, { x: X(v), y: yc - 0.08, w: 0, h: 0.16, line: { color: cor, width: 2 }, objectName: 'Extremo do IC' }));
    s.addShape(pres.ShapeType.ellipse, { x: X(r.efeito) - 0.09, y: yc - 0.09, w: 0.18, h: 0.18, fill: { color: vazio ? 'FFFFFF' : cor }, line: { color: cor, width: 2 }, objectName: 'Estimativa: ' + nomes[i] });
    s.addText(sg(r.efeito), { x: X(r.efeito) - 0.5, y: yc - 0.42, w: 1.0, h: 0.24, fontSize: 12, bold: true, color: C.text1, align: 'center', margin: 0, isTextBox: true, objectName: 'Valor: ' + nomes[i] });
  });
  // destaques à direita
  const xr = 9.0, wr = R - xr;
  const cards = [
    [sg(A[0].efeito) + ' p.p.', 'transição para ocupação menos exposta', 'cerca de 12,6% da taxa pós, de 17,4%'],
    [sg(A[6].efeito) + ' p.p.', 'transição para ocupação mais exposta', 'as duas margens direcionais se leem juntas'],
    [sg(A[1].efeito) + ' · ' + sg(A[2].efeito) + ' p.p.', 'mudança de ocupação (3 e 2 dígitos)', 'p = 0,030 no de 2 dígitos: não citar isoladamente'],
  ];
  cards.forEach(([n, t, d], i) => {
    const y = 1.55 + i * 1.6;
    cartao(s, xr, y, wr, 1.5, [], 'Destaque ' + (i + 1));
    s.addText(n, { x: xr + 0.2, y: y + 0.08, w: wr - 0.4, h: 0.55, fontFace: '+mj-lt', fontSize: 28, bold: true, color: C.accent1, margin: 0, isTextBox: true, objectName: 'Valor do destaque ' + (i + 1) });
    s.addText([{ text: t, options: { bold: true, breakLine: true } }, { text: d, options: { fontSize: 12, color: C.accent6 } }], { x: xr + 0.2, y: y + 0.65, w: wr - 0.4, h: 0.8, fontSize: 14, color: C.text1, margin: 0, valign: 'top', isTextBox: true, objectName: 'Texto do destaque ' + (i + 1) });
  });
  fonte(s, 'Fonte: elaboração própria a partir da PNADC/IBGE. Erros-padrão por UPA; sete desfechos, sem correção para multiplicidade.');
  notas(s, 'resultado', 9);
}

// ===================================================================== 10 ====
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Resultados' });
  s.addText(SLIDES[9].titulo, { placeholder: 'title' });
  const A = D.principal.A, B = D.principal.B;
  const w3 = (LARG - 2 * 0.22) / 3;
  const cards = [
    [sg(A[3].efeito) + ' p.p.', 'saída do emprego', 'exposição × pós'],
    [sg(A[5].efeito) + ' p.p.', 'de formal para informal', 'exposição × pós'],
    [sg(B[5].efeito) + ' p.p.', 'de formal para informal', 'teletrabalhabilidade × pós (painel B)'],
  ];
  cards.forEach(([n, t, d], i) => {
    const x = L + i * (w3 + 0.22);
    cartao(s, x, 1.55, w3, 1.8, [], 'Efeito ' + (i + 1));
    s.addText(n, { x: x + 0.2, y: 1.65, w: w3 - 0.4, h: 0.8, fontFace: '+mj-lt', fontSize: 38, bold: true, color: i === 2 ? C.accent3 : C.accent1, margin: 0, isTextBox: true, objectName: 'Valor ' + (i + 1) });
    s.addText([{ text: t, options: { bold: true, breakLine: true } }, { text: d, options: { fontSize: 14, color: C.accent6 } }], { x: x + 0.2, y: 2.48, w: w3 - 0.4, h: 0.8, fontSize: 17, color: C.text1, margin: 0, valign: 'top', isTextBox: true, objectName: 'Texto ' + (i + 1) });
  });
  cartao(s, L, 3.6, 7.75, 1.75, [
    { text: 'Teste de atrito', options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true } },
    { text: `Pareamento: ${sg(A[4].efeito, 3)} p.p., p = 0,064. `, options: { bold: true, fontSize: 16 } },
    { text: 'Não rejeita a estabilidade do gradiente de pareamento, mas o resultado está perto do limiar e o sinal é negativo. A seleção longitudinal não está descartada.', options: { fontSize: 15 } },
  ], 'Teste de atrito', { margin: [0.14, 0.25, 0.1, 0.25] });
  cartao(s, L + 7.75 + 0.22, 3.6, LARG - 7.75 - 0.22, 1.75, [
    { text: 'Como ler', options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true } },
    { text: 'Compatível com o ramo de Autor e Thompson (2025) em que o vínculo se preserva e o ajuste recai sobre o rendimento, que esta pesquisa não observa. Compatibilidade não é teste.', options: { fontSize: 15 } },
  ], 'Como ler', { margin: [0.14, 0.25, 0.1, 0.25] });
  s.addText('Maior exposição se associa a menos saída do emprego e a menos informalização: o sinal oposto ao da leitura alarmista.', { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y: 5.6, w: LARG, h: 0.85, fill: { color: C.accent2 }, line: { type: 'none' }, fontSize: 19, bold: true, color: C.background1, margin: [0.1, 0.3, 0.1, 0.3], valign: 'middle', objectName: 'Síntese' });
  fonte(s, 'Fonte: elaboração própria a partir da PNADC/IBGE. Efeitos em pontos percentuais por unidade do índice.');
  notas(s, 'vinculo', 10);
}

// ===================================================================== 11 ====
pres.addSection({ title: 'Conclusão' });
{
  const s = pres.addSlide({ masterName: 'CONTEUDO', sectionTitle: 'Conclusão' });
  s.addText(SLIDES[10].titulo, { placeholder: 'title' });
  const wc = (LARG - 0.3) / 2;
  const colunas = [
    ['✓', C.accent1, 'O que os resultados sustentam', [
      'Aumento generalizado das taxas medidas de rotatividade ocupacional, em todas as faixas de exposição.',
      'Gradiente condicional detectável: +2,19 p.p. por unidade de AIOE na transição para ocupação menos exposta.',
      'Nas margens de vínculo, sinal oposto ao da leitura alarmista.',
    ]],
    ['✕', C.accent6, 'O que não sustentam', [
      'Efeito causal: cenário único, sem estudo de evento nem teste de tendências pré-marco.',
      'Adoção de IA: o tratamento é exposição potencial, num marco único e nacional.',
      'Estabilidade da medida: a mudança de ocupação (3 dígitos) cai de 30,0% em 2019T4 para 15,3% em 2020T1 e volta a 34,3% em 2021T4.',
      'Seleção longitudinal e horizonte maior que um trimestre.',
    ]],
  ];
  colunas.forEach(([icone, cor, titulo, itens], i) => {
    const x = L + i * (wc + 0.3);
    cartao(s, x, 1.55, wc, 5.0, [], 'Coluna: ' + titulo);
    disco(s, x + 0.25, 1.78, 0.6, icone, cor, C.background1, 'Marca: ' + titulo, 20);
    s.addText(titulo, { x: x + 1.05, y: 1.78, w: wc - 1.3, h: 0.6, fontSize: 20, bold: true, color: C.text2, valign: 'middle', margin: 0, isTextBox: true, objectName: 'Título: ' + titulo });
    s.addText(itens.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < itens.length - 1, paraSpaceAfter: 12 } })), { x: x + 0.3, y: 2.6, w: wc - 0.6, h: 3.85, fontSize: 18, color: C.text1, valign: 'top', margin: 0, isTextBox: true, objectName: 'Itens: ' + titulo });
  });
  notas(s, 'limites', 11);
}

// ===================================================================== 12 ====
{
  const s = pres.addSlide({ masterName: 'FECHO', sectionTitle: 'Conclusão' });
  s.addText(SLIDES[11].titulo, { placeholder: 'title' });
  const niveis = [
    ['✓', C.accent3, 'Descritivo', 'A mobilidade subiu para todos, e não só para os mais expostos.'],
    ['✓', C.accent3, 'Associação condicional', 'Gradiente detectável, da ordem de 2 p.p. por unidade de AIOE. Vínculo sem deterioração.'],
    ['✕', C.accent5, 'Causal', 'O desenho atual não sustenta a afirmação.'],
  ];
  rotulo(s, 'TRÊS NÍVEIS DE RESPOSTA', L, 1.5, 5.6, C.accent4);
  niveis.forEach(([ic, cor, t, d], i) => {
    const y = 1.9 + i * 1.38;
    s.addText('', { shape: pres.ShapeType.roundRect, rectRadius: 0.1, x: L, y, w: 5.75, h: 1.25, fill: { color: C.accent1, transparency: 35 }, line: { type: 'none' }, objectName: 'Nível: ' + t });
    disco(s, L + 0.2, y + 0.325, 0.6, ic, cor, C.text2, 'Marca: ' + t, 20);
    s.addText([{ text: t, options: { bold: true, fontSize: 18, color: C.background1, breakLine: true } }, { text: d, options: { fontSize: 14, color: C.accent4 } }], { x: L + 1.0, y: y + 0.1, w: 4.6, h: 1.05, valign: 'middle', margin: 0, isTextBox: true, objectName: 'Texto: ' + t });
  });
  const xr = 6.8, wr = R - xr;
  rotulo(s, 'AGENDA, EM ORDEM DE PRIORIDADE', xr, 1.5, wr, C.accent4);
  const agenda = [
    'Tratar a quebra de medida de 2020 e 2021 e definir a janela homogênea',
    'Estudo de evento e teste de tendências anteriores ao marco',
    'Bateria de sensibilidade: janelas, agrupamento, tendência por exposição',
    'Medida específica para modelos de linguagem e placebo com teletrabalho',
    'Tendências não paralelas e estimadores para tratamento contínuo',
  ];
  agenda.forEach((t, i) => {
    const y = 1.9 + i * 0.84;
    disco(s, xr, y + 0.06, 0.5, String(i + 1), C.accent4, C.text2, 'Passo ' + (i + 1), 16);
    s.addText(t, { x: xr + 0.7, y, w: wr - 0.7, h: 0.66, fontSize: 15, color: C.background1, valign: 'middle', margin: 0, isTextBox: true, objectName: 'Passo ' + (i + 1) + ' (texto)' });
  });
  s.addText('Extensões, por último: rendimentos, dimensão regional e margem de entrada no mercado de trabalho.', { x: xr, y: 6.12, w: wr, h: 0.5, fontSize: 13, italic: true, color: C.accent4, margin: 0, isTextBox: true, objectName: 'Extensões' });
  s.addText('Obrigado. Perguntas?', { x: L, y: 6.2, w: 5.75, h: 0.6, fontFace: '+mj-lt', fontSize: 28, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: 'Agradecimento' });
  notas(s, 'conclusao', 12);
}

// ----------------------------------------------------------------- gravação ----
(async () => {
  await pres.writeFile({ fileName: ARQUIVO });
  await applyTheme(ARQUIVO, THEME);
  console.log('gerado:', ARQUIVO, `(${(fs.statSync(ARQUIVO).size / 1024).toFixed(0)} KB, ${SLIDES.length} slides)`);
  console.log(`ritmo adotado nas notas: ${RITMO_PALAVRAS_POR_MINUTO} palavras/min; ${mmss(relogio)} reservados`);
})();
