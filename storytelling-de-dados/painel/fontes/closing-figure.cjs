// Figura de fecho, abaixo da tabela dos próximos jogos.
//
// A imagem "Em busca do título de mestre" vem do autor do painel. O original
// está em assets/titulo-mestre.png (3 MB); o que entra no HTML é uma versão em
// JPEG de qualidade 90 (0,65 MB), para o arquivo único não passar de 30 MB.
// O lugar da figura é marcado no fonte por <!--FIGURA_FECHO-->.
const fs = require('fs');
const path = require('path');

module.exports = function closing(html) {
  const marca = '<!--FIGURA_FECHO-->';
  if (!html.includes(marca)) throw Error('Marca da figura de fecho não encontrada');

  const b64 = fs.readFileSync(path.join(__dirname, 'assets', 'titulo-mestre.jpg')).toString('base64');
  const alt = 'Imagem de estádio: um jogador de camisa verde do Palmeiras e um de camisa rubro-negra do Flamengo correm lado a lado em direção a um pódio ' +
    'com as taças da Libertadores, do Brasileirão e da Copa do Brasil. No pódio está escrito "Em busca do título de ' +
    'mestre", e um capelo de formatura repousa sobre ele.';
  const figura = '<figure class="fecho"><img src="data:image/jpeg;base64,' + b64 + '" alt="' + alt + '"></figure>';
  html = html.replace(marca, figura);

  if (!html.includes('</style>')) throw Error('Fim do style não encontrado');
  html = html.replace('</style>',
    '.fecho{margin:30px 0 0}' +
    '.fecho img{display:block;width:100%;max-width:1100px;height:auto;margin:0 auto;border-radius:12px;' +
    'border:1px solid #2e5a43;box-shadow:0 14px 40px #0006}' +
    '</style>');
  return html;
};
