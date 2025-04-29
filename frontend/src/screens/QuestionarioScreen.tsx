import React, { useState } from "react";
import {
    Box,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    IconButton,
    Tooltip,
    Button,
    Snackbar,
    Alert
} from "@mui/material";
import { Delete, InfoRounded, Add } from "@mui/icons-material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import { useNavigate } from "react-router-dom";

interface Questionario {
    id: string;
    titulo: string;
    // Outras propriedades podem existir, mas não serão exibidas
}

export default function QuestionarioScreen() {
    const [questionarios, setQuestionarios] = useState<Questionario[]>([]);
    const [snackbar, setSnackbar] = useState({
        open: false,
        message: "",
        type: ""
    });
    const [searchQuery, setSearchQuery] = useState<string>("");
    const navigate = useNavigate();
    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    const handleFilter = (query: string) => {
        if (query.length < 3) return;
        setSearchQuery(query);

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        const url = `${baseUrl}/questionario/find_by_title_or_description/${query}/`;

        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
            .then((response) => response.json())
            .then((data) => {
                setQuestionarios(data);
            })
            .catch((error) => {
                console.error("Error fetching questionários:", error);
                setSnackbar({
                    open: true,
                    type: "error",
                    message: "Erro ao buscar questionários"
                });
            });
    };

    const handleDelete = (id: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        const url = `${baseUrl}/questionario/${id}`;

        fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
            .then((response) => response.json())
            .then((data) => {
                setSnackbar({
                    open: true,
                    type: "success",
                    message: data.message || "Questionário deletado com sucesso"
                });
                if (searchQuery) {
                    handleFilter(searchQuery);
                }
            })
            .catch((error) => {
                console.error("Error deleting questionário:", error);
                setSnackbar({
                    open: true,
                    type: "error",
                    message: "Erro ao deletar questionário"
                });
            });
    };

    return (
        <AdminLayout>
            <Box sx={{ marginBottom: 2 }}>
                <SearchBar onSearch={handleFilter} />
            </Box>
            <Box sx={{ display: "flex", justifyContent: "flex-end", marginBottom: 2 }}>
                <Button onClick={() => navigate("/cadastro-questionario")} variant="contained" color="primary" startIcon={<Add />}>
                    Cadastrar Questionário
                </Button>
            </Box>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Título</TableCell>
                        <TableCell>Ações</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {questionarios.map((q) => (
                        <TableRow key={q.id}>
                            <TableCell>{q.titulo}</TableCell>
                            <TableCell>
                                <Tooltip title="Info">
                                    <IconButton color="primary">
                                        <InfoRounded />
                                    </IconButton>
                                </Tooltip>
                                <Tooltip title="Delete">
                                    <IconButton
                                        color="error"
                                        onClick={() => handleDelete(q.id)}
                                    >
                                        <Delete />
                                    </IconButton>
                                </Tooltip>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            >
                <Alert
                    onClose={handleSnackbarClose}
                    severity={snackbar.type as "error" | "success" | "info" | "warning"}
                    sx={{ width: "100%" }}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </AdminLayout>
    );
}