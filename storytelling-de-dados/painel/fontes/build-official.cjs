const fs=require('fs'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const rotulo='storytelling-de-dados/dados/dashboard_data.json';
const source=require('path').resolve(__dirname,'../../dados/dashboard_data.json');
const raw=fs.readFileSync(source,'utf8').replace(/^\uFEFF/,'');const data=JSON.parse(raw);
assert.equal(data.meta.n_transicoes,data.destino_por_quartil.reduce((s,r)=>s+r.n_obs,0));
for(const r of data.destino_por_quartil){const sum=['Mesmo grupo','Outro grupo','Desocupado','Fora da força'].reduce((s,k)=>s+r[k],0);assert(Math.abs(sum-100)<.05);}
assert.equal(data.destino_por_quartil.find(r=>r.q==='Q4'&&r.periodo==='pós')['Outro grupo'],25.34);
assert.equal(data.destino_por_quartil.find(r=>r.q==='Q1'&&r.periodo==='pós')['Outro grupo'],20.06);
let html=fs.readFileSync(__dirname+'/classico_matchday.html','utf8');
html=html.replace('<title>Clássico da IA · Matchday</title>','<title>Clássico da IA · Matchday · Dados oficiais</title>');
html=html.replace('<script id="dados-embutidos" type="application/json"></script>','<script id="dados-embutidos" type="application/json">\n'+raw.replace(/</g,'\\u003c')+'\n</script>');
// Remove synthetic data generation altogether; failed loading must never fall back to a demo.
const demoStart=html.indexOf('function demo() {'),demoEnd=html.indexOf('/* ======================= render',demoStart);
assert(demoStart>0&&demoEnd>demoStart);html=html.slice(0,demoStart)+html.slice(demoEnd);
html=html.replace(/if \(!inicial\) \{ try \{ const s = localStorage[\s\S]*?\}\s*catch\(_\) \{ inicial = null; \} \}/,'');
html=html.replace('render(inicial || demo(), !!inicial);','if(inicial){render(inicial,true);}else{$("dataMsg").textContent="Erro ao ler os dados oficiais embutidos. Carregue o JSON do projeto.";}');
html=html.replace(/\s*try \{ localStorage\.setItem\([^\n]+\} catch\(_\) \{\}/,'');
html=html.replace('PÓS / FLUXOS ILUSTRATIVOS','PÓS / DADOS DO PROJETO');
html=html.replace('Dados ilustrativos: carregue o dashboard_data.json para ver o painel real.','Dados oficiais do projeto · carregando…');
html=html.replace('EDIÇÃO EXPERIMENTAL','DADOS DO PROJETO');
html=html.replace('<div class="databar" id="databar"','<div class="databar real" id="databar"');
html=html.replace('Arquivo carregado: ${Number((d.meta||{}).n_transicoes||0).toLocaleString("pt-BR")} transições.','Dados do projeto: ${Number((d.meta||{}).n_transicoes||0).toLocaleString("pt-BR")} transições nas médias · ${(d.meta||{}).janela||""}.');
html=html.replace('const bar = $("databar");','$("liveLabel").textContent="PÓS / FLUXOS DO ARQUIVO";\n  const bar = $("databar");');
html=html.replace('Se já vinham se afastando antes, a diferença não é culpa da IA.','Se já vinham se afastando antes, a comparação exige investigação adicional.');
html=html.replace('<div class="duelo">','<p class="lede" style="font-size:14px;margin:16px 0">Recorte das médias: 2020T1 a 2021T3 ficam de fora por mudança no modo de coleta; 2022T4 também é excluído. O pós começa em 2023T1. Taxas ponderadas pelo peso da origem.</p><div class="duelo">');
html=html.replace('  <section id="var">','  <p class="lede" style="font-size:14px;margin-top:18px"><strong>Direção da exposição:</strong> a mudança é entre quartis. Q4 não tem quartil acima e Q1 não tem quartil abaixo: parte do resultado é mecânica. Menor exposição não significa emprego pior.</p>\n  <section id="var">');
html=html.replace('<p id="rodapeDados"></p>','<p id="rodapeDados"></p><details class="official-audit"><summary>Procedência e alertas da auditoria</summary><div id="officialAudit"></div></details>');
const chartStart=html.indexOf('function varChart() {'),chartEnd=html.indexOf('document.querySelectorAll(".seg button")',chartStart);
assert(chartStart>0&&chartEnd>chartStart);
html=html.slice(0,chartStart)+`function varChart() {
 const E=DATA.serie_q1_q4||[], QM=qMax(), svg=$("grafVar"), ord=s=>Number(s.slice(0,4))*4+Number(s.slice(-1))-1;
 const tris=[...new Set(E.map(r=>r.tri_lbl))].sort(); if(!tris.length){svg.innerHTML='<text x="450" y="180" fill="#ccc" text-anchor="middle">Série não disponível.</text>';$("veredito").textContent='';return;}
 const vals=E.map(r=>r[metrica]).filter(Number.isFinite),L=48,R=18,T=48,B=46,W=900,H=360;
 const lo=Math.max(0,Math.min(...vals)-(Math.max(...vals)-Math.min(...vals))*.15),hi=Math.max(...vals)+Math.max(.5,(Math.max(...vals)-Math.min(...vals))*.2);
 const tmin=ord(tris[0]),tmax=ord(tris[tris.length-1]),X=t=>L+(t-tmin)/(tmax-tmin||1)*(W-L-R),Y=v=>T+(1-(v-lo)/(hi-lo))*(H-T-B);
 let h='';const omitted=new Set(DATA.meta?.trimestres_fora_das_medias||[]);
 for(const t of tris){if(omitted.has(t)){const x1=Math.max(L,X(ord(t)-.5)),x2=Math.min(W-R,X(ord(t)+.5));h+='<rect x="'+x1+'" y="'+T+'" width="'+(x2-x1)+'" height="'+(H-T-B)+'" fill="#a9b4ba22"/>';}}
 if(omitted.size)h+='<text x="'+L+'" y="20" fill="#c0c7ca" font-size="12">Cinza: trimestres fora das médias pré/pós</text>';
 for(let i=0;i<=4;i++){const v=lo+(hi-lo)*i/4,y=Y(v);h+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y+'" y2="'+y+'" stroke="#344237"/><text x="'+(L-8)+'" y="'+(y+4)+'" fill="#b5c2b7" font-size="12" text-anchor="end">'+fmt(v)+'%</text>';}
 tris.forEach(t=>{if(t.endsWith('T1'))h+='<text x="'+X(ord(t))+'" y="'+(H-20)+'" fill="#b5c2b7" font-size="12" text-anchor="middle">'+t.slice(0,4)+'</text>';});
 const start=DATA.meta?.pos_inicio||[2023,1],cut=start[0]*4+start[1]-1,xc=X(cut);
 if(xc>=L&&xc<=W-R)h+='<line x1="'+xc+'" x2="'+xc+'" y1="'+T+'" y2="'+(H-B)+'" stroke="#d7fe61" stroke-dasharray="6 5"/><text x="'+(xc+6)+'" y="36" fill="#d7fe61" font-size="12">Pós: '+start[0]+'T'+start[1]+'</text>';
 for(const q of ['Q1',QM]){let path='',last=null,pts='';for(const r of E.filter(r=>r.q===q).sort((a,b)=>ord(a.tri_lbl)-ord(b.tri_lbl))){const v=r[metrica],t=ord(r.tri_lbl);if(!Number.isFinite(v)){last=null;continue;}path+=(last!==null&&t-last===1?'L':'M')+X(t)+' '+Y(v)+' ';last=t;pts+='<circle cx="'+X(t)+'" cy="'+Y(v)+'" r="3" fill="'+(q===QM?'#58df94':'#ff7c8c')+'"><title>'+r.tri_lbl+' · '+q+' · '+fmt(v)+'%</title></circle>';}
 h+='<path d="'+path+'" fill="none" stroke="'+(q===QM?'#58df94':'#ff7c8c')+'" stroke-width="3" '+(q==='Q1'?'stroke-dasharray="6 3"':'')+'/>'+pts;}
 svg.innerHTML=h;
 const col={pct_muda_grupo:'Outro grupo',pct_vai_desocupado:'Desocupado',pct_sai_forca:'Fora da força'}[metrica],A=DATA.destino_por_quartil;
 const pre=pega(A,'pré',QM)[col]-pega(A,'pré','Q1')[col],pos=pega(A,'pós',QM)[col]-pega(A,'pós','Q1')[col];
 $("veredito").textContent='Nas médias ponderadas do recorte, a diferença Q4 − Q1 é '+fmt(pre,2)+' p.p. no pré e '+fmt(pos,2)+' p.p. no pós. A diferença das mudanças é '+fmt(pos-pre,2)+' p.p. Esta comparação é descritiva; a inspeção visual não comprova tendências paralelas nem causalidade.';
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
html=html.replace('</style>','.databar.real{background:#175235;color:#fff}.databar.real label{color:#174626;background:#e5f1d5}.official-audit{border:1px solid #526348;padding:15px;border-radius:6px;margin-top:20px}.official-audit summary{cursor:pointer;font-weight:700}.official-audit p,.official-audit li{font-size:14px;line-height:1.6}</style>');
fs.writeFileSync(__dirname+'/../classico_da_ia.html',html);
const embedded=JSON.parse(html.match(/<script id="dados-embutidos" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.deepStrictEqual(embedded,data);assert(!html.includes('function demo()'));assert(!html.includes('localStorage.getItem'));assert(!html.includes('FLUXOS ILUSTRATIVOS'));
for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)){if(m[0].includes('application/json'))continue;if(m[1].trim())new vm.Script(m[1]);}
const report={source:rotulo,sha256:crypto.createHash('sha256').update(raw).digest('hex'),n_transicoes:data.meta.n_transicoes,rows:Object.fromEntries(['destino_por_quartil','grupo_destino','direcao_exposicao','serie_q1_q4','sankey_pos'].map(k=>[k,data[k].length])),output:'classico_da_ia.html',checks:['Embedded JSON identical to source','No demo generator or stored data fallback','JavaScript syntax valid','Quartile counts sum to metadata','Destination percentages sum to 100% within rounding']};
fs.writeFileSync(__dirname+'/../validacao-dados-oficiais.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
