// Barra de trilha no topo do painel, com botao para desligar.
//
// A gravacao nao e embutida no arquivo: o que entra e o player oficial do
// Spotify, servido pelo proprio detentor dos direitos. E um iframe simples, sem
// API e sem script externo, que e o que tem mais chance de carregar quando o
// HTML e aberto direto do disco. O player do YouTube, usado antes, precisa
// carregar a IFrame API e costuma recusar a origem file://.
//
// Para trocar a trilha, mude ALBUM (ou use .../embed/track/ID para uma faixa).
module.exports = function music(html) {
  const ALBUM = '1zfrABBjKnIhKIub9UCI1N';     // Shakira No Rio - As Melhores
  const FAIXA = 'Waka Waka (This Time for Africa)';
  const ARTISTA = 'Shakira · faixa 3 do álbum';
  const LINK = 'https://open.spotify.com/album/' + ALBUM;

  const barra = '<div class="trilha" id="trilha">' +
    '<div class="trilha-info"><span class="trilha-kicker">TRILHA DA PARTIDA</span>' +
    '<b>' + FAIXA + '</b><span class="trilha-art">' + ARTISTA + '</span>' +
    '<a href="' + LINK + '" target="_blank" rel="noopener noreferrer">Abrir no Spotify ↗</a></div>' +
    '<div class="trilha-player"><iframe title="Spotify: ' + FAIXA + '" ' +
    'src="https://open.spotify.com/embed/album/' + ALBUM + '?utm_source=generator" ' +
    'loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">' +
    '</iframe></div>' +
    '<p class="trilha-status" id="trilhaStatus">Aperte o play no player para ouvir. O Spotify não toca sozinho; sem conta conectada, reproduz trechos de 30 segundos. Para desligar, use o botão na barra do topo.</p>' +
    '</div>';

  if (!html.includes('</header>')) throw Error('Cabeçalho não encontrado para a trilha');
  html = html.replace('</header>', '</header>\n' + barra);

  html = html.replace('</style>',
    '.trilha{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;max-width:1240px;margin:14px auto 0;' +
    'padding:14px 18px;border:1px solid #42664d;border-radius:10px;background:linear-gradient(120deg,#183d29,#101f18)}' +
    '.trilha-info{display:flex;flex-direction:column;gap:3px;min-width:210px;flex:1 1 210px}' +
    '.trilha-kicker{font:600 10px var(--body);letter-spacing:2px;color:#d7fe61}' +
    '.trilha-info b{font-size:17px;color:#f1f7ea;line-height:1.2}' +
    '.trilha-art{font:13px var(--body);color:#b9cfbe}' +
    '.trilha-info a{font:13px var(--body);color:#d7fe61;margin-top:3px}' +
    '.trilha-player{flex:1 1 340px;min-width:280px;max-width:520px}' +
    '.trilha-player iframe{width:100%;height:152px;border:0;border-radius:10px}' +
    '#trilhaOff{padding:9px 16px;border:1px solid #577a5e;border-radius:6px;cursor:pointer;' +
    'font:700 13px var(--body);background:transparent;color:#cfe0cf;align-self:center}' +
    '#trilhaOff:hover{border-color:#d7fe61;color:#d7fe61}' +
    '.trilha-status{flex-basis:100%;margin:0;font:12px var(--body);color:#a8c0ad;line-height:1.45}' +
    '@media(max-width:700px){.trilha{margin:12px 16px 0;padding:14px}.trilha-player{min-width:0}}' +
    '</style>');

  const script = String.raw`<script>
(()=>{
 const barra=document.getElementById('trilha'),botao=document.getElementById('musicaToggle'),
       quadro=barra&&barra.querySelector('iframe');
 if(!barra||!botao||!quadro)return;
 const fonte=quadro.src;
 let ligada=true;
 /* Esvaziar o src para o player, e devolve-lo recomeca do zero. Esconder a
    barra sem esvaziar deixaria o som tocando atras. */
 botao.onclick=()=>{
  ligada=!ligada;
  if(ligada){quadro.src=fonte;barra.hidden=false;}
  else{quadro.src='about:blank';barra.hidden=true;}
  botao.textContent=ligada?'Desligar música':'Ligar música';
 };
})();
</script>`;

  return html.replace('</body>', script + '</body>');
};
