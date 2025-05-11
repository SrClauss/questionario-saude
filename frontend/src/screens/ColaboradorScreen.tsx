import React from "react";
import { Snackbar, Alert } from "@mui/material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import ColaboradorModal from "../modals/ColaboradorModal";
import { Colaborador } from "../types/user";
import { Add, Delete, InfoRounded } from "@mui/icons-material";
import { Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog";

export default function ColaboradorScreen() {
    const [showColaboradorModal, setShowColaboradorModal] = React.useState(false);
    const [selectedColaborador, setSelectedColaborador] = React.useState<Colaborador | null>(null);
    const [colaboradores, setColaboradores] = React.useState<Colaborador[]>([]);
    const [snackbar, setSnackbar] = React.useState({ open: false, type: '', message: '' });
    const [searchQuery, setSearchQuery] = React.useState<string>(''); // Armazena o último termo de busca
    const [showDeleteModal, setShowDeleteModal] = React.useState(false);

    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const handleFilter = (query: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        if (query.length < 3) {
            return;
        }

        setSearchQuery(query); // Salva o termo de busca mais recente

        const url = `${baseUrl}/colaboradores/filter_by_name/${query}`;
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setColaboradores(data);
            })
            .catch((error) => {
                console.error('Error fetching colaboradores:', error);
            });
    };

    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowColaboradorModal(false);

        // Atualiza a lista de colaboradores com o último termo de busca
        if (searchQuery) {
            handleFilter(searchQuery);
        }
    };

    const handleDelete = (colaboradorId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/colaboradores/${colaboradorId}`;
        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
            .then((response) => {
                if (response.ok) {
                    setSnackbar({ open: true, type: 'success', message: 'Colaborador deletado com sucesso!' });
                    setShowDeleteModal(false);
                    // Atualiza a lista de colaboradores com o último termo de busca
                    if (searchQuery) {
                        handleFilter(searchQuery);
                    }
                } else {
                    setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar colaborador.' });
                }
            }).catch((error) => {
                console.error('Error deleting colaborador:', error);
                setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar colaborador.' });
            }
        );
    }

    return (
        <AdminLayout>
            <SearchBar onSearch={handleFilter} />
            {showColaboradorModal && (
                <ColaboradorModal
                    open={showColaboradorModal}
                    onClose={() => setShowColaboradorModal(false)}
                    onSubmit={handleModalSubmit} // Chama a função para atualizar a lista e exibir a snackbar
                    colaborador={selectedColaborador}
                    mode={selectedColaborador ? 'edit' : 'create'}
                />
            )}

            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginY: 2 }}>
                {colaboradores.length > 0 && (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Nome</TableCell>
                                <TableCell>Função</TableCell>
                                <TableCell>Info</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {colaboradores.map((colaborador) => (
                                <TableRow key={colaborador.id}>
                                    <TableCell>{colaborador.nome}</TableCell>
                                    <TableCell>{colaborador.funcao}</TableCell>
                                    <TableCell>
                                        <IconButton>
                                            <InfoRounded
                                                color="info"
                                                onClick={() => {
                                                    setSelectedColaborador(colaborador);
                                                    setShowColaboradorModal(true);
                                                }}
                                            />
                                        </IconButton>
                                        <IconButton
                                            color="error"
                                            onClick={() => {
                                                setSelectedColaborador(colaborador);
                                                setShowDeleteModal(true);
                                            }}
                                        >
                                            <Delete />
                                        </IconButton>
                                        {showDeleteModal && (
                                            <DeleteModal
                                                open={showDeleteModal}
                                                onClose={() => setShowDeleteModal(false)}
                                                onConfirm={() => {
                                                    handleDelete(colaborador.id);
                                                    setShowDeleteModal(false);
                                                }}
                                            />
                                        )}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </Box>
            <Tooltip title="Adicionar Colaborador" arrow>
                <Fab
                    color="primary"
                    aria-label="add"
                    onClick={() => {
                        setSelectedColaborador(null);
                        setShowColaboradorModal(true);
                    }}
                    style={{ position: 'fixed', bottom: 16, right: 16 }}
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
        </AdminLayout>
    );
}