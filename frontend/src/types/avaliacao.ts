export class Avaliacao{
    id: string;
    data_inicio: string;
    unidade_saude_id: string;
    laudo_id: string | null;
    paciente_id: string;
    fechada: boolean;
    created_at: string;
    updated_at: string;


    constructor(
        id: string,
        data_inicio: string,
        unidade_saude_id: string,
        laudo_id: string | null,
        paciente_id: string,
        fechada: boolean, 
        created_at: string,
        updated_at: string

    ){

        this.id = id;
        this.data_inicio = data_inicio;
        this.unidade_saude_id = unidade_saude_id;
        this.laudo_id = laudo_id;
        this.paciente_id = paciente_id;
        this.fechada = fechada;
        this.created_at = created_at;
        this.updated_at = updated_at;
    }
}



