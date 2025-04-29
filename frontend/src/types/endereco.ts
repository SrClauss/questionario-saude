
export class Endereco {
    id: string
    logradouro: string;
    numero: string;
    complemento?: string;
    bairro: string;
    cidade: string;
    estado: string;
    cep: string;
  
    constructor(
      id: string,
      logradouro: string,
      numero: string,
      bairro: string,
      cidade: string,
      estado: string,
      cep: string,
      complemento?: string
    ) {
      this.id = id;
      this.logradouro = logradouro;
      this.numero = numero;
      this.complemento = complemento || '';
      this.bairro = bairro;
      this.cidade = cidade;
      this.estado = estado;
      this.cep = cep;
    }
  }