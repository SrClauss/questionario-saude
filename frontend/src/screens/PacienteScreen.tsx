import { useState, useEffect } from "react";
import { Snackbar, Alert, Pagination } from "@mui/material";
import SearchBar from "../components/SearchBar";
import VariableLayout from "../layouts/VariableLayout";
import PacienteModal from "../modals/PacienteModal";
import { Paciente } from "../types/user";
import { Add, BallotRounded, Delete, Edit, InfoRounded } from "@mui/icons-material";
import { Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog";
import { useNavigate } from "react-router-dom";
import StylizedTitle from "../components/StylizedTitle";
import { apiFetch } from "../utils/apiFetch";
import AvaliacaoIconComponent from "../components/AvaliacaoIconComponent";
import { auth } from "../utils/auth";


export default function PacienteScreen() {
    const [showPacienteModal, setShowPacienteModal] = useState(false);
    const [selectedPaciente, setSelectedPaciente] = useState<Paciente | null>(null);
    const [pacientes, setPacientes] = useState<Paciente[]>([]);
    const [snackbar, setSnackbar] = useState({ open: false, type: '', message: '' });
    const [searchQuery, setSearchQuery] = useState<string>(''); // Armazena o último termo de busca
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showPagination, setShowPagination] = useState(false);
    const [page, setPage] = useState(1); // Página inicial
    const [totalPages, setTotalPages] = useState(1); // Total de páginas
    const role = auth.getUserData()?.role;
    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const handleFilter = async (query: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        if (query.length < 3) {
            return;
        }

        setSearchQuery(query); // Salva o termo de busca mais recente

        const url = `${baseUrl}/pacientes/filter_by_name/${query}`;
        try {
            const response = await apiFetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setPacientes(data);
        } catch (error) {
            console.error('Error fetching pacientes:', error);
        }
    };

    const getPacientesPage = async (page: number) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/pacientes/${page}/10`; // Ajuste o número de pacientes por página conforme necessário
        try {
            const response = await apiFetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            //ordene data.items por nome

            setPacientes(data.items); // Assumindo que a API retorna um objeto com a propriedade 'items'
            setTotalPages(data.totalPages); // Assumindo que a API retorna um objeto com a propriedade 'totalPages'
            setShowPagination(true);
        } catch (error) {
            console.error('Error fetching pacientes:', error);
        }
    };

    const navigate = useNavigate();

    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowPacienteModal(false);

        // Atualiza a lista de pacientes com o último termo de busca
        if (searchQuery) {
            handleFilter(searchQuery);
        }
    };

    const handleDelete = async (pacienteId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/pacientes/${pacienteId}`; // Mantendo sua rota original

        try {
            const response = await apiFetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setSnackbar({ open: true, type: 'success', message: 'Paciente deletado com sucesso!' });
                setShowDeleteModal(false);

                // Apenas isto já deveria atualizar a lista após a exclusão
                if (searchQuery) {
                    handleFilter(searchQuery);
                } else {
                    // Force a atualização da página atual mesmo sem uma busca
                    await getPacientesPage(page);
                }
            } else {
                setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar paciente.' });
            }
        } catch (error) {
            console.error('Error deleting paciente:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar paciente.' });
        }
    };

    const handleChangePage = (_event: any, value: number) => {
        setPage(value);
        getPacientesPage(value);
    };

    useEffect(() => {
        getPacientesPage(1); // Carrega a primeira página ao montar o componente
    }, []);

    return (
        <VariableLayout>
            <Box id="container"
                sx={{
                    paddingTop: { xs: 4, sm: 4, md: 0 },
                }}
            >
                <StylizedTitle title="Pacientes" />
                <SearchBar onSearch={handleFilter} />
                {showPacienteModal && (
                    <PacienteModal
                        open={showPacienteModal}
                        onClose={() => setShowPacienteModal(false)}
                        onSubmit={handleModalSubmit} // Chama a função para atualizar a lista e exibir a snackbar
                        paciente={selectedPaciente}
                        mode={selectedPaciente ? 'edit' : 'create'}
                    />
                )}

                <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center', marginY: 2 }}>
                    {pacientes?.length > 0 && (
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Nome</TableCell>
                                    <TableCell>Data Nascimento</TableCell>
                                    <TableCell>Info</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {pacientes.map((paciente) => (
                                    <TableRow key={paciente.id}>
                                        <TableCell>{paciente.nome}</TableCell>
                                        <TableCell>
                                            {new Date(paciente.data_nascimento).toLocaleDateString('pt-BR')}
                                        </TableCell>
                                        <TableCell>
                                            <Tooltip title="Avaliações">
                                                <IconButton
                                                    onClick={() => navigate(`/avaliacao/${paciente.id}`)}
                                                >
                                                    <AvaliacaoIconComponent
                                                        color="secoundary"
                                                    />
                                                </IconButton>

                                            </Tooltip>

                                            {
                                                role === "admin" &&

                                                (<Tooltip title="Editar">
                                                    <IconButton >
                                                        <Edit
                                                            color="success"

                                                            onClick={() => {
                                                                setSelectedPaciente(paciente);
                                                                setShowPacienteModal(true);
                                                            }}
                                                        />
                                                    </IconButton>
                                                </Tooltip>)
                                            }


                                            {

                                                role === "admin" && (

                                                    <Tooltip title="Excluir">
                                                        <IconButton
                                                            color="error"
                                                            onClick={() => {
                                                                setSelectedPaciente(paciente);
                                                                setShowDeleteModal(true);
                                                            }}
                                                        >
                                                            <Delete />
                                                        </IconButton>
                                                    </Tooltip>
                                                )
                                            }
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                    {showPagination && (
                        <Pagination
                            count={totalPages}
                            page={page}
                            onChange={handleChangePage}
                            color="primary"
                        />
                    )}
                </Box>
                <Tooltip title="Adicionar Paciente" arrow>
                    <Fab
                        color="primary"
                        aria-label="add"
                        onClick={() => {
                            setSelectedPaciente(null);
                            setShowPacienteModal(true);
                        }}
                        style={{ position: 'fixed', bottom: 16, right: 32 }}
                    >
                        <Add />
                    </Fab>
                </Tooltip>
                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={handleSnackbarClose}
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                >
                    <Alert
                        onClose={handleSnackbarClose}
                        severity={snackbar.type as 'success' | 'error' | 'info' | 'warning'}
                        sx={{ width: '100%' }}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>

                {/* Modal fora do loop */}
                {showDeleteModal && selectedPaciente && (
                    <DeleteModal
                        open={showDeleteModal}
                        onClose={() => setShowDeleteModal(false)}
                        onConfirm={() => {
                            handleDelete(selectedPaciente.id); // Agora usa o ID correto
                            setShowDeleteModal(false);
                        }}
                    />
                )}

                {

                }
            </Box>
        </VariableLayout>
    );
}