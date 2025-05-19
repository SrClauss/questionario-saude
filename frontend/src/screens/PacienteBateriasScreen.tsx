import BateriaCard from "../components/BateriaCard";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Paciente } from "../types/user";
import { BateriaTestes } from "../types/baterias";
import { Questionario } from "../types/questionario";
import AdminLayout from "../layouts/AdminLayout";
import StylizedTitle from "../components/StylizedTitle";
import { Box, Modal, Typography, Button, Snackbar, Alert, useTheme } from "@mui/material";

interface BateriaTestesState {
    bateria: BateriaTestes;
    qtd_perguntas: number;
    questionario: Questionario;
    nome_profissional: string;
}

const PacienteBateriasScreen: React.FC = () => {
    const theme = useTheme();
    const { id } = useParams<{ id: string }>()
    const [baterias, setBaterias] = useState<BateriaTestesState[]>([]);
    const [paciente, setPaciente] = useState<Paciente | null>(null);
    const [openDeleteModal, setOpenDeleteModal] = useState(false);
    const [selectedBateriaId, setSelectedBateriaId] = useState<string | null>(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");

    const fetchPaciente = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/pacientes/${id}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                }
            );
            const data = await response.json();

            console.log("Paciente data:", data);
            setPaciente(data);
        } catch (error) {
            console.error("Error fetching paciente:", error);
        }
    };
    const fetchBaterias = async () => {
        try {
            const response = await fetch(

                `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/paciente/${paciente?.id}`,



                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                }
            );
            const data = await response.json();
            setBaterias(data);
        }
        catch (error) {
            console.error("Error fetching baterias:", error);
        }

    }

    useEffect(() => {
        fetchPaciente();
    }, []);

    useEffect(() => {
        if (paciente) {
            fetchBaterias();
        }
    }, [paciente]);
    const handleDelete = async (bateriaId: string) => {
//Rota: /backend/baterias_testes/<id> -> Métodos: OPTIONS, DELETE
        try {
            const response = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/${bateriaId}`,
                {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                }
            );

            if (response.ok) {
                setSnackbarMessage("Bateria excluída com sucesso!");
                setSnackbarOpen(true);
                setOpenDeleteModal(false);
                fetchBaterias();
            } else {
                setSnackbarMessage("Erro ao excluir a bateria.");
                setSnackbarOpen(true);
            }
        } catch (error) {
            console.error("Error deleting bateria:", error);
        }

    

        

    }

    return (
        <AdminLayout>
            <StylizedTitle title={`${paciente?.nome}`} />

            {
                baterias.length > 0 ? (
                    baterias.map((bateria) => (


                        <BateriaCard
                            key={bateria.bateria.id}
                            bateria={bateria.bateria}
                            qtd_perguntas={bateria.qtd_perguntas}
                            questionario={bateria.questionario}
                            nome_profissional={bateria.nome_profissional}
                            onAction={() => {
                                setSelectedBateriaId(bateria.bateria.id);
                                setOpenDeleteModal(true);
                            }}
                        />


                    ))


                ) : (

                    <Box>
                        <Typography variant="h6" color="text.secondary">
                            Nenhuma bateria encontrada para este paciente.
                        </Typography>

                        <Typography variant="body2" color="text.secondary">
                            {id}
                        </Typography>
                    </Box>
                )
            }
                        <Snackbar
                open={snackbarOpen}
                autoHideDuration={6000}
                onClose={() => setSnackbarOpen(false)}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert
                    onClose={() => setSnackbarOpen(false)}
                    severity="success" // ou "info", "warning", "error"
                    sx={{
                        backgroundColor: theme.palette.success.dark, // Cor de fundo desejada
                        color: 'white', // Cor do texto desejada
                    }}
                >
                    {snackbarMessage}
                </Alert>
            </Snackbar>
            <Modal
                open={openDeleteModal}
                onClose={() => setOpenDeleteModal(false)}
            >
                <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 400,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    borderRadius: 2,
                    p: 4,
                }}>
                    <Typography variant="h6" component="h2">
                        Deseja realmente excluir esta bateria?
                    </Typography>
                    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
                        <Button variant="contained" onClick={() => setOpenDeleteModal(false)}>Cancelar</Button>
                        <Button
                            color="error"
                            variant="contained"
                            onClick={() => {
                                if (selectedBateriaId) {
                                    handleDelete(selectedBateriaId);
                                }
                            }}
                        >
                            Excluir
                        </Button>
                    </Box>
                </Box>
            </Modal>

        </AdminLayout>
    )
}

export default PacienteBateriasScreen;