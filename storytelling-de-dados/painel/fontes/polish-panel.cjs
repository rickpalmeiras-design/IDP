module.exports=function polish(html){
 const replace=(a,b)=>{if(!html.includes(a))throw Error('Missing polish target: '+a.slice(0,70));html=html.replace(a,b)};
 replace('O MERCADO<br>ENTRA EM <em>CAMPO.</em>','A IA ENTROU EM JOGO.<em>O TRABALHO MUDOU?</em>');
 replace('De uma ocupação à outra.<br>Acompanhe o movimento de quem trabalha.','Dois times em campo. O Verdão reúne os trabalhadores cujo trabalho mais se parece com o que a IA faz; o Mengão, os que menos se parecem. A pergunta é simples: depois do ChatGPT, quem mudou mais de tipo de trabalho?');
 html=html.replace(/<p class="legenda-placar" id="legendaPlacar">[\s\S]*?<\/p>/,'<p class="legenda-placar" id="legendaPlacar">A partida começa em 0 × 0. Ao longo do jogo, vamos comparar os dois times antes e depois do lançamento do ChatGPT. O placar será revelado no apito final.</p>');
 html=html.replace(/<p><strong>A pergunta do jogo:<\/strong>[\s\S]*?<\/p>/,'<p>A bola vai rolar! Acompanhe o duelo entre os trabalhadores mais e menos expostos à IA e compare o que mudou depois do lançamento do ChatGPT. Fique até o apito final: é lá que você descobre o placar!</p>');
 html=html.replace('Os 10 grandes grupos de profissões do IBGE, cada um com um boneco e exemplos de quem joga ali. No mercado da bola, no início da página, você vê quem troca de posição.','Conheça os dez grandes grupos ocupacionais do IBGE. Os números identificam as posições no campo; os exemplos ajudam a reconhecer cada grupo.');
 html=html.replace('mas o gol só vale depois do VAR','uma diferença descritiva, não um efeito comprovado da IA');
 const start=html.indexOf('function boneco(cod, o = {}) {'), end=html.indexOf('/* ======================= dados ilustrativos',start);
 html=html.slice(0,start)+
 'function boneco(cod, o = {}) {\n'+
 ' if(!o.corre) return \'<span class="position-token" aria-hidden="true">\'+cod+\'</span>\';\n'+
 ' const id=Number(o.athlete)||0,row=Math.floor(id/4),col=id%4;\n'+
 ' return \'<span class="athlete running" aria-hidden="true" style="background-position:\'+col*100/3+\'% \'+row*100+\'%"></span>\';\n}\n\n'+html.slice(end);
 const a=html.indexOf('function fila() {'),b=html.indexOf('function escalacao()',a);
 html=html.slice(0,a)+'function fila() { $("fila").innerHTML=\'<div class="flaco-lead"><img src="assets/flaco-lopez.png" alt="Representação artística de Flaco López em corrida"><span>FLACO LÓPEZ<small>NA LINHA DE FRENTE</small></span></div>\'; }\n\n'+html.slice(b);
 replace('const c = $("campo"); if (c.querySelectorAll(".viajante").length > 16) return;', 'const c = $("campo"); const used=new Set([...c.querySelectorAll(".viajante")].map(e=>Number(e.dataset.athlete))); const available=[0,1,2,3,4,5,6,7].filter(id=>!used.has(id)); if(!available.length || used.size>=5) return; const athlete=available[Math.floor(Math.random()*available.length)];');
 replace('el.className = "viajante"; el.innerHTML = boneco(l.o,{corre:true});','el.className = "viajante"; el.dataset.athlete=athlete; el.innerHTML = boneco(l.o,{corre:true,athlete});');
 replace('i<=16;i++){ const t=i/16','i<=60;i++){ const t=i/60');
 replace('i===0||i===16 ? 0 : 1','i===0||i===60 ? 0 : 1');
 replace('duration:3600/speed,easing:"ease-in-out"','duration:6200/speed,easing:"linear"');
 replace('}, 650/speed);','}, 1450/speed);');
 html=html.replace('inspirados visualmente em Vitor Roque','inspirados visualmente em Flaco López, Vitor Roque');
 html=html.replace('</style>',
 '.matchnav a{color:#dce9db;text-decoration:none}@media(min-width:601px){.match-heading .matchtitle{font-size:clamp(40px,4.4vw,62px)}}.matchtitle em{display:block}.matchtitle br{display:block}.board .time .nome{font-size:clamp(23px,2.2vw,32px)}@media(max-width:600px){.matchtitle{font-size:43px;line-height:1.02;letter-spacing:0}.board .time .nome{font-size:22px}}.lineup-strip{height:210px;overflow:visible;align-items:center}.lineup-strip .fila{position:relative;bottom:auto}.flaco-lead{display:flex;align-items:center;gap:18px}.flaco-lead img{display:block;width:135px;height:205px;object-fit:contain;filter:drop-shadow(0 8px 7px #0005)}.flaco-lead>span{font:24px var(--display);color:#e0ff9a}.flaco-lead small{display:block;font:10px var(--body);letter-spacing:2px;color:#b7cbb9;margin-top:7px}.position-token{display:grid;place-items:center;width:36px;height:36px;margin:auto;border:1px solid #9db88d;border-radius:50%;background:#142d22;color:#e2f2d5;font:600 15px var(--body)}.no .fig{width:36px}.no .fig:after{display:none}.no .fig .position-token{display:grid;width:32px;height:32px;border-radius:50%;padding:0;background:#142d22;font-size:13px}.ficha .fig{display:none}.viajante{width:48px}.athlete.running{animation:softStride .65s ease-in-out infinite;transform-origin:50% 90%}@keyframes softStride{0%,100%{transform:translateY(0) rotate(-.5deg)}50%{transform:translateY(-1.5px) rotate(.5deg)}}@media(max-width:600px){.lineup-strip{height:180px;gap:10px}.flaco-lead img{width:95px;height:170px}.flaco-lead{gap:6px}.flaco-lead>span{font-size:18px}.flaco-lead small{font-size:8px}.lineup-strip>span{max-width:125px;font-size:9px;line-height:1.5}.viajante{width:36px}}@media(prefers-reduced-motion:reduce){.athlete.running{animation:none}}'+ '</style>');
 return html;
};
