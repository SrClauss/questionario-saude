import { useEffect, useState } from "react";
import {useNavigate } from "react-router-dom";
import {Box } from "@mui/material";
import { BateriaTestes } from "../types/baterias";
import { Paciente } from "../types/user";
import { Questionario } from "../types/questionario";
import PacienteLayout from "../layouts/PacienteLayout";
import StylizedTitle from "../components/StylizedTitle";
import BateriaCard from "../components/BateriaCard";


interface BateriaTestesState {
    bateria: BateriaTestes;
    qtd_perguntas: number;
    questionario: Questionario;
    nome_profissional: string;
}
export default function TestesAplicadosPacienteScreen() {
    const profile: Paciente = JSON.parse(localStorage.getItem("@App:profile") || "{}");
    const navigate = useNavigate();
    const [baterias, setBaterias] = useState<BateriaTestesState[]>([]);
    
    useEffect(() => {
        if (profile) {
            const fetchBaterias = async () => {
                try {
                    const response = await fetch(
                        `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/paciente/${profile.id}`,
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


        }

    }, []);
    return (
        <PacienteLayout>
            <StylizedTitle title="Testes Aplicados" />
            
            <Box>
                {
                    baterias.map((bateria) => {

                        return (
                            <BateriaCard
                                key={bateria.bateria.id}
                                bateria={bateria.bateria}
                                questionario={bateria.questionario}
                                qtd_perguntas={bateria.qtd_perguntas}
                                nome_profissional={bateria.nome_profissional}
                                onAction={() => {
                                    navigate(`/bateria/${bateria.bateria.id}`);
                                }}
                                
                                
                            />
                        );
                    })
                }
            </Box>
        </PacienteLayout>
    );
}



