import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Box } from "@mui/material";
import { BateriaTestes } from "../types/baterias";
import { Questionario } from "../types/questionario";
import PacienteLayout from "../layouts/PacienteLayout";
import StylizedTitle from "../components/StylizedTitle";
import BateriaCard from "../components/BateriaCard";

// Nova interface BateriaTestesState para refletir o payload da API
interface BateriaTestesState extends BateriaTestes {
  
    questionario: Questionario; // Objeto Questionario aninhado
    qtd_perguntas: number; // Quantidade de perguntas do questionário associado
    nome_profissional: string | null; // Nome do profissional, pode ser nulo
  
}

export default function TestesAplicadosPacienteScreen() {

    const avaliacaId = useParams().avaliacao_id

    const navigate = useNavigate();
    const [baterias, setBaterias] = useState<BateriaTestesState[]>([]);

    useEffect(() => {

        const fetchBaterias = async () => {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/avaliacao/${avaliacaId}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem(
                                "@App:token"
                            )}`,
                        },
                    }
                );
                const data = await response.json();
                console.log("dada", data);
                setBaterias(data);
            } catch (error) {
                console.error("Error fetching baterias:", error);
            }
        };
        fetchBaterias();




    }, []);
    return (
        <PacienteLayout>
            <StylizedTitle title="Testes Aplicados" />

            <Box>
                {
                    baterias.map((bateria) => {

                        return (
                            <BateriaCard
                                key={bateria.id}
                                bateria={bateria} // Passa o objeto bateria inteiro
                                questionario={bateria.questionario}
                                qtd_perguntas={bateria.qtd_perguntas}
                                nome_profissional={bateria.nome_profissional || "Não informado"} // Lida com nome_profissional nulo
                                onAction={() => {
                                    navigate(`/bateria/${bateria.id}`); // Navega usando o id da bateria
                                }}


                            />
                        );
                    })
                }
            </Box>
        </PacienteLayout>
    );
}
