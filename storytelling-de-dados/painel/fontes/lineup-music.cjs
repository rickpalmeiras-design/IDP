module.exports=function music(html){
const card='<aside class="lineup-music" aria-label="Trilha da escalação"><div><span class="music-kicker">TRILHA DA ESCALAÇÃO</span><h3>É Uma Partida de Futebol</h3><p>Skank · áudio oficial</p><button type="button" id="musicToggle">Tocar música</button><p id="musicStatus" role="status">A música entra quando você chega à escalação. Se necessário, toque no botão para começar.</p><a href="https://www.youtube.com/watch?v=kVvhHgWwgWA" target="_blank" rel="noopener noreferrer">Ouvir no canal oficial ↗</a></div><div class="music-video"><div id="lineupPlayer"></div></div></aside>';
if(!html.includes('<div class="escalacao" id="escalacaoGrid">'))throw Error('Escalação não encontrada');
html=html.replace('<div class="escalacao" id="escalacaoGrid">',card+'<div class="escalacao" id="escalacaoGrid">');
html=html.replace('</style>','.lineup-music{display:grid;grid-template-columns:1fr minmax(260px,360px);gap:24px;align-items:center;margin:24px 0;padding:24px;border:1px solid #42664d;border-radius:12px;background:linear-gradient(120deg,#183d29,#102019)}.music-kicker{font:11px var(--body);letter-spacing:2px;color:#d7fe61}.lineup-music h3{margin:8px 0;font-size:30px;line-height:1.15}.lineup-music p{font:14px/1.5 var(--body);color:#bdd0c2;margin:7px 0}.lineup-music button{padding:10px 18px;margin:10px 0;border:0;border-radius:6px;background:#d7fe61;color:#14251a;cursor:pointer;font-weight:700}.lineup-music a{font:13px var(--body);color:#d7fe61}.music-video{width:100%;height:203px;background:#07130c;border-radius:8px;overflow:hidden}.music-video iframe{width:100%;height:100%;border:0}@media(max-width:650px){.lineup-music{grid-template-columns:1fr;padding:18px;gap:15px}.lineup-music h3{font-size:26px}.music-video{height:220px}}'+'</style>');
const script=String.raw`<script>
(()=>{
 const section=document.getElementById('escalacao'),button=document.getElementById('musicToggle'),status=document.getElementById('musicStatus');
 let player,ready=false,visible=false,loading=false,userPaused=false,attempted=false,failed=false;
 function message(text){status.textContent=text;}
 function play(){if(!ready)return;userPaused=false;player.playVideo();message('Se a música não começar, clique em Tocar música ou use o player.');}
 function load(){
  if(loading)return;loading=true;
  const create=()=>{player=new YT.Player('lineupPlayer',{width:'360',height:'203',videoId:'kVvhHgWwgWA',playerVars:{playsinline:1,controls:1,rel:0},events:{
   onReady:()=>{ready=true;document.getElementById('lineupPlayer').title='Skank — É Uma Partida de Futebol, áudio oficial';player.setVolume(35);if(visible&&!userPaused){attempted=true;play();}},
   onStateChange:e=>{const playing=e.data===1;button.textContent=playing?'Pausar música':'Tocar música';button.setAttribute('aria-label',button.textContent);if(playing){if(!visible||document.hidden){player.pauseVideo();return;}message('Tocando · Skank — É Uma Partida de Futebol');}else if(e.data===2){message('Música pausada.');}else if(e.data===0){userPaused=true;message('A música terminou. Clique para ouvir novamente.');}},
   onAutoplayBlocked:()=>message('Clique em Tocar música para liberar o som.'),
   onError:()=>{failed=true;message('O YouTube não conseguiu tocar aqui. Use Ouvir no canal oficial; arquivos HTML locais podem bloquear o player.');}
  }});};
  if(window.YT&&YT.Player){create();return;}
  window.onYouTubeIframeAPIReady=create;
  const api=document.createElement('script');api.src='https://www.youtube.com/iframe_api';api.onerror=()=>{loading=false;message('Conecte-se à internet para ouvir a música ou abra o canal oficial.');};document.head.appendChild(api);
 }
 button.onclick=()=>{if(failed){window.open('https://www.youtube.com/watch?v=kVvhHgWwgWA','_blank','noopener,noreferrer');return;}if(!ready){userPaused=false;load();message('Carregando o player oficial…');return;}if(player.getPlayerState()===1){userPaused=true;player.pauseVideo();}else{play();}};
 new IntersectionObserver(entries=>{for(const entry of entries){visible=entry.isIntersecting;if(visible){load();if(ready&&!attempted&&!userPaused){attempted=true;play();}}else if(ready&&player.getPlayerState()===1){player.pauseVideo();}}},{threshold:0,rootMargin:'-15% 0px -15% 0px'}).observe(section);
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&ready&&player.getPlayerState()===1)player.pauseVideo();});
})();
</script>`;
return html.replace('</body>',script+'</body>');
};
