export class Laudo {
  id: string;
  medico_id: string;
  paciente_id: string;
  cid: string;
  data: string; // Assuming date is represented as a string (e.g., ISO format)
  parecer: string;
  abordagem_terapeutica: string;
  created_at: string; // Assuming datetime is represented as a string
  updated_at: string; // Assuming datetime is represented as a string

  constructor(
    id: string,
    medico_id: string,
    paciente_id: string,
    cid: string,
    data: string,
    parecer: string,
    abordagem_terapeutica: string,
    created_at: string,
    updated_at: string
  ) {
    this.id = id;
    this.medico_id = medico_id;
    this.paciente_id = paciente_id;
    this.cid = cid;
    this.data = data;
    this.parecer = parecer;
    this.abordagem_terapeutica = abordagem_terapeutica;
    this.created_at = created_at;
    this.updated_at = updated_at;
  }
}

