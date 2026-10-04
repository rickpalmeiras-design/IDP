// Trilha do painel: um botao na barra do topo, e nada mais.
//
// A gravacao nao e embutida no arquivo. O que entra e o player oficial do
// Spotify, um iframe simples, sem API e sem script externo, que e o que tem mais
// chance de carregar quando o HTML e aberto direto do disco. O player do
// YouTube, usado antes, precisa da IFrame API e recusa a origem file://.
//
// O player so aparece, e so e requisitado ao Spotify, depois que alguem liga a
// musica: o iframe nasce sem src. Ele precisa ficar visivel enquanto toca,
// porque o embed do Spotify nao tem como ser comandado de fora; esconde-lo
// seria o mesmo que desliga-lo.
//
// Para trocar a trilha, mude ALBUM (ou use embed/track/ID para uma faixa so).
module.exports = function music(html) {
  const ALBUM = '1zfrABBjKnIhKIub9UCI1N';   // Shakira No Rio - As Melhores
  const FONTE = 'https://open.spotify.com/embed/album/' + ALBUM + '?utm_source=generator';

  const barra = '<div class="trilha" id="trilha" hidden>' +
    '<iframe id="trilhaFrame" title="Spotify: Waka Waka (This Time for Africa)" data-src="' + FONTE + '" ' +
    'loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">' +
    '</iframe>' +
    '<p class="trilha-status">Waka Waka é a faixa 3 da lista. Aperte o play no player: o Spotify não toca sozinho e, sem conta conectada, reproduz trechos de 30 segundos.</p>' +
    '</div>';

  if (!html.includes('</header>')) throw Error('Cabeçalho não encontrado para a trilha');
  html = html.replace('</header>', '</header>\n' + barra);

  html = html.replace('</style>',
    '.trilha{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;max-width:1240px;' +
    'margin:12px auto 0;padding:12px 18px;border:1px solid #42664d;border-radius:10px;' +
    'background:linear-gradient(120deg,#183d29,#101f18)}' +
    '.trilha iframe{flex:1 1 320px;min-width:260px;max-width:520px;height:152px;border:0;border-radius:10px}' +
    '.trilha-status{flex:1 1 240px;margin:0;font:12px/1.5 var(--body);color:#a8c0ad}' +
    '@media(max-width:700px){.trilha{margin:12px 16px 0}.trilha iframe{min-width:0}}' +
    '</style>');

  const script = String.raw`<script>
(()=>{
 const barra=document.getElementById('trilha'),botao=document.getElementById('musicaToggle'),
       quadro=document.getElementById('trilhaFrame');
 if(!barra||!botao||!quadro)return;
 const fonte=quadro.dataset.src;
 let ligada=false;
 botao.textContent='Ligar música';
 /* Esvaziar o src para o player de verdade. Esconder a barra sem esvaziar
    deixaria o som tocando atras. */
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
