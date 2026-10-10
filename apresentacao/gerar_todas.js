// Gera dez apresentações numeradas com o mesmo conteúdo e cronograma.
const { execFileSync } = require('child_process');
const path = require('path');
const { VARIANTES } = require('./variantes.js');
for (const variante of VARIANTES) {
  execFileSync(process.execPath, [path.join(__dirname, 'gerar_apresentacao.js'), '--versao', String(variante.numero)], { stdio: 'inherit' });
}
