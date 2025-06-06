import React from "react";
import { Snackbar, Alert, Pagination, Box, Fab, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Tooltip } from "@mui/material";
import { Add, Delete, InfoRounded } from "@mui/icons-material";
import SearchBar from "../components/SearchBar";
import VariableLayout from "../layouts/VariableLayout";
import ProfissionalSaudeModal from "../modals/ProfissionalSaudeModal";
import { ProfissionalSaude } from "../types/user";
import DeleteModal from "../modals/DeleteDialog";
import StylizedTitle from "../components/StylizedTitle";
import { UnidadeSaudeContext } from "../contexts/UnidadesSaudeContext";

export default function ProfissionalSaudeScreen() {
    const unidadeSaude = React.useContext(UnidadeSaudeContext);
    const [showProfissionalSaudeModal, setShowProfissionalSaudeModal] = React.useState(false);
    const [selectedProfissionalSaude, setSelectedProfissionalSaude] = React.useState<ProfissionalSaude | null>(null);
    const [profissionaisSaude, setProfissionaisSaude] = React.useState<ProfissionalSaude[]>([]);
    const [snackbar, setSnackbar] = React.useState({ open: false, type: '', message: '' });
    const [searchQuery, setSearchQuery] = React.useState<string>(''); // Armazena o último termo de busca
    const [showDeleteModal, setShowDeleteModal] = React.useState(false);

    // Estados para paginação
    const [page, setPage] = React.useState(1);
    const [totalPages, setTotalPages] = React.useState(1);
    const [showPagination, setShowPagination] = React.useState(false);

    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const handleFilter = (query: string) => {
        // Se houver busca, utiliza a rota de filtro; caso contrário, desabilita a paginação
        if (query.length >= 3) {
            setSearchQuery(query); // Salva o termo de busca mais recente
            setShowPagination(false);
            const baseUrl = import.meta.env.VITE_BACKEND_URL;
            const token = localStorage.getItem('@App:token');


            
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
        }
    };

    const getProfissionaisSaudePage = async (pageNumber: number) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/profissionais_saude/${pageNumber}/10`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`Error fetching profissionais de saúde. Status: ${response.status}. Mensagem: ${errorText}`);
                return;
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await response.json();
                console.log('Profissionais de saúde:', data);
                // Considera que a API retorna um objeto com 'items' e 'totalPages'
                setProfissionaisSaude(data.items);
                setTotalPages(data.totalPages);
                setShowPagination(true);
                setSearchQuery(''); // Garante que o searchQuery permaneça vazio para a paginação
            } else {
                const text = await response.text();
                console.error('Tipo de conteúdo inesperado. Esperado JSON, mas recebeu:', text);
            }
        } catch (error) {
            console.error('Error fetching profissionais de saúde:', error);
        }
    };

    const handleChangePage = (_event: any, value: number) => {
        setPage(value);
        getProfissionaisSaudePage(value);
    };

    React.useEffect(() => {
        // Se nenhum termo de busca foi inserido, carrega a primeira página
        if (!searchQuery) {
            getProfissionaisSaudePage(1);
        }
    }, []);

    const handleModalSubmit = (feedback: { type: string; message: string }) => {
        setSnackbar({ open: true, type: feedback.type, message: feedback.message });
        setShowProfissionalSaudeModal(false);
        // Atualiza a lista: se houver busca, usa o filtro; caso contrário, recarrega a página atual
        if (searchQuery) {
            handleFilter(searchQuery);
        } else {
            getProfissionaisSaudePage(page);
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
                    // Atualiza a lista: se houver busca, usa o filtro; caso contrário, recarrega a página atual
                    if (searchQuery) {
                        handleFilter(searchQuery);
                    } else {
                        getProfissionaisSaudePage(page);
                    }
                } else {
                    setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar profissional de saúde.' });
                }
            }).catch((error) => {
                console.error('Error deleting profissional de saúde:', error);
                setSnackbar({ open: true, type: 'error', message: 'Erro ao deletar profissional de saúde.' });
            }
        );
    };

    return (
        <VariableLayout>
            <Box id="container"
                sx={{
                    paddingTop: { xs: 4, sm: 4, md: 0 },
                }}
            >
            
                <StylizedTitle title="Terapeutas" />
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
                {/* Renderiza a paginação se disponível */}
                {showPagination && (
                    <Pagination
                        count={totalPages}
                        page={page}
                        onChange={handleChangePage}
                        color="primary"
                    />
                )}
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
        </VariableLayout>
    );
}