// Gera roteiro.md: o texto falado de cada slide, com o relógio de 15 minutos.
//
//   node gerar_roteiro.js
//
// Usa o mesmo conteudo.js das notas do PowerPoint, então roteiro e slides não
// se desencontram. As referências saem de dissertacao/referencias.bib.
const fs = require('fs');
const path = require('path');
const { SLIDES, RITMO_PALAVRAS_POR_MINUTO } = require('./conteudo.js');

const palavras = t => (t.match(/[\p{L}\p{N}][\p{L}\p{N}.,%\-]*/gu) || []).length;
const mmss = s => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const porSegundo = RITMO_PALAVRAS_POR_MINUTO / 60;

// Referências citadas nos slides, conforme dissertacao/referencias.bib.
const REFERENCIAS = [
  'ACEMOGLU, D.; RESTREPO, P. Robots and jobs. Journal of Political Economy, v. 128, n. 6, p. 2188–2244, 2020. DOI 10.1086/705716.',
  'AUTOR, D.; THOMPSON, N. Expertise. Journal of the European Economic Association, v. 23, n. 4, p. 1203–1271, 2025. DOI 10.1093/jeea/jvaf023.',
  'BRYNJOLFSSON, E.; LI, D.; RAYMOND, L. Generative AI at work. The Quarterly Journal of Economics, v. 140, n. 2, p. 889–942, 2025. DOI 10.1093/qje/qjae044.',
  'DINGEL, J. I.; NEIMAN, B. How many jobs can be done at home? Journal of Public Economics, v. 189, p. 104235, 2020. DOI 10.1016/j.jpubeco.2020.104235.',
  'ELOUNDOU, T.; MANNING, S.; MISHKIN, P.; ROCK, D. GPTs are GPTs: labor market impact potential of LLMs. Science, v. 384, n. 6702, p. 1306–1308, 2024. DOI 10.1126/science.adj0998.',
  'FELTEN, E. W.; RAJ, M.; SEAMANS, R. Occupational, industry, and geographic exposure to artificial intelligence: a novel dataset and its potential uses. Strategic Management Journal, v. 42, n. 12, p. 2195–2217, 2021. DOI 10.1002/smj.3286.',
  'HUMLUM, A.; VESTERGAARD, E. Still waters, rapid currents: early labor market transformation under generative AI. NBER Working Paper 33777. Cambridge, MA: National Bureau of Economic Research, 2025. Disponível em: https://www.nber.org/papers/w33777.',
  'MEGHIR, C.; NARITA, R.; ROBIN, J.-M. Wages and informality in developing countries. American Economic Review, v. 105, n. 4, p. 1509–1546, 2015. DOI 10.1257/aer.20121110.',
  'ULYSSEA, G. Informality: causes and consequences for development. Annual Review of Economics, v. 12, p. 525–546, 2020. DOI 10.1146/annurev-economics-082119-121914.',
];

let relogio = 0, falado = 0;
const linhasTabela = [], blocos = [];
SLIDES.forEach((s, i) => {
  const n = palavras(s.leitura), fala = n / porSegundo;
  relogio += s.segundos; falado += fala;
  const titulo = i === 0 ? 'Abertura' : s.titulo;
  linhasTabela.push(`| ${i + 1} | ${titulo} | ${mmss(s.segundos)} | ${mmss(relogio)} | ${n} |`);
  blocos.push(
`## Slide ${i + 1} · ${titulo}

> **Tempo:** ${mmss(s.segundos)} · **Ao terminar, o relógio marca:** ${mmss(relogio)}

${s.leitura}
`);
});

const md =
`# Roteiro de fala · apresentação da dissertação

**Exposição ocupacional à inteligência artificial e transições no mercado de trabalho brasileiro**

Duração: **15 minutos exatos**, em 12 slides. O mesmo texto está nas notas do orador de cada slide do arquivo
\`apresentacao_dissertacao.pptx\` (no PowerPoint, modo Apresentador).

## Como usar

- O texto foi calibrado para **${RITMO_PALAVRAS_POR_MINUTO} palavras por minuto**, um ritmo tranquilo de exposição acadêmica. Somadas, as leituras
  ocupam cerca de **${mmss(falado)}**, o que deixa uma folga curta para pausas e para a troca de slides.
- A coluna **Relógio** da tabela é o ponto de controle: ao terminar cada slide, o cronômetro deve marcar aquele tempo. Se
  estiver adiantado, respire e deixe o gráfico falar; se estiver atrasado, corte primeiro as ressalvas já ditas
  (o slide 9 e o slide 11 têm margem para isso).
- Ensaie com cronômetro. O ritmo de cada pessoa varia, e a estimativa acima é só um ponto de partida.

## Quadro de tempo

| Slide | Título | Tempo | Relógio | Palavras |
| ---: | --- | ---: | ---: | ---: |
${linhasTabela.join('\n')}
| | **Total** | **${mmss(relogio)}** | | **${SLIDES.reduce((a, s) => a + palavras(s.leitura), 0)}** |

${blocos.join('\n')}
## Referências citadas nos slides

${REFERENCIAS.map(r => '- ' + r).join('\n')}

As demais referências da dissertação ficam no arquivo \`dissertacao/referencias.bib\`.
`;

fs.writeFileSync(path.join(__dirname, 'roteiro.md'), md, 'utf8');
console.log(`roteiro.md gerado: ${SLIDES.length} slides, ${mmss(relogio)} reservados, fala estimada ${mmss(falado)}`);
