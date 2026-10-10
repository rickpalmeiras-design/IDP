// Variações visuais. Texto, dados e tempo continuam nas fontes originais.
const VARIANTES = [
  { numero: 1, nome: 'Verde acadêmico', verde: '006437', profundo: '0B3B2A', claro: 'EEF4F0' },
  { numero: 2, nome: 'Acadêmico com gráficos à esquerda', verde: '006437', profundo: '083A25', claro: 'EFF6F1', inverter: true, quadrado: true },
  { numero: 3, nome: 'Clássico com títulos centralizados', verde: '005C32', profundo: '103C2B', claro: 'F0F5F2', centralizar: true, titulo: 'Times New Roman' },
  { numero: 4, nome: 'Editorial com resultados à esquerda', verde: '006437', profundo: '123B2B', claro: 'EDF4EF', inverter: true, titulo: 'Times New Roman', quadrado: true },
  { numero: 5, nome: 'Verde profundo e composição plana', verde: '00552F', profundo: '072F20', claro: 'F2F7F4', plano: true, centralizar: true },
  { numero: 6, nome: 'Institucional com gráficos à esquerda', verde: '006437', profundo: '0C3326', claro: 'E8F1EB', inverter: true, centralizar: true },
  { numero: 7, nome: 'Clássico em verde floresta', verde: '006437', profundo: '143B2B', claro: 'F0F6F2', titulo: 'Times New Roman', plano: true },
  { numero: 8, nome: 'Editorial em verde escuro', verde: '005C35', profundo: '082F22', claro: 'ECF4EF', inverter: true, centralizar: true, quadrado: true, titulo: 'Times New Roman' },
  { numero: 9, nome: 'Acadêmico com fundo verde suave', verde: '006437', profundo: '0A3526', claro: 'E3EEE7', fundo: 'F4F8F5', quadrado: true, centralizar: true },
  { numero: 10, nome: 'Síntese com evidências à esquerda', verde: '006437', profundo: '062F20', claro: 'EDF5F0', inverter: true, plano: true, titulo: 'Times New Roman' },
];

// Troca blocos completos, preservando a posição relativa de seus elementos.
// [fim do bloco esquerdo, início do bloco direito].
const COLUNAS = { 4: [4.5, 4.85], 5: [5.5, 5.9], 8: [7.1, 7.55], 12: [6.35, 6.8] };

function configurarLayouts(pres, variante) {
  const adicionar = pres.addSlide.bind(pres);
  let numero = 0;
  pres.addSlide = (...args) => {
    const slide = adicionar(...args);
    numero++;
    const limites = variante.inverter && COLUNAS[numero];
    for (const metodo of ['addText', 'addShape', 'addChart']) {
      const original = slide[metodo].bind(slide);
      slide[metodo] = (...params) => {
        const indice = metodo === 'addChart' ? 2 : 1;
        const entrada = params[indice];
        if (!entrada) return original(...params);
        const op = { ...entrada };
        if (variante.centralizar && op.placeholder === 'title') op.align = 'center';
        if (variante.quadrado && op.shape === pres.ShapeType.roundRect) op.shape = pres.ShapeType.rect;
        if (variante.plano && op.fill && op.fill.color === pres.SchemeColor.background2) {
          op.fill = { ...op.fill, color: pres.SchemeColor.background1 };
        }
        if (limites && Number.isFinite(op.x) && Number.isFinite(op.w) && op.y >= 1.45 && op.y < 6.65) {
          const [fimEsquerda, inicioDireita] = limites;
          if (op.x >= 0.6 - 0.001 && op.x + op.w <= fimEsquerda + 0.001) {
            op.x += 12.73 - fimEsquerda;
          } else if (op.x >= inicioDireita - 0.001 && op.x + op.w <= 12.73 + 0.001) {
            op.x -= inicioDireita - 0.6;
          }
        }
        params[indice] = op;
        return original(...params);
      };
    }
    return slide;
  };
}

module.exports = { VARIANTES, configurarLayouts };
