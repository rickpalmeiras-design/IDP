const assert = require('assert');

// Ajustes editoriais aplicados depois da montagem e da inclusão dos dados reais.
module.exports = function narrativa(html) {
  function troca(antes, depois) {
    assert(html.includes(antes), 'Texto da narrativa não encontrado: ' + antes.slice(0, 100));
    html = html.replace(antes, depois);
  }
  troca('<h2>Estatísticas da partida</h2>', '<h2>Os dois grupos passaram a mudar mais de tipo de trabalho</h2>');
  troca('<h2>Chama o VAR</h2>', '<div class="tempo">Chama o VAR</div><h2 id="tituloVar">A diferença já existia antes do ChatGPT</h2>');
  troca('<h2>O placar final</h2>', '<h2>Mais expostos mudam mais, mas essa diferença já existia antes</h2>');
  troca('<h2>A súmula do jogo</h2>', '<h2>As mudanças observadas não demonstram um efeito da IA</h2>');
  troca('<h2>Os destaques da partida</h2>', '<h2>Alguns destinos ganharam espaço; outros perderam</h2>');
  troca('A tabela do que ainda falta disputar antes de qualquer um desses números virar resultado de verdade.', 'O que falta investigar para avançar da descrição para uma interpretação causal.');
  troca('Se o placar virar, o resultado era da regra, não do jogo.', 'Se a conclusão mudar muito, precisamos entender quanto ela depende das escolhas da análise.');
  troca('Rodar tudo de novo pondo trabalho remoto no lugar da IA. Se der quase o mesmo, a história não era sobre IA.', 'Repetir a análise usando a possibilidade de trabalhar remotamente como foco e a exposição à IA como controle. Um padrão semelhante dificulta interpretar o resultado como específico da IA.');
  troca('Na pandemia o IBGE passou a entrevistar por telefone, e a taxa medida de troca de trabalho caiu pela metade. Antes de tudo, decidir quais trimestres entram no jogo.', 'Durante a coleta por telefone na pandemia, a taxa medida de mudança de ocupação caiu pela metade. Investigar quanto veio da coleta e quanto veio de mudanças reais, para definir períodos comparáveis.');
  troca('Ficar desempregado caiu nos dois times.', 'A parcela que ficou desempregada caiu nos dois grupos.');
  troca('mas ninguém ficou mais desempregado.', 'e a taxa de transição para o desemprego caiu nos dois grupos.');
  troca('Quem trocou de trabalho foi para os mesmos lugares de antes.', 'A ida para ocupações menos expostas mudou pouco no Verdão.');
  troca('o efeito causal depende do diff-in-diff e do teste de pré-tendências.', 'uma interpretação causal exige hipóteses justificadas, investigação da coleta e análises adicionais; nenhum teste isolado comprova causalidade.');
  troca('O placar final só vale se este lance for limpo. Antes de dizer que a IA fez o gol, o VAR confere uma condição: antes do apito (o lançamento do ChatGPT), as duas linhas precisam andar lado a lado.', 'O VAR ajuda a investigar as trajetórias. Para discutir um possível efeito da IA, precisamos avaliar se os grupos evoluíam de forma semelhante antes do lançamento do ChatGPT, mesmo com taxas diferentes.');
  const nota = '<p class="recorte-visivel">Pessoas de 18 a 65 anos, trabalhando na entrevista inicial e acompanhadas três meses depois. Taxas ponderadas pelo peso da pesquisa na origem. Pós-ChatGPT a partir de 2023T1; 2020T1 a 2021T3 e 2022T4 ficam fora das médias. Fonte: PNAD Contínua/IBGE, via Base dos Dados; AIOE de Felten, Raj e Seamans (2021).</p>';
  troca('<h2>Os dois grupos passaram a mudar mais de tipo de trabalho</h2>', '<h2>Os dois grupos passaram a mudar mais de tipo de trabalho</h2>' + nota);
  troca('<div class="var-acoes">', nota + '<div class="var-acoes">');
  // Resposta recolhida para preservar a revelação durante a apresentação oral.
  troca('</p></div><div class="board" aria-label="Placar">', '</p><details class="resposta-central"><summary>Ver a resposta dos dados</summary><p id="respostaCentral"></p></details></div><div class="board" aria-label="Placar">');
  troca('vereditoVar(pre,pos,anima);', `vereditoVar(pre,pos,anima);
 const titulo={pct_muda_grupo:'A diferença já existia antes do ChatGPT e '+(pos-pre>=0?'aumentou ':'diminuiu ')+fmt(Math.abs(pos-pre),2)+' ponto percentual',pct_vai_desocupado:'A transição para o desemprego caiu nos dois grupos',pct_sai_forca:'A saída da força de trabalho teve movimentos diferentes entre os grupos'};
 $("tituloVar").textContent=titulo[metrica];`);
  troca('const gapA = aV - aM, gapD = dV - dM;', `const gapA = aV - aM, gapD = dV - dM;
 $("respostaCentral").textContent='Os mais expostos já mudavam mais de tipo de trabalho antes do ChatGPT. Depois, a distância entre os grupos '+(gapD>=gapA?'aumentou ':'diminuiu ')+fmt(Math.abs(gapD-gapA),2)+' ponto percentual. Essa comparação não demonstra que a IA causou a mudança.';`);
  troca('<p id="rodapeDados"></p>', `<p id="rodapeDados"></p><div class="fontes-publicas"><strong>Fontes e referências</strong><ul><li><a href="https://www.ibge.gov.br/estatisticas/sociais/trabalho/17270-pnad-continua.html" target="_blank" rel="noopener noreferrer">IBGE — PNAD Contínua</a>. Dados trimestrais de trabalho, acessados via <a href="https://basedosdados.org/" target="_blank" rel="noopener noreferrer">Base dos Dados</a>.</li><li>Felten, E.; Raj, M.; Seamans, R. (2021). <em>Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses.</em> Strategic Management Journal, 42(12), 2195–2217. <a href="https://doi.org/10.1002/smj.3286" target="_blank" rel="noopener noreferrer">DOI: 10.1002/smj.3286</a>.</li></ul><p>Recorte descritivo preparado para a disciplina de storytelling de dados a partir dos agregados do projeto. As transições não representam uma contagem de pessoas únicas.</p></div>`);
  troca('</style>', '.recorte-visivel{font-size:13px;line-height:1.6;color:#bdcbbd;margin:16px 0;max-width:90ch}.resposta-central{margin:18px 0;color:#dce9db;font-size:14px}.resposta-central summary{cursor:pointer;text-decoration:underline;text-underline-offset:4px}.fontes-publicas{margin:24px 0;font-size:14px;line-height:1.6}.fontes-publicas a{color:inherit;text-decoration:underline}.fontes-publicas li{margin:10px 0}@media(max-width:600px){.var-scroll{overflow-x:auto}.var-scroll svg{min-width:640px;max-width:none}}#tituloVar{font-size:clamp(1.8rem,4vw,3rem);line-height:1.12}</style>');
  return html;
};
