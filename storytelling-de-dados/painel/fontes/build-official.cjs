const fs=require('fs'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const rotulo='storytelling-de-dados/dados/dashboard_data.json';
const source=require('path').resolve(__dirname,'../../dados/dashboard_data.json');
const raw=fs.readFileSync(source,'utf8').replace(/^\uFEFF/,'');const data=JSON.parse(raw);
assert.equal(data.meta.n_transicoes,data.destino_por_quartil.reduce((s,r)=>s+r.n_obs,0));
for(const r of data.destino_por_quartil){const sum=['Mesmo grupo','Outro grupo','Desocupado','Fora da força'].reduce((s,k)=>s+r[k],0);assert(Math.abs(sum-100)<.05);}
assert.equal(data.destino_por_quartil.find(r=>r.q==='Q4'&&r.periodo==='pós')['Outro grupo'],25.34);
assert.equal(data.destino_por_quartil.find(r=>r.q==='Q1'&&r.periodo==='pós')['Outro grupo'],20.06);
let html=fs.readFileSync(__dirname+'/classico_matchday.html','utf8');
// Troca que acusa quando nao encontra. Um replace calado deixa o painel sair
// sem o codigo que deveria ter entrado, e nada no build denuncia.
let nTroca = 0;
function troca(alvo, novo) {
  nTroca++;
  const achou = alvo instanceof RegExp ? alvo.test(html) : html.includes(alvo);
  assert(achou, 'troca ' + nTroca + ': nao encontrei o alvo:\n' + String(alvo).slice(0, 120));
  const antes = html.length;
  html = html.replace(alvo, novo);
  assert(html.length !== antes || alvo === novo, 'a troca nao mudou nada: ' + String(alvo).slice(0, 60));
}
troca('<title>Clássico da IA · Matchday</title>','<title>Clássico da IA · Matchday · Dados oficiais</title>');
troca('<script id="dados-embutidos" type="application/json"></script>','<script id="dados-embutidos" type="application/json">\n'+raw.replace(/</g,'\\u003c')+'\n</script>');
// Remove synthetic data generation altogether; failed loading must never fall back to a demo.
const demoStart=html.indexOf('function demo() {'),demoEnd=html.indexOf('/* ======================= render',demoStart);
assert(demoStart>0&&demoEnd>demoStart);html=html.slice(0,demoStart)+html.slice(demoEnd);
troca(/if \(!inicial\) \{ try \{ const s = localStorage[\s\S]*?\}\s*catch\(_\) \{ inicial = null; \} \}/,'');
troca('render(inicial || demo(), !!inicial);','if(inicial){render(inicial,true);}else{$("dataMsg").textContent="Erro ao ler os dados oficiais embutidos. Carregue o JSON do projeto.";}');
troca('PÓS / FLUXOS ILUSTRATIVOS','PÓS / DADOS DO PROJETO');
troca('Dados ilustrativos: carregue o dashboard_data.json para ver o painel real.','Dados oficiais do projeto · carregando…');
troca('EDIÇÃO EXPERIMENTAL','DADOS DO PROJETO');
troca('<div class="databar" id="databar"','<div class="databar real" id="databar"');
troca('Arquivo carregado: ${Number((d.meta||{}).n_transicoes||0).toLocaleString("pt-BR")} transições.','Dados do projeto: ${Number((d.meta||{}).n_transicoes||0).toLocaleString("pt-BR")} transições nas médias · ${(d.meta||{}).janela||""}.');
troca('const bar = $("databar");','$("liveLabel").textContent="PÓS / FLUXOS DO ARQUIVO";\n  const bar = $("databar");');
troca('Se já vinham se afastando antes, a diferença não é culpa da IA.','Se já vinham se afastando antes, a comparação exige investigação adicional.');
troca('<div class="duelo">','<p class="lede" style="font-size:14px;margin:16px 0">Recorte das médias: 2020T1 a 2021T3 ficam de fora por mudança no modo de coleta; 2022T4 também é excluído. O pós começa em 2023T1. Taxas ponderadas pelo peso da origem.</p><div class="duelo">');
troca('  <section id="var">','  <p class="lede" style="font-size:14px;margin-top:18px"><strong>Direção da exposição:</strong> a mudança é entre quartis. Q4 não tem quartil acima e Q1 não tem quartil abaixo: parte do resultado é mecânica. Menor exposição não significa emprego pior.</p>\n  <section id="var">');
troca('<p id="rodapeDados"></p>','<p id="rodapeDados"></p><details class="official-audit"><summary>Procedência e alertas da auditoria</summary><div id="officialAudit"></div></details>');
const chartStart=html.indexOf('function varChart() {'),chartEnd=html.indexOf('document.querySelectorAll(".seg button")',chartStart);
assert(chartStart>0&&chartEnd>chartStart);
html=html.slice(0,chartStart)+`function varChart(anima) {
 const E=DATA.serie_q1_q4||[], QM=qMax(), svg=$("grafVar"), ord=s=>Number(s.slice(0,4))*4+Number(s.slice(-1))-1;
 const tris=[...new Set(E.map(r=>r.tri_lbl))].sort(); if(!tris.length){svg.innerHTML='<text x="450" y="180" fill="#ccc" text-anchor="middle">Série não disponível.</text>';$("veredito").textContent='';return;}
 const vals=E.map(r=>r[metrica]).filter(Number.isFinite),L=48,R=18,T=48,B=46,W=900,H=360;
 const lo=Math.max(0,Math.min(...vals)-(Math.max(...vals)-Math.min(...vals))*.15),hi=Math.max(...vals)+Math.max(.5,(Math.max(...vals)-Math.min(...vals))*.2);
 const tmin=ord(tris[0]),tmax=ord(tris[tris.length-1]),X=t=>L+(t-tmin)/(tmax-tmin||1)*(W-L-R),Y=v=>T+(1-(v-lo)/(hi-lo))*(H-T-B);
 let fundo='';const omitted=new Set(DATA.meta?.trimestres_fora_das_medias||[]);
 for(const t of tris){if(omitted.has(t)){const x1=Math.max(L,X(ord(t)-.5)),x2=Math.min(W-R,X(ord(t)+.5));fundo+='<rect x="'+x1+'" y="'+T+'" width="'+(x2-x1)+'" height="'+(H-T-B)+'" fill="#a9b4ba22"/>';}}
 if(omitted.size)fundo+='<text x="'+L+'" y="20" fill="#c0c7ca" font-size="12">Cinza: trimestres fora das médias pré/pós</text>';
 for(let i=0;i<=4;i++){const v=lo+(hi-lo)*i/4,y=Y(v);fundo+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y+'" y2="'+y+'" stroke="#344237"/><text x="'+(L-8)+'" y="'+(y+4)+'" fill="#b5c2b7" font-size="12" text-anchor="end">'+fmt(v)+'%</text>';}
 tris.forEach(t=>{if(t.endsWith('T1'))fundo+='<text x="'+X(ord(t))+'" y="'+(H-20)+'" fill="#b5c2b7" font-size="12" text-anchor="middle">'+t.slice(0,4)+'</text>';});
 const start=DATA.meta?.pos_inicio||[2023,1],cut=start[0]*4+start[1]-1,xc=X(cut);
 if(xc>=L&&xc<=W-R)fundo+='<line x1="'+xc+'" x2="'+xc+'" y1="'+T+'" y2="'+(H-B)+'" stroke="#d7fe61" stroke-dasharray="6 5"/><text x="'+(xc+6)+'" y="36" fill="#d7fe61" font-size="12">Pós: '+start[0]+'T'+start[1]+'</text>';
 let serie='';
 for(const q of ['Q1',QM]){let path='',last=null,pts='';for(const r of E.filter(r=>r.q===q).sort((a,b)=>ord(a.tri_lbl)-ord(b.tri_lbl))){const v=r[metrica],t=ord(r.tri_lbl);if(!Number.isFinite(v)){last=null;continue;}path+=(last!==null&&t-last===1?'L':'M')+X(t)+' '+Y(v)+' ';last=t;pts+='<circle cx="'+X(t)+'" cy="'+Y(v)+'" r="3" fill="'+(q===QM?'#58df94':'#ff7c8c')+'"><title>'+r.tri_lbl+' · '+q+' · '+fmt(v)+'%</title></circle>';}
 serie+='<path d="'+path+'" fill="none" stroke="'+(q===QM?'#58df94':'#ff7c8c')+'" stroke-width="3" '+(q==='Q1'?'stroke-dasharray="6 3"':'')+'/>'+pts;}
 svg.innerHTML='<defs><clipPath id="varWipe"><rect id="varWipeRect" x="'+L+'" y="0" width="'+(W-L-R+4)+'" height="'+H+'"/></clipPath></defs>'
  +fundo+'<g clip-path="url(#varWipe)">'+serie+'</g>'
  +'<g id="varScan" opacity="0"><line x1="'+L+'" x2="'+L+'" y1="'+T+'" y2="'+(H-B)+'" stroke="#d7fe61" stroke-width="2"/><circle cx="'+L+'" cy="'+(T-9)+'" r="4" fill="#d7fe61"/></g>';
 const col={pct_muda_grupo:'Outro grupo',pct_vai_desocupado:'Desocupado',pct_sai_forca:'Fora da força'}[metrica],A=DATA.destino_por_quartil;
 const pre=pega(A,'pré',QM)[col]-pega(A,'pré','Q1')[col],pos=pega(A,'pós',QM)[col]-pega(A,'pós','Q1')[col];
 vereditoVar(pre,pos,anima);
 if(anima&&!reduz)tocaVar(W-R-L);
}
/* A varredura do VAR: o gráfico é redesenhado da esquerda para a direita e uma
   linha acompanha a revisão. Só roda a pedido e nunca sob movimento reduzido. */
function tocaVar(vao) {
 const rect=document.getElementById('varWipeRect'),scan=document.getElementById('varScan'),dur=950,ease='cubic-bezier(.2,.65,.3,1)';
 try{
  if(rect&&rect.animate){rect.style.transformBox='fill-box';rect.style.transformOrigin='left center';rect.animate([{transform:'scaleX(0)'},{transform:'scaleX(1)'}],{duration:dur,easing:ease});}
  if(scan&&scan.animate)scan.animate([{transform:'translateX(0)',opacity:.95},{transform:'translateX('+vao+'px)',opacity:.95,offset:.82},{transform:'translateX('+vao+'px)',opacity:0}],{duration:dur+250,easing:ease});
 }catch(_){}
}
function vereditoVar(pre,pos,anima) {
 const v=$("veredito");v.replaceChildren();
 const partes=[['Nas médias ponderadas do recorte, a diferença Q4 − Q1 é ',0],[fmt(pre,2)+' p.p.',1],[' no pré e ',0],[fmt(pos,2)+' p.p.',1],[' no pós. A diferença das mudanças é ',0],[fmt(pos-pre,2)+' p.p.',1],[' Esta comparação é descritiva; a inspeção visual não comprova tendências paralelas nem causalidade.',0]];
 for(const par of partes){const el=document.createElement(par[1]?'b':'span');if(par[1])el.className='num';el.textContent=par[0];v.appendChild(el);}
 if(anima&&!reduz&&v.animate){try{v.animate([{opacity:0,transform:'translateY(7px)'},{opacity:1,transform:'none'}],{duration:420,delay:820,easing:'ease-out',fill:'backwards'});}catch(_){}}
}
`+html.slice(chartEnd);
const footStart=html.indexOf('function rodape() {'),footEnd=html.indexOf('\nfunction render(',footStart);
html=html.slice(0,footStart)+`function rodape() {
 const m=DATA.meta||{},a=DATA.auditoria||{};
 $("rodapeDados").textContent='Base: '+(m.base||'não informada')+'. Janela: '+(m.janela||a.trimestres||'não informada')+'. '+Number(m.n_transicoes||0).toLocaleString('pt-BR')+' transições nas médias. Amostra: '+(m.amostra||'não informada')+'.';
 const box=$("officialAudit");box.replaceChildren();
 const source=document.createElement('p');source.textContent='Fonte: '+(m.fonte||'não informada')+'. Dados agregados fornecidos pelo projeto; não foi realizada nova consulta aos microdados.';box.appendChild(source);
 const list=document.createElement('ul');for(const item of a.alertas||[]){const li=document.createElement('li');li.textContent=item;list.appendChild(li);}box.appendChild(list);
 const note=document.createElement('p');note.textContent='Os alertas acima são os registrados no arquivo de origem. A auditoria de identidade não está disponível neste painel agregado. Não há contagens individuais por rota para verificar o limite de 30 observações.';box.appendChild(note);
}
`+html.slice(footEnd);
troca('</style>','.databar.real{background:#175235;color:#fff}.databar.real label{color:#174626;background:#e5f1d5}.official-audit{border:1px solid #526348;padding:15px;border-radius:6px;margin-top:20px}.official-audit summary{cursor:pointer;font-weight:700}.official-audit p,.official-audit li{font-size:14px;line-height:1.6}.var .tela{transition:color .25s}.var .tela.revisando{color:#ff7c8c}.var .tela.revisando::before{background:#ff7c8c}.var-acoes{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 10px}.revar{background:#1c3330;border:1px solid #4b6a5f;color:#eaf3ef;padding:7px 14px;border-radius:999px;cursor:pointer;font:13px var(--body)}.revar:hover{border-color:#d7fe61;color:#d7fe61}.var-dica{font-size:12px;color:#9fb6a9}.seg button{transition:background .18s,color .18s}.veredito .num{color:#d7fe61;font-weight:700;font-variant-numeric:tabular-nums}.var .tela{gap:12px}.arbitro{flex:0 0 auto;align-self:center;transition:filter .3s}.tela.revisando .arbitro{filter:drop-shadow(0 0 12px #d7fe6188)}.revar.rod[aria-pressed="true"]{border-color:#d7fe61;color:#d7fe61}@media (prefers-reduced-motion: reduce){.var .tela::before{animation:none}.revar.rod{display:none}}@media(max-width:600px){.arbitro{width:104px;height:156px}.var-dica{width:100%}}</style>');
const arbitroPng=fs.readFileSync(__dirname+'/assets/referee.png').toString('base64');
const ARBITRO='<img class="arbitro" id="arbitro" width="160" height="240" alt="Representação realista de Anderson Daronco fazendo o sinal do VAR, com os indicadores desenhando um quadrado à frente do peito" src="data:image/png;base64,'+arbitroPng+'">';
troca('<div class="tela">VAR em análise</div>','<div class="tela" id="varTela">'+ARBITRO+'<span class="tela-txt">VAR em análise</span></div>');
troca('<div class="var-scroll">','<div class="var-acoes"><button type="button" id="rodizio" class="revar rod" aria-pressed="false">Rodar sozinho</button><button type="button" id="revar" class="revar">Rever o lance</button><span class="var-dica">O VAR passa pelos três indicadores sozinho. Clique em um deles para assumir o controle.</span></div><div class="var-scroll">');
troca(`document.querySelectorAll(".seg button").forEach(b => b.onclick = () => {
  metrica = b.dataset.m; document.querySelectorAll(".seg button").forEach(x=>x.setAttribute("aria-pressed", x===b?"true":"false")); varChart(); });`,`let varTimer=null;
/* A tela do VAR acompanha a troca de aba: entra em revisao, depois anuncia o
   indicador revisado. Sob movimento reduzido nao ha piscada nem espera. */
function telaVar(estado) {
 const t=document.getElementById("varTela"); if(!t) return;
 const b=document.querySelector('.seg button[aria-pressed="true"]'), nome=b?b.textContent.trim():"";
 t.classList.toggle("revisando", estado==="revisando");
 const txt=t.querySelector(".tela-txt");
 if(txt) txt.textContent = estado==="revisando" ? "Revisando o lance…" : (nome ? "VAR · "+nome : "VAR em análise");
}
function revisar() {
 if(reduz){ varChart(false); telaVar("pronto"); return; }
 telaVar("revisando"); apitaVar(); varChart(true);
 clearTimeout(varTimer); varTimer=setTimeout(()=>telaVar("pronto"),1150);
}
/* O sinal do VAR: o retângulo é redesenhado entre as mãos e os braços sobem. */
function apitaVar() {
 const svg=document.getElementById("arbitro"); if(!svg||reduz) return;
 const box=svg.querySelector(".varbox"),bracos=svg.querySelectorAll(".braco"),per=2*(60+34);
 try{
  if(box&&box.animate){box.style.strokeDasharray=per;box.animate([{strokeDashoffset:per,opacity:.3},{strokeDashoffset:0,opacity:1}],{duration:720,easing:'ease-out'});}
  bracos.forEach(b=>{if(b.animate)b.animate([{transform:'rotate(-7deg) translateY(5px)'},{transform:'rotate(1.5deg) translateY(-2px)'},{transform:'none'}],{duration:660,easing:'ease-out'});});
  if(svg.animate)svg.animate([{transform:'scale(.94)'},{transform:'scale(1)'}],{duration:430,easing:'cubic-bezier(.2,1.5,.5,1)'});
 }catch(_){}
}
/* Rodízio: o VAR passa sozinho pelos três indicadores enquanto a seção está à
   vista e a aba do navegador, aberta. Um clique em qualquer indicador encerra o
   rodízio, porque a partir daí quem escolhe é quem está lendo. */
let rodTimer=null,rodLigado=false,varAVista=false;
function botaoRodizio(){ return document.getElementById("rodizio"); }
function rodizio(liga) {
 rodLigado=liga&&!reduz;
 clearInterval(rodTimer); rodTimer=null;
 const bt=botaoRodizio();
 if(bt){ bt.setAttribute("aria-pressed",String(rodLigado)); bt.textContent=rodLigado?"Pausar rodízio":"Rodar sozinho"; }
 if(rodLigado) rodTimer=setInterval(()=>{ if(document.hidden||!varAVista) return; proximoIndicador(); },6500);
}
function proximoIndicador() {
 const bs=[...document.querySelectorAll(".seg button")]; if(!bs.length) return;
 const atual=bs.findIndex(x=>x.getAttribute("aria-pressed")==="true");
 const b=bs[(atual+1)%bs.length];
 metrica=b.dataset.m;
 bs.forEach(x=>x.setAttribute("aria-pressed", x===b?"true":"false"));
 revisar();
}
document.querySelectorAll(".seg button").forEach(b => b.onclick = () => {
 metrica = b.dataset.m;
 document.querySelectorAll(".seg button").forEach(x=>x.setAttribute("aria-pressed", x===b?"true":"false"));
 rodizio(false);
 revisar();
});
const btRevar=document.getElementById("revar"); if(btRevar) btRevar.onclick=revisar;
const btRod=botaoRodizio(); if(btRod) btRod.onclick=()=>rodizio(!rodLigado);
telaVar("pronto");
/* Na primeira vez que a secao aparece na tela, o VAR revisa sozinho. O grafico
   ja esta desenhado antes disso: a animacao parte de um estado completo. */
if(!reduz && "IntersectionObserver" in window){
 const alvo=document.getElementById("var");
 if(alvo){ let primeira=true;
  const io=new IntersectionObserver(es=>{for(const e of es){ varAVista=e.isIntersecting;
   if(e.isIntersecting&&primeira){ primeira=false; revisar(); rodizio(true); } }},{threshold:.3});
  io.observe(alvo); }
}`);

fs.writeFileSync(__dirname+'/../classico_da_ia.html',html);
const embedded=JSON.parse(html.match(/<script id="dados-embutidos" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.deepStrictEqual(embedded,data);assert(!html.includes('function demo()'));assert(!html.includes('localStorage.getItem'));assert(!html.includes('FLUXOS ILUSTRATIVOS'));
for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)){if(m[0].includes('application/json'))continue;if(m[1].trim())new vm.Script(m[1]);}
const report={source:rotulo,sha256:crypto.createHash('sha256').update(raw).digest('hex'),n_transicoes:data.meta.n_transicoes,rows:Object.fromEntries(['destino_por_quartil','grupo_destino','direcao_exposicao','serie_q1_q4','sankey_pos'].map(k=>[k,data[k].length])),output:'classico_da_ia.html',checks:['Embedded JSON identical to source','No demo generator or stored data fallback','JavaScript syntax valid','Quartile counts sum to metadata','Destination percentages sum to 100% within rounding']};
fs.writeFileSync(__dirname+'/../validacao-dados-oficiais.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
