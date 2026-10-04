// Trilha do painel: apenas o botao da barra do topo.
//
// Nao ha player dentro da pagina. O embed do Spotify precisava ficar visivel
// para tocar, porque nao pode ser comandado de fora, e com o HTML aberto direto
// do disco ele nem chegava a carregar. O botao abre a musica no proprio Spotify,
// em outra aba, que e onde ela toca de verdade.
//
// A gravacao nao e embutida no arquivo em nenhum momento.
module.exports = function music(html) {
  const ALBUM = '1zfrABBjKnIhKIub9UCI1N';   // Shakira No Rio - As Melhores, Waka Waka e a faixa 3
  const LINK = 'https://open.spotify.com/album/' + ALBUM;

  const script = String.raw`<script>
(()=>{
 const botao=document.getElementById('musicaToggle');
 if(!botao)return;
 botao.title='Abre Waka Waka no Spotify, em outra aba';
 botao.onclick=()=>window.open('LINK_SPOTIFY','_blank','noopener,noreferrer');
})();
</script>`.replace('LINK_SPOTIFY', LINK);

  return html.replace('</body>', script + '</body>');
};
