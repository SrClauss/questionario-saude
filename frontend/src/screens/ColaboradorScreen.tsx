import React, { useEffect, useState } from "react";
import { Snackbar, Alert, Pagination } from "@mui/material";
import SearchBar from "../components/SearchBar";
import VariableLayout from "../layouts/VariableLayout";
import ColaboradorModal from "../modals/ColaboradorModal";
import { Colaborador } from "../types/user";
import { Add, Delete, Edit, InfoRounded } from "@mui/icons-material";
import { Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog";
import StylizedTitle from "../components/StylizedTitle";
import { ProtectedRouteProvider } from "../providers/ProtectedRouteProvider";

export default function ColaboradorScreen() {
    const [showColaboradorModal, setShowColaboradorModal] = React.useState(false);
    const [selectedColaborador, setSelectedColaborador] = React.useState<Colaborador | null>(null);
    const [colaboradores, setColaboradores] = React.useState<Colaborador[]>([]);
    const [snackbar, setSnackbar] = React.useState({ open: false, type: '', message: '' });
    const [searchQuery, setSearchQuery] = React.useState<string>(''); // Armazena o último termo de busca
    const [showDeleteModal, setShowDeleteModal] = React.useState(false);
    const [showPagination, setShowPagination] = React.useState(false);
    const [page, setPage] = React.useState(1); // Página inicial
    const [totalPages, setTotalPages] = React.useState(1); // Total de páginas

    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const getColaboradoresPage = async (pageNumber: number) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/colaboradores/${pageNumber}/10`; // Assumindo 10 itens por página

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();

            // Assumindo que a API retorna um objeto com 'items' e 'totalPages'
            if (data && data.items && typeof data.totalPages === 'number') {
                setColaboradores(data.items);
                setTotalPages(data.totalPages);
                setShowPagination(true);
            } else {
                // Fallback se a estrutura não for a esperada (ex: API antiga)
                setColaboradores(data || []);
                setTotalPages(1);
                setShowPagination(Array.isArray(data) && data.length > 0);
            }
        } catch (error) {
            console.error('Error fetching colaboradores:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao buscar colaboradores.' });
            setColaboradores([]);
            setShowPagination(false);
        }
    };

    useEffect(() => {
        getColaboradoresPage(1); // Carrega a primeira página ao montar o componente
    }, []);

    const handleFilter = async (query: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');

        if (query.length === 0) {
            setSearchQuery('');
            getColaboradoresPage(1); // Volta para a primeira página da lista completa
            return;
        }

        if (query.length < 3) {
            return;
        }

        setSearchQuery(query); // Salva o termo de busca mais recente
        setShowPagination(false); // Filtro geralmente não é paginado ou reseta a paginação

        const url = `${baseUrl}/colaboradores/filter_by_name/${query}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setColaboradores(data);
        } catch (error) {
            console.error('Error fetching colaboradores:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao filtrar colaboradores.' });
            setColaboradores([]);
        }
    };

    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowColaboradorModal(false);
        setSelectedColaborador(null);

        if (searchQuery) {
            handleFilter(searchQuery);
        } else {
            getColaboradoresPage(page);
        }
    };

    const handleDelete = async (colaboradorId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/colaboradores/${colaboradorId}`;
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setSnackbar({ open: true, type: 'success', message: 'Colaborador deletado com sucesso!' });
                setShowDeleteModal(false);
                setSelectedColaborador(null);

                if (searchQuery) {
                    handleFilter(searchQuery);
                } else {
                    // Se a página atual ficar vazia após a exclusão, vá para a página anterior se não for a primeira
                    if (colaboradores.length === 1 && page > 1) {
                        setPage(page - 1);
                        getColaboradoresPage(page - 1);
                    } else {
                        getColaboradoresPage(page);
                    }
                }
            } else {
                const errorData = await response.json().catch(() => ({ message: 'Erro ao deletar colaborador.' }));
                setSnackbar({ open: true, type: 'error', message: errorData.message || 'Erro ao deletar colaborador.' });
            }
        } catch (error) {
            console.error('Error deleting colaborador:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar colaborador.' });
        }
    };

    const handleChangePage = (_event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
        getColaboradoresPage(value);
    };

    return (

        <VariableLayout>
            <ProtectedRouteProvider allowed={['admin', 'colaborador']}>
                <Box sx={{ paddingTop: { xs: 4, sm: 4, md: 0 } }}>
                    <StylizedTitle title="Colaboradores" />
                    <SearchBar onSearch={handleFilter} />
                </Box>

                {showColaboradorModal && (
                    <ColaboradorModal
                        open={showColaboradorModal}
                        onClose={() => setShowColaboradorModal(false)}
                        onSubmit={handleModalSubmit} // Chama a função para atualizar a lista e exibir a snackbar
                        colaborador={selectedColaborador}
                        mode={selectedColaborador ? 'edit' : 'create'}
                    />
                )}

                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginY: 2 }}>
                    {colaboradores && colaboradores.length > 0 && (
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
                                                <Edit
                                                    color="success"
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
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                    {showPagination && colaboradores && colaboradores.length > 0 && (
                        <Pagination
                            count={totalPages}
                            page={page}
                            onChange={handleChangePage}
                            color="primary"
                            sx={{ marginTop: 2 }}
                        />
                    )}
                </Box>
                {showDeleteModal && selectedColaborador && (
                    <DeleteModal
                        open={showDeleteModal}
                        onClose={() => { setShowDeleteModal(false); setSelectedColaborador(null); }}
                        onConfirm={() => handleDelete(selectedColaborador.id)}
                        itemName={selectedColaborador.nome}
                    />
                )}
                <Tooltip title="Adicionar Colaborador" arrow>
                    <Fab
                        color="primary"
                        aria-label="add"
                        onClick={() => {
                            setSelectedColaborador(null);
                            setShowColaboradorModal(true);
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
            </ProtectedRouteProvider>
        </VariableLayout>
    );
}