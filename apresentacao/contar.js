// Confere se as leituras cabem nos 15 minutos.
//
//   node contar.js
//
// Conta as palavras de cada leitura, converte em tempo ao ritmo definido em
// conteudo.js e compara com o tempo reservado ao slide. O total reservado é de
// 900 segundos. A coluna "folga" é o que sobra (+) ou falta (-) em cada slide.
const { SLIDES, RITMO_PALAVRAS_POR_MINUTO } = require('./conteudo.js');

const palavras = t => (t.match(/[\p{L}\p{N}][\p{L}\p{N}.,%\-]*/gu) || []).length;
const mmss = s => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const porSegundo = RITMO_PALAVRAS_POR_MINUTO / 60;

let reservado = 0, falado = 0, relogio = 0;
console.log(`Ritmo: ${RITMO_PALAVRAS_POR_MINUTO} palavras/min\n`);
console.log('slide'.padEnd(12) + 'reservado'.padStart(10) + 'palavras'.padStart(10) + 'alvo'.padStart(7) + 'fala'.padStart(8) + 'folga'.padStart(8) + 'relógio'.padStart(9));
for (const s of SLIDES) {
  const n = palavras(s.leitura);
  const fala = n / porSegundo;
  reservado += s.segundos; falado += fala; relogio += s.segundos;
  console.log(
    s.id.padEnd(12) + mmss(s.segundos).padStart(10) + String(n).padStart(10) +
    String(Math.round(s.segundos * porSegundo)).padStart(7) + mmss(fala).padStart(8) +
    ((s.segundos - fala) >= 0 ? '+' : '-') + String(Math.abs(Math.round(s.segundos - fala))).padStart(2) + 's' +
    mmss(relogio).padStart(8));
}
console.log('-'.repeat(60));
console.log(`TOTAL reservado ${mmss(reservado)} | fala estimada ${mmss(falado)} | diferença ${Math.round(reservado - falado)}s`);
if (reservado !== 900) console.log(`ATENÇÃO: o tempo reservado soma ${reservado}s, e não 900s.`);
