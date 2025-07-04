import { useEffect, useState, useCallback } from "react";
import MedicoLayout from "../layouts/MedicoLayout";
import { auth } from "../utils/auth";
import { Box, Typography, Button, Stack } from "@mui/material";
import StylizedTitle from "../components/StylizedTitle";
import { AvaliacaoFetch } from "../components/ComponenteAvaliacao"; // Reutilizando a interface
import ComponenteAvaliacaoMedico from "../components/ComponenteAvaliacaoMedico";
import SearchBar from "../components/SearchBar"; // Assumindo que você tem este componente

export default function PesquisaAvaliacoesMedicoScreen() {
    const medico = auth.getProfile();
    const [avaliacoes, setAvaliacoes] = useState<AvaliacaoFetch[]>([]);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [statusFiltro, setStatusFiltro] = useState<"todas" | "abertas" | "fechadas">("abertas"); // Padrão para abertas
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const fetchAvaliacoesFiltradas = useCallback(async (medicoId: string, query: string, status: string) => {
        if (!medicoId) return;

        setIsLoading(true);
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");

        // Constrói a URL com os parâmetros de query
        let url = `${baseUrl}/avaliacoes/por_medico_e_filtro_paciente/${medicoId}?status=${status}`;
        if (query.trim() !== "") {
            url += `&nome_paciente=${encodeURIComponent(query.trim())}`;
        }

        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            const data = await response.json();
            if (response.ok) {
                setAvaliacoes(data);
            } else {
                console.error("Error fetching avaliacoes:", data.error || "Erro desconhecido");
                setAvaliacoes([]); // Limpa em caso de erro
            }
        } catch (error) {
            console.error("Error fetching avaliacoes:", error);
            setAvaliacoes([]); // Limpa em caso de erro de rede
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        if (medico?.id) {
            // Carrega inicialmente com o status padrão e sem query de nome
            fetchAvaliacoesFiltradas(medico.id, searchQuery, statusFiltro);
        }
    }, [medico?.id, statusFiltro, fetchAvaliacoesFiltradas]); // Adicionado searchQuery aqui se quiser busca automática ao digitar, mas geralmente é melhor com um botão ou debounce

    const handleSearch = (query: string) => {
        setSearchQuery(query);
        if (medico?.id) {
            fetchAvaliacoesFiltradas(medico.id, query, statusFiltro);
        }
    };

    const handleStatusChange = (newStatus: "todas" | "abertas" | "fechadas") => {
        setStatusFiltro(newStatus);
        // A busca será refeita pelo useEffect devido à mudança no statusFiltro
    };

    return (
        <MedicoLayout>
            <Box id="container" sx={{ paddingTop: { xs: 4, sm: 4, md: 0 } }}>
                <StylizedTitle title="Pesquisar Avaliações" />

                <SearchBar onSearch={handleSearch} />

                <Stack direction="row" spacing={1} sx={{ my: 2, justifyContent: 'center' }}>
                    <Button
                        variant={statusFiltro === "abertas" ? "contained" : "outlined"}
                        onClick={() => handleStatusChange("abertas")}
                    >
                        Abertas
                    </Button>
                    <Button
                        variant={statusFiltro === "fechadas" ? "contained" : "outlined"}
                        onClick={() => handleStatusChange("fechadas")}
                    >
                        Fechadas
                    </Button>
                    <Button
                        variant={statusFiltro === "todas" ? "contained" : "outlined"}
                        onClick={() => handleStatusChange("todas")}
                    >
                        Todas
                    </Button>
                </Stack>

                {isLoading ? (
                    <Typography sx={{ textAlign: 'center', my: 2 }}>Carregando...</Typography>
                ) : (
                    <Box>
                        {avaliacoes.length > 0 ? (
                            avaliacoes.map((avaliacao) => (
                                <ComponenteAvaliacaoMedico
                                    key={avaliacao.avaliacao.id}
                                    avaliacaoFetch={avaliacao}
                                />
                            ))
                        ) : (
                            <Typography sx={{ textAlign: 'center', my: 2 }}>
                                Nenhuma avaliação encontrada para os critérios informados.
                            </Typography>
                        )}
                    </Box>
                )}
            </Box>
        </MedicoLayout>
    );
}