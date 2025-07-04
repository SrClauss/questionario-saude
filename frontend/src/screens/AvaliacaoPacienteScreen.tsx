import { useEffect } from "react";
import { Box} from "@mui/material";
import { Paciente } from "../types/user";
import PacienteLayout from "../layouts/PacienteLayout";
import { useState } from "react";
import { auth } from "../utils/auth";
import { Avaliacao } from "../types/avaliacao";
import { Questionario } from "../types/questionario";

import StylizedTitle from "../components/StylizedTitle";
import ComponenteAvaliacao from "../components/ComponenteAvaliacao";
interface AvaliacaoFetch {
    avaliacao: Avaliacao;
    baterias_testes: BateriasTestesJoin[];
    paciente: Paciente;

}
interface BateriasTestesJoin {
    colaborador_id: string;
    created_at: string;
    data_aplicacao: string;
    id: string;
    is_completo: boolean;
    observacoes: string;
    paciente_id: string;
    profissional_saude_id: string;
    questionario_id: string;
    respostas: {};
    total_perguntas: number;
    updated_at: string;
    questionario: Questionario;

}

export default function AvaliacaoPacienteScreen() {
    const pacienteId = auth.getProfile()?.id;
    const [avaliacoesFetch, setAvaliacoesFetch] = useState<AvaliacaoFetch[]>([]);

    const fetchAvaliacoes = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");

        try {
            const response = await fetch(`${baseUrl}/avaliacoes/paciente/${pacienteId}`, {

                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },

            });
            const data = await response.json();
            setAvaliacoesFetch(data);
        } catch (error) {
            console.error("Error fetching avaliacoes:", error);
        }
    };


    useEffect(() => {
        fetchAvaliacoes();
    }, []);

    return (
        <PacienteLayout>
            <Box>

                <Box sx={{ marginBottom: 2 }} >
                    <StylizedTitle title={`Avaliações de ${avaliacoesFetch[0]?.paciente?.nome || "N/A"}`} size="h6" />

                </Box>
       

                {avaliacoesFetch.map((avaliacaoFetch) => (
                    <ComponenteAvaliacao key={avaliacaoFetch.avaliacao.id} avaliacaoJoin={avaliacaoFetch} />
                ))}
             


            </Box>
        
        </PacienteLayout>
    );
}

