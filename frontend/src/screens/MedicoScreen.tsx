
import { useState, useEffect } from "react";
import { Snackbar, Alert, Pagination } from "@mui/material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import MedicoModal from "../modals/MedicoModal";
import { Medico } from "../types/user";
import { Add, Delete, Edit,  } from "@mui/icons-material";
import { Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog";
import { useNavigate } from "react-router-dom";
import StylizedTitle from "../components/StylizedTitle";
import { apiFetch } from "../utils/apiFetch";


export default function MedicoScreen() {
    const [showMedicoModal, setShowMedicoModal] = useState(false);
    const [selectedMedico, setSelectedMedico] = useState<Medico | null>(null);
    const [medicos, setMedicos] = useState<Medico[]>([]);
    const [snackbar, setSnackbar] = useState({ open: false, type: '', message: '' });
    const [searchQuery, setSearchQuery] = useState<string>(''); // Armazena o último termo de busca
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showPagination, setShowPagination] = useState(false);
    const [page, setPage] = useState(1); // Página inicial
    const [totalPages, setTotalPages] = useState(1); // Total de páginas

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

        const url = `${baseUrl}/medicos/filter_by_name/${query}/1/10`;
        try {
            const response = await apiFetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setMedicos(data);


        } catch (error) {
            console.error('Error fetching pacientes:', error);
        }
    };
    const getMedicoPage = async (page: number) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/medicos/${page}/10`; // Ajuste o número de médicos por página conforme necessário
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

            setMedicos(data.items); // Assumindo que a API retorna um objeto com a propriedade 'items'
            setTotalPages(data.totalPages); // Assumindo que a API retorna um objeto com a propriedade 'totalPages'
            setShowPagination(true);
        } catch (error) {
            console.error('Error fetching medicos:', error);
        }
    };


    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowMedicoModal(false);

        // Atualiza a lista de médicos com o último termo de busca
        if (searchQuery) {
            handleFilter(searchQuery);
        } else {
            getMedicoPage(page);
        }
    };
    const handleDelete = (medicoId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/medicos/${medicoId}`; // Mantendo sua rota original

        apiFetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        }).then((response) => {
            if (response.ok) {
                setSnackbar({ open: true, type: 'success', message: 'Médico deletado com sucesso!' });
                setShowDeleteModal(false);

                // Apenas isto já deveria atualizar a lista após a exclusão
                if (searchQuery) {
                    handleFilter(searchQuery);
                } else {
                    // Force a atualização da página atual mesmo sem uma busca
                    getMedicoPage(page);
                }
            } else {
                setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar médico.' });
            }
        })
            .catch((error) => {
                console.error('Error deleting paciente:', error);
            })

    };
    const handleChangePage = (_event: any, value: number) => {
        setPage(value);
        getMedicoPage(value);
    };

    useEffect(() => {
        getMedicoPage(1); // Carrega a primeira página ao montar o componente
    }, []);



    return (
        <AdminLayout>
            <Box id="container"
                sx={{
                    paddingTop: { xs: 4, sm: 4, md: 0 },
                }}
            >
                <StylizedTitle title="Médicos" />
                <SearchBar onSearch={handleFilter} />
                {showMedicoModal && (
                    <MedicoModal
                        open={showMedicoModal}
                        onClose={() => setShowMedicoModal(false)}
                        onSubmit={handleModalSubmit} // Chama a função para atualizar a lista e exibir a snackbar
                        medico={selectedMedico}
                        mode={selectedMedico ? 'edit' : 'create'}
                    />
                )}

                <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center', marginY: 2 }}>
                    {medicos?.length > 0 && (
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Nome</TableCell>
                                    <TableCell>CRM</TableCell>
                                    <TableCell>Info</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {medicos.map((medico) => (
                                    <TableRow key={medico.id}>
                                        <TableCell>{medico.nome}</TableCell>
                                        <TableCell>{medico.crm}</TableCell>
                                        <TableCell>
                                            <IconButton>
                                                <Edit
                                                    color="success"
                                                    onClick={() => {
                                                        setSelectedMedico(medico);
                                                        setShowMedicoModal(true);
                                                    }}
                                                />
                                            </IconButton>
                                            <IconButton
                                                color="error"
                                                onClick={() => {
                                                    setSelectedMedico(medico);
                                                    setShowDeleteModal(true);
                                                }}
                                            >
                                                <Delete />
                                            </IconButton>
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

                <Tooltip title="Adicionar Médico" arrow>
                    <Fab
                        color="primary"
                        aria-label="add"
                        onClick={() => {
                            setSelectedMedico(null);
                            setShowMedicoModal(true);
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

   
                {showDeleteModal && selectedMedico && (
                    <DeleteModal
                        open={showDeleteModal}
                        onClose={() => setShowDeleteModal(false)}
                        onConfirm={() => {
                            handleDelete(selectedMedico.id); // Agora usa o ID correto
                            setShowDeleteModal(false);
                        }}
                    />
                )}
            </Box>
        </AdminLayout>
    )


}



