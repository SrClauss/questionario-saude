import { FonteBibliografica } from "../types/questionario";

// Função para formatar uma única fonte bibliográfica no padrão ABNT
export const formatarFonteABNT = (fonte: FonteBibliografica): string => {
  // Formata os autores
  const autoresArray = fonte.autores.split(',').map(autor => autor.trim());
  const autoresFormatados = autoresArray.map(autor => {
    const partes = autor.split(' ');
    if (partes.length > 1) {
      const sobrenome = partes.pop()?.toUpperCase();
      const nome = partes.join(' ');
      return `${sobrenome}, ${nome}`;
    } else {
      return autor.toUpperCase();
    }
  });

  let autoresString = autoresFormatados.join('; ');

  // Monta a referência bibliográfica
  let referencia = `${autoresString}. ${fonte.titulo}. `;

  if (fonte.local && fonte.editora) {
    referencia += `${fonte.local}: ${fonte.editora}, ${fonte.ano}.`;
  } else if (fonte.editora) {
    referencia += `${fonte.editora}, ${fonte.ano}.`;
  } else if (fonte.local) {
    referencia += `${fonte.local}, ${fonte.ano}.`;
  } else {
    referencia += `${fonte.ano}.`;
  }

  return referencia;
};