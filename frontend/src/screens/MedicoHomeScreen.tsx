import { useEffect, useState } from "react";
import MedicoLayout from "../layouts/MedicoLayout";
import { auth } from "../utils/auth";
import { Box, Typography } from "@mui/material";
import StylizedTitle from "../components/StylizedTitle";

import { AvaliacaoFetch } from "../components/ComponenteAvaliacao";
import ComponenteAvaliacaoMedico from "../components/ComponenteAvaliacaoMedico";
export default function MedicoHomeScreen() {

    const medico = auth.getProfile()
    const [avaliacoes, setAvaliacoes] = useState<AvaliacaoFetch[]>([])
    

    useEffect(() => {

        fetchAvaliacoesByMedicoId()

    }, [])
    const fetchAvaliacoesByMedicoId = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");

        try {
            const response = await fetch(`${baseUrl}/avaliacoes/por_medico/${medico?.id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setAvaliacoes(data);
        } catch (error) {
            console.error("Error fetching avaliacoes:", error);
        }

      



    }
    return (



        <MedicoLayout>
            <Box id="container"
                sx={{
                    paddingTop: { xs: 4, sm: 4, md: 0 }
                }
            }
            >
                <StylizedTitle title={`Olá, ${medico?.nome.split(" ")[0]}`} />

                <Box>
                    <Typography variant="body1">
                        Estas são as avaliações direcionadas a voce:
                    </Typography>
                    {avaliacoes
                        .filter(avaliacao => !avaliacao.avaliacao.fechada) // Filtra para mostrar apenas avaliações não fechadas
                        .map((avaliacao) => (
                        <ComponenteAvaliacaoMedico 
                            key={avaliacao.avaliacao.id} // Adicionar uma key única
                            avaliacaoFetch={avaliacao} // Passar o objeto avaliacao para a prop avaliacaoFetch
                        />
                    ))}


                </Box>


            </Box>
        </MedicoLayout>
    )
}