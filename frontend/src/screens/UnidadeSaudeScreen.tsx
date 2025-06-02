import React, { useState, useEffect } from "react";
import { Snackbar, Alert, Pagination, Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import { Add, Delete, Edit } from "@mui/icons-material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import UnidadeSaudeModal, { UnidadeSaude } from "../modals/UnidadeSaudeModal"; // Assuming UnidadeSaude type is exported from here
import DeleteModal from "../modals/DeleteDialog";
import StylizedTitle from "../components/StylizedTitle";
import { apiFetch } from "../utils/apiFetch";
import { auth } from "../utils/auth";

export default function UnidadeSaudeScreen() {
    const [showUnidadeSaudeModal, setShowUnidadeSaudeModal] = useState(false);
    const [selectedUnidadeSaude, setSelectedUnidadeSaude] = useState<UnidadeSaude | null>(null);
    const [unidadesSaude, setUnidadesSaude] = useState<UnidadeSaude[]>([]);
    const [snackbar, setSnackbar] = useState({ open: false, type: 'success' as 'success' | 'error' | 'warning' | 'info', message: '' });
    const [searchQuery, setSearchQuery] = useState<string>('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [showPagination, setShowPagination] = useState(false);

    const itemsPerPage = 10;

    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const fetchAllUnidadesSaude = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/unidades_saude/`;
        try {
            const response = await apiFetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setUnidadesSaude(data);
            setTotalPages(1); // No pagination for fetching all
            setShowPagination(false);
        } catch (error) {
            console.error('Error fetching unidades de saúde:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao buscar unidades de saúde.' });
        }
    };

    const handleFilter = async (query: string, currentPage: number = 1) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();

        if (query.length === 0) {
            setSearchQuery('');
            setPage(1);
            await fetchAllUnidadesSaude();
            return;
        }
        
        if (query.length < 3 && query.length > 0) { // Only filter if query is 3+ chars, or reset if empty
            setUnidadesSaude([]);
            setShowPagination(false);
            setTotalPages(1);
            return;
        }

        setSearchQuery(query);
        const url = `${baseUrl}/unidades_saude/filter_by_name/${query}/${currentPage}/${itemsPerPage}`;
        try {
            const response = await apiFetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setUnidadesSaude(data.items || []);
            setTotalPages(data.totalPages || 1);
            setShowPagination(data.totalPages > 1);
        } catch (error) {
            console.error('Error filtering unidades de saúde:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao filtrar unidades de saúde.' });
            setUnidadesSaude([]);
            setShowPagination(false);
        }
    };

    useEffect(() => {
        if (searchQuery) {
            handleFilter(searchQuery, page);
        } else {
            fetchAllUnidadesSaude();
        }
    }, [page]); // Re-fetch on page change only if there's a search query

    useEffect(() => { // Initial fetch or fetch when search query is cleared
        if (!searchQuery) {
            fetchAllUnidadesSaude();
        }
    }, []);


    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type as 'success' | 'error' | 'warning' | 'info', message: feedback.message });
        setShowUnidadeSaudeModal(false);
        setSelectedUnidadeSaude(null);
        if (searchQuery) {
            handleFilter(searchQuery, page);
        } else {
            fetchAllUnidadesSaude();
        }
    };

    const handleDelete = async (unidadeId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/unidades_saude/${unidadeId}`;

        try {
            const response = await apiFetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setSnackbar({ open: true, type: 'success', message: 'Unidade de Saúde deletada com sucesso!' });
                setShowDeleteModal(false);
                setSelectedUnidadeSaude(null);
                if (searchQuery) {
                    handleFilter(searchQuery, page);
                } else {
                    fetchAllUnidadesSaude();
                }
            } else {
                const errorData = await response.json().catch(() => ({ message: 'Erro ao deletar unidade de saúde.' }));
                setSnackbar({ open: true, type: 'error', message: errorData.error || errorData.message || 'Erro ao deletar unidade de saúde.' });
            }
        } catch (error) {
            console.error('Error deleting unidade de saúde:', error);
            setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar unidade de saúde.' });
        }
    };

    const handleChangePage = (_event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
        // handleFilter will be called by useEffect if searchQuery is present
    };

    return (
        <AdminLayout>
            <Box id="container" sx={{ paddingTop: { xs: 4, sm: 4, md: 0 } }}>
                <StylizedTitle title="Unidades de Saúde" />
                <SearchBar onSearch={(query) => { setPage(1); handleFilter(query, 1); }} />

                {showUnidadeSaudeModal && (
                    <UnidadeSaudeModal
                        open={showUnidadeSaudeModal}
                        onClose={() => { setShowUnidadeSaudeModal(false); setSelectedUnidadeSaude(null); }}
                        onSubmit={handleModalSubmit}
                        unidadeSaude={selectedUnidadeSaude}
                        mode={selectedUnidadeSaude ? 'edit' : 'create'}
                    />
                )}

                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginY: 2 }}>
                    {unidadesSaude.length > 0 && (
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Nome</TableCell>
                                    <TableCell>CNPJ</TableCell>
                                    <TableCell>Ações</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {unidadesSaude.map((unidade) => (
                                    <TableRow key={unidade.id}>
                                        <TableCell>{unidade.nome}</TableCell>
                                        <TableCell>{unidade.cnpj}</TableCell>
                                        <TableCell>
                                            <Tooltip title="Editar">
                                                <IconButton color="success" onClick={() => { setSelectedUnidadeSaude(unidade); setShowUnidadeSaudeModal(true); }}>
                                                    <Edit />
                                                </IconButton>
                                            </Tooltip>
                                            <Tooltip title="Deletar">
                                                <IconButton color="error" onClick={() => { setSelectedUnidadeSaude(unidade); setShowDeleteModal(true); }}>
                                                    <Delete />
                                                </IconButton>
                                            </Tooltip>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                    {showPagination && unidadesSaude.length > 0 && (
                        <Pagination count={totalPages} page={page} onChange={handleChangePage} color="primary" sx={{ marginTop: 2 }} />
                    )}
                </Box>

                <Tooltip title="Adicionar Unidade de Saúde" arrow>
                    <Fab color="primary" aria-label="add" onClick={() => { setSelectedUnidadeSaude(null); setShowUnidadeSaudeModal(true); }} style={{ position: 'fixed', bottom: 16, right: 32 }}>
                        <Add />
                    </Fab>
                </Tooltip>

                <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={handleSnackbarClose} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
                    <Alert onClose={handleSnackbarClose} severity={snackbar.type} sx={{ width: '100%' }}>
                        {snackbar.message}
                    </Alert>
                </Snackbar>

                {showDeleteModal && selectedUnidadeSaude && (
                    <DeleteModal
                        open={showDeleteModal}
                        onClose={() => { setShowDeleteModal(false); setSelectedUnidadeSaude(null); }}
                        onConfirm={() => handleDelete(selectedUnidadeSaude.id)}
                        itemName={selectedUnidadeSaude.nome}
                    />
                )}
            </Box>
        </AdminLayout>
    );
}