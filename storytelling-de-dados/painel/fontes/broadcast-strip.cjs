// Faixa "O jogo será transmitido", no lugar do ícone do cartão amarelo.
//
// Os logotipos vieram do próprio autor do painel, em assets/logos/, e dão o
// clima de transmissão esportiva. Numa primeira versão a faixa trazia o rótulo
// "Referências visuais" e um aviso de que as marcas não transmitem nem apoiam o
// projeto; o autor pediu para tirar os dois. O aviso que morava na caixa
// ("exposição não indica risco individual de demissão") continua no mesmo
// lugar, logo abaixo da faixa.
const fs = require('fs');
const path = require('path');

module.exports = function strip(html) {
  // arquivo, nome para o texto alternativo, cor de fundo do próprio PNG
  const LOGOS = [
    ['cazetv.png',  'Logotipo da CazéTV',  '#fff'],
    ['globo.png',   'Logotipo da Globo',   '#fff'],
    ['sportv.png',  'Logotipo do sportv',  '#f5f5f5'],
    ['espn.png',    'Logotipo da ESPN',    '#fff'],
    ['youtube.png', 'Logotipo do YouTube', '#fff'],
  ];
  const uri = f => 'data:image/png;base64,' +
    fs.readFileSync(path.join(__dirname, 'assets', 'logos', f)).toString('base64');

  const tiles = LOGOS.map(([f, alt, fundo]) =>
    '<li style="background:' + fundo + '"><img src="' + uri(f) + '" alt="' + alt + '" height="56"></li>').join('');

  const faixa = '<div class="faixa-tv">' +
    '<span class="faixa-tv-rot">O jogo será transmitido</span>' +
    '<ul class="faixa-tv-logos">' + tiles + '</ul>' +
    '</div>';

  const cartao = '<div class="cartao" aria-hidden="true"></div>';
  if (!html.includes(cartao)) throw Error('Cartão amarelo não encontrado');
  html = html.replace(cartao, faixa);

  const caixa = '<div class="regra">';
  if (!html.includes(caixa)) throw Error('Caixa da pergunta do jogo não encontrada');
  html = html.replace(caixa, '<div class="regra regra-tv">');

  if (!html.includes('</style>')) throw Error('Fim do style não encontrado');
  html = html.replace('</style>',
    // a caixa passa de linha para coluna: faixa em cima, aviso embaixo
    '.regra.regra-tv{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:16px!important}' +
    '.faixa-tv{display:flex;flex-wrap:wrap;align-items:center;gap:12px 22px;padding:12px 16px;border-radius:8px;' +
      'background:linear-gradient(90deg,#0b1712,#13291e);border-left:4px solid #d7fe61}' +
    '.faixa-tv-rot{font:700 13px var(--body);letter-spacing:1.8px;text-transform:uppercase;color:#d7fe61}' +
    '.faixa-tv-logos{display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0;list-style:none}' +
    '.faixa-tv-logos li{display:flex;border-radius:8px;overflow:hidden;border:1px solid #ffffff2e}' +
    '.faixa-tv-logos img{display:block;height:56px;width:auto}' +
    '</style>');
  return html;
};
