// Barra de trilha no topo do painel, com botao para desligar.
//
// A gravacao nao e embutida no arquivo: o que entra e o player oficial, servido
// pelo proprio detentor dos direitos. Para trocar a faixa, mude FONTE abaixo.
// Um embed do Spotify tambem funciona aqui: basta trocar o bloco do iframe por
// <iframe src="https://open.spotify.com/embed/album/ID" ...></iframe> e apagar o
// script do YouTube, lembrando que o Spotify nao toca sozinho e, sem conta
// conectada, reproduz apenas trechos de 30 segundos.
module.exports = function music(html) {
  const VIDEO = 'kVvhHgWwgWA';          // Skank - E Uma Partida de Futebol, audio oficial
  const TITULO = 'É Uma Partida de Futebol';
  const ARTISTA = 'Skank · áudio oficial';

  const barra = '<div class="trilha" id="trilha">' +
    '<div class="trilha-info"><span class="trilha-kicker">TRILHA DA PARTIDA</span>' +
    '<b>' + TITULO + '</b><span class="trilha-art">' + ARTISTA + '</span></div>' +
    '<div class="trilha-acoes">' +
    '<button type="button" id="trilhaPlay">▶ Tocar música</button>' +
    '<button type="button" id="trilhaOff" aria-label="Desligar a música e fechar a barra">Desligar</button>' +
    '<a href="https://www.youtube.com/watch?v=' + VIDEO + '" target="_blank" rel="noopener noreferrer">Ouvir no canal oficial ↗</a>' +
    '</div><p class="trilha-status" id="trilhaStatus" role="status"></p>' +
    '<div class="trilha-player"><div id="trilhaFrame"></div></div></div>';

  if (!html.includes('</header>')) throw Error('Cabeçalho não encontrado para a trilha');
  html = html.replace('</header>', '</header>\n' + barra);

  html = html.replace('</style>',
    '.trilha{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;max-width:1240px;margin:14px auto 0;' +
    'padding:13px 18px;border:1px solid #42664d;border-radius:10px;background:linear-gradient(120deg,#183d29,#101f18)}' +
    '.trilha-info{display:flex;flex-direction:column;gap:2px;min-width:200px}' +
    '.trilha-kicker{font:600 10px var(--body);letter-spacing:2px;color:#d7fe61}' +
    '.trilha-info b{font-size:17px;color:#f1f7ea;line-height:1.2}' +
    '.trilha-art{font:13px var(--body);color:#b9cfbe}' +
    '.trilha-acoes{display:flex;align-items:center;gap:10px;flex-wrap:wrap}' +
    '.trilha-acoes button{padding:9px 15px;border:0;border-radius:6px;cursor:pointer;font:700 13px var(--body)}' +
    '#trilhaPlay{background:#d7fe61;color:#14251a}' +
    '#trilhaOff{background:transparent;color:#cfe0cf;border:1px solid #577a5e}' +
    '#trilhaOff:hover{border-color:#d7fe61;color:#d7fe61}' +
    '.trilha-acoes a{font:13px var(--body);color:#d7fe61}' +
    '.trilha-status{flex-basis:100%;margin:0;font:12px var(--body);color:#a8c0ad;min-height:15px}' +
    '.trilha-player{width:0;height:0;overflow:hidden}' +
    '.trilha-player.aberto{width:300px;height:170px;border-radius:8px;overflow:hidden;background:#07130c}' +
    '.trilha-player iframe{width:100%;height:100%;border:0}' +
    '@media(max-width:700px){.trilha{margin:12px 16px 0}.trilha-player.aberto{width:100%;height:190px}}' +
    '</style>');

  const script = String.raw`<script>
(()=>{
 const barra=document.getElementById('trilha'),botao=document.getElementById('trilhaPlay'),
       desliga=document.getElementById('trilhaOff'),aviso=document.getElementById('trilhaStatus'),
       caixa=document.querySelector('.trilha-player');
 let player,pronto=false,carregando=false,falhou=false;
 const diz=t=>{aviso.textContent=t;};
 function cria(){
  player=new YT.Player('trilhaFrame',{width:'300',height:'170',videoId:'VIDEO_ID',
   playerVars:{playsinline:1,controls:1,rel:0},
   events:{
    onReady:()=>{pronto=true;player.setVolume(30);caixa.classList.add('aberto');player.playVideo();
      diz('Se não começar sozinho, o navegador está bloqueando o som: clique em Tocar música.');},
    onStateChange:e=>{const tocando=e.data===1;botao.textContent=tocando?'⏸ Pausar música':'▶ Tocar música';
      if(tocando&&document.hidden){player.pauseVideo();return;}
      if(tocando)diz('Tocando · TITULO_MUS');else if(e.data===2)diz('Música pausada.');
      else if(e.data===0)diz('A música terminou. Clique em Tocar música para ouvir de novo.');},
    onError:()=>{falhou=true;caixa.classList.remove('aberto');
      diz('O player não carregou aqui. Abrindo o HTML direto do disco isso é comum: use Ouvir no canal oficial.');}
   }});
 }
 function carrega(){
  if(carregando)return;carregando=true;diz('Carregando o player oficial…');
  if(window.YT&&YT.Player){cria();return;}
  window.onYouTubeIframeAPIReady=cria;
  const api=document.createElement('script');api.src='https://www.youtube.com/iframe_api';
  api.onerror=()=>{carregando=false;diz('Sem internet para tocar a música. Use Ouvir no canal oficial.');};
  document.head.appendChild(api);
 }
 botao.onclick=()=>{
  if(falhou){window.open('https://www.youtube.com/watch?v=VIDEO_ID','_blank','noopener,noreferrer');return;}
  if(!pronto){carrega();return;}
  if(player.getPlayerState()===1)player.pauseVideo();else player.playVideo();
 };
 desliga.onclick=()=>{try{if(pronto)player.stopVideo();}catch(_){}barra.remove();};
 document.addEventListener('visibilitychange',()=>{
  if(document.hidden&&pronto&&player.getPlayerState()===1)player.pauseVideo();});
 carrega();
})();
</script>`.split('VIDEO_ID').join(VIDEO).split('TITULO_MUS').join(TITULO);

  return html.replace('</body>', script + '</body>');
};
