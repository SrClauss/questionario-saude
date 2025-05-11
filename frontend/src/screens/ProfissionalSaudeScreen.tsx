// filepath: d:\Source\projeto-noemi\frontend\src\screens\ProfissionalSaudeScreen.tsx
import React from "react";
import { Snackbar, Alert } from "@mui/material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import ProfissionalSaudeModal from "../modals/ProfissionalSaudeModal";
import { ProfissionalSaude } from "../types/user";
import { Add, Delete, InfoRounded } from "@mui/icons-material";
import { Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog";
import StylizedTitle from "../components/StylizedTitle";

export default function ProfissionalSaudeScreen() {
    const [showProfissionalSaudeModal, setShowProfissionalSaudeModal] = React.useState(false);
    const [selectedProfissionalSaude, setSelectedProfissionalSaude] = React.useState<ProfissionalSaude | null>(null);
    const [profissionaisSaude, setProfissionaisSaude] = React.useState<ProfissionalSaude[]>([]);
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

        const url = `${baseUrl}/profissionais_saude/filter_by_name/${query}`;
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setProfissionaisSaude(data);
            })
            .catch((error) => {
                console.error('Error fetching profissionais de saúde:', error);
            });
    };


    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowProfissionalSaudeModal(false);

        // Atualiza a lista de profissionais de saúde com o último termo de busca
        if (searchQuery) {
            handleFilter(searchQuery);
        }
    };
    const handleDelete = (profissionalSaudeId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/profissionais_saude/${profissionalSaudeId}`;
        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
            .then((response) => {
                if (response.ok) {
                    setSnackbar({ open: true, type: 'success', message: 'Profissional de saúde deletado com sucesso!' });
                    setShowDeleteModal(false);
                    // Atualiza a lista de profissionais de saúde com o último termo de busca
                    if (searchQuery) {
                        handleFilter(searchQuery);
                    }
                } else {
                    setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar profissional de saúde.' });
                }
            }).catch((error) => {
                console.error('Error deleting profissional de saúde:', error);
                setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar profissional de saúde.' });
            }
        );
    }
    return (
        <AdminLayout>

             <Box id="container"

            sx={{
                paddingTop:{ xs: 4, sm: 4, md: 0 },
            }}
            >
            <StylizedTitle title="Profissionais de Saúde" />
            <SearchBar onSearch={handleFilter} />
            {showProfissionalSaudeModal && (
                <ProfissionalSaudeModal
                    open={showProfissionalSaudeModal}
                    onClose={() => setShowProfissionalSaudeModal(false)}
                    onSubmit={handleModalSubmit} // Chama a função para atualizar a lista e exibir a snackbar
                    profissionalSaude={selectedProfissionalSaude}
                    mode={selectedProfissionalSaude ? 'edit' : 'create'}
                />
            )}



            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginY: 2 }}>
                {profissionaisSaude.length > 0 && (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Nome</TableCell>
                                <TableCell>Registro Profissional</TableCell>
                                <TableCell>Info</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {profissionaisSaude.map((profissionalSaude) => (
                                <TableRow key={profissionalSaude.id}>
                                    <TableCell>{profissionalSaude.nome}</TableCell>
                                    <TableCell>{profissionalSaude.registro_profissional}</TableCell>
                                    <TableCell>
                                        <IconButton>
                                            <InfoRounded
                                                color="info"
                                                onClick={() => {
                                                    setSelectedProfissionalSaude(profissionalSaude);
                                                    setShowProfissionalSaudeModal(true);
                                                }}
                                            />
                                        </IconButton>
                                        <IconButton
                                            color="error"
                                            onClick={() => {
                                                setSelectedProfissionalSaude(profissionalSaude);
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
                                                    handleDelete(profissionalSaude.id);
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
            <Tooltip title="Adicionar Profissional de Saúde" arrow>
                <Fab
                    color="primary"
                    aria-label="add"
                    onClick={() => {
                        setSelectedProfissionalSaude(null);
                        setShowProfissionalSaudeModal(true);
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
            </Box>
        </AdminLayout>
    );
}