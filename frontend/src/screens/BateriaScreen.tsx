import { useParams } from "react-router-dom";
import { Questionario, Sessao, Alternativa, Pergunta } from "../types/questionario";
import { useState, useEffect } from "react";
import PacienteLayout from "../layouts/PacienteLayout";
import { Box, Button, Container, Divider, Paper, RadioGroup, Radio, Typography, Fade, Fab, TextField } from "@mui/material";
import { ArrowBack, ArrowForward } from "@mui/icons-material";
import HomeIcon from "@mui/icons-material/Home";
import ProgressBar from "../components/ProgressBar";
import { useNavigate } from "react-router-dom";
import AlternativaRadioItem from "../components/AlternativaRadioItem";
import AlternativaCheckItem from "../components/AlternativaCheckItem";
interface BateriaTestesCompleta {
    id: string;
    profissional_saude_id: string | null;
    paciente_id: string;
    questionario_id: string;
    data_aplicacao: string;
    respostas: {};
    observacoes: string | null;
    is_completo: boolean;
    created_at: string;
    updated_at: string;
}

interface BateriaCompletaResponse {
    bateria: BateriaTestesCompleta;
    questionario: Questionario;
}

// Valores iniciais vazios, mas válidos
const emptySessao: Sessao = {
    id: "",
    questionario_id: "",
    titulo: "",
    descricao: "",
    ordem: 0,
    pergunta_condicional: undefined,
    respostas_condicionais: [],
    created_at: "",
    updated_at: "",
    perguntas: []
};


const emptyPergunta: Pergunta = {
    id: "",
    sessao_id: "",
    texto: "",
    tipo_resposta: "",
    metodo_pontuacao: undefined,
    ordem: 0,
    is_obrigatoria: false,
    created_at: "",
    updated_at: "",
    alternativas: []
};

export default function BateriaScreen() {
    const navigate = useNavigate();
    const bateriaId = useParams().id;
    const [bateriaCompletaResponse, setBateriaCompletaResponse] = useState<BateriaCompletaResponse | null>(null);
    const [currentSessao, setCurrentSessao] = useState<Sessao>(emptySessao);
    const [currentPergunta, setCurrentPergunta] = useState<Pergunta>(emptyPergunta);
    const [alternativas, setAlternativas] = useState<Alternativa[]>([]);
    const [respostas, setRespostas] = useState<{ [key: string]: string | number | string[] }>({});
    const [fade, setFade] = useState(true);
    const [isComplete, setIsComplete] = useState(false);
    const isFirstPergunta = () => {
        return currentSessao.ordem === 1 && currentPergunta.ordem === 1;
    }

    const isLastPergunta = () => {
        if (!bateriaCompletaResponse) return false;

        const sessoes = bateriaCompletaResponse.questionario.sessoes;
        const lastSessao = sessoes[sessoes.length - 1];
        const perguntas = lastSessao.perguntas;
        const lastPergunta = perguntas[perguntas.length - 1];

        return (
            currentSessao.ordem === lastSessao.ordem &&
            currentPergunta.ordem === lastPergunta.ordem
        );
    }
    const primeiraPerguntaNaoRespondida = () => {
        if (!bateriaCompletaResponse) return;

        // Organiza as sessões por ordem
        const sessoesOrdenadas = [...bateriaCompletaResponse.questionario.sessoes]
            .sort((a, b) => a.ordem - b.ordem);

        // Percorre cada sessão em ordem
        for (const sessao of sessoesOrdenadas) {
            // Organiza as perguntas por ordem
            const perguntasOrdenadas = [...sessao.perguntas]
                .sort((a, b) => a.ordem - b.ordem);

            // Percorre cada pergunta em ordem
            for (const pergunta of perguntasOrdenadas) {
                // Verifica se a pergunta não foi respondida
                if (!respostas[pergunta.id]) {
                    // Atualiza os estados para essa pergunta não respondida
                    setCurrentSessao(sessao);
                    setCurrentPergunta(pergunta);
                    setAlternativas(pergunta.alternativas || []);

                    // Indica que encontrou uma pergunta não respondida
                    return true;
                }
            }
        }

        // Se chegou aqui, todas as perguntas foram respondidas
        // Navega para a última pergunta
        const ultimaSessao = sessoesOrdenadas[sessoesOrdenadas.length - 1];
        const perguntasUltimaSessao = [...ultimaSessao.perguntas]
            .sort((a, b) => a.ordem - b.ordem);
        const ultimaPergunta = perguntasUltimaSessao[perguntasUltimaSessao.length - 1];

        // Atualiza os estados para a última pergunta
        setCurrentSessao(ultimaSessao);
        setCurrentPergunta(ultimaPergunta);
        setAlternativas(ultimaPergunta.alternativas || []);

        return false; // Indica que não encontrou perguntas não respondidas
    };
    const fetchBateriaCompleta = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/${bateriaId}/completo`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                }
            );
            const data = await response.json();

            // Verifica se os dados têm a estrutura esperada
            if (data && data.questionario && data.questionario.sessoes &&
                data.questionario.sessoes.length > 0 &&
                data.questionario.sessoes[0].perguntas &&
                data.questionario.sessoes[0].perguntas.length > 0) {

                setBateriaCompletaResponse(data);
                setRespostas(data.bateria.respostas || {});
                setCurrentSessao(data.questionario.sessoes[0]);
                setCurrentPergunta(data.questionario.sessoes[0].perguntas[0]);
                setAlternativas(data.questionario.sessoes[0].perguntas[0].alternativas || []);
            } else {
                console.error("Dados incompletos recebidos da API");
            }
        } catch (error) {
            console.error("Error fetching bateria completa:", error);
        }
    }
    const fetchUpdateBateria = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/${bateriaId}/respostas`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                    body: JSON.stringify({
                        respostas,
                    }),
                }
            );
            const data = await response.json();
            console.log("Bateria atualizada com sucesso:", data);
        } catch (error) {
            console.error("Error updating bateria:", error);
        }
    }
    useEffect(() => {
        fetchBateriaCompleta();
    }, []);
    useEffect(() => {
        primeiraPerguntaNaoRespondida();
    }
        , [bateriaCompletaResponse]);

    // Cálculo do total de perguntas e respondidas
    const totalPerguntas = bateriaCompletaResponse
        ? bateriaCompletaResponse.questionario.sessoes.reduce((acc, sessao) => acc + sessao.perguntas.length, 0)
        : 0;
    const respondidas = Object.keys(respostas).length;

    // Função para avançar para a próxima pergunta/sessão
    const handleNext = async () => {
        if (isLastPergunta()) return;

        setFade(false);

        try {
            // Salva as respostas no servidor antes de avançar
            await fetchUpdateBateria();

            // Obtenha a próxima pergunta na sessão atual
            const currentSessaoPerguntas = currentSessao.perguntas || [];
            const currentPerguntaIndex = currentSessaoPerguntas.findIndex(p => p.id === currentPergunta.id);

            if (currentPerguntaIndex < currentSessaoPerguntas.length - 1) {
                // Avançar para a próxima pergunta na mesma sessão
                setCurrentPergunta(currentSessaoPerguntas[currentPerguntaIndex + 1]);
                setAlternativas(currentSessaoPerguntas[currentPerguntaIndex + 1].alternativas || []);
            } else {
                // Avançar para a próxima sessão
                if (bateriaCompletaResponse) {
                    const currentSessaoIndex = bateriaCompletaResponse.questionario.sessoes.findIndex(s => s.id === currentSessao.id);
                    if (currentSessaoIndex >= 0 &&
                        bateriaCompletaResponse.questionario.sessoes[currentSessaoIndex + 1]) {
                        const nextSessao = bateriaCompletaResponse.questionario.sessoes[currentSessaoIndex + 1];
                        setCurrentSessao(nextSessao);
                        if (nextSessao.perguntas && nextSessao.perguntas.length > 0) {
                            setCurrentPergunta(nextSessao.perguntas[0]);
                            setAlternativas(nextSessao.perguntas[0].alternativas || []);
                        }
                    }
                }
            }

            // Depois que tudo for atualizado, ativa a animação novamente
            setFade(true);
        } catch (error) {
            console.error("Erro ao salvar resposta ou navegar:", error);
            // Em caso de erro, reativa a animação para não deixar a interface congelada
            setFade(true);
        }
    };

    // Função para voltar para a pergunta/sessão anterior
    const handlePrevious = async () => {
        if (isFirstPergunta()) return;

        setFade(false);

        try {
            // Salva as respostas no servidor antes de voltar
            await fetchUpdateBateria();

            // Obtenha a pergunta anterior na sessão atual
            const currentSessaoPerguntas = currentSessao.perguntas || [];
            const currentPerguntaIndex = currentSessaoPerguntas.findIndex(p => p.id === currentPergunta.id);

            if (currentPerguntaIndex > 0) {
                // Voltar para a pergunta anterior na mesma sessão
                setCurrentPergunta(currentSessaoPerguntas[currentPerguntaIndex - 1]);
                setAlternativas(currentSessaoPerguntas[currentPerguntaIndex - 1].alternativas || []);
            } else {
                // Voltar para a última pergunta da sessão anterior
                if (bateriaCompletaResponse) {
                    const currentSessaoIndex = bateriaCompletaResponse.questionario.sessoes.findIndex(s => s.id === currentSessao.id);
                    if (currentSessaoIndex > 0) {
                        const prevSessao = bateriaCompletaResponse.questionario.sessoes[currentSessaoIndex - 1];
                        setCurrentSessao(prevSessao);
                        if (prevSessao.perguntas && prevSessao.perguntas.length > 0) {
                            const lastPergunta = prevSessao.perguntas[prevSessao.perguntas.length - 1];
                            setCurrentPergunta(lastPergunta);
                            setAlternativas(lastPergunta.alternativas || []);
                        }
                    }
                }
            }

            // Depois que tudo for atualizado, ativa a animação novamente
            setFade(true);
        } catch (error) {
            console.error("Erro ao salvar resposta ou navegar:", error);
            // Em caso de erro, reativa a animação para não deixar a interface congelada
            setFade(true);
        }
    };

    useEffect(() => {
        if (respondidas === totalPerguntas) {
            setIsComplete(true);
        }
        else {
            setIsComplete(false);
        }
    }, [respostas]);
    //@bateria_testes_bp.route('/<id>/complete', methods=['PUT'])
    const handleCompleteBateria = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/${bateriaId}/complete`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
                    },
                    body: JSON.stringify({
                        respostas,
                    }),
                }
            );
            const data = await response.json();
            navigate("/paciente-baterias-list");
            console.log("Bateria atualizada com sucesso:", data);

        }
        catch (error) {
            console.error("Error updating bateria:", error);
        }

    }

    // Verifica se o carregamento inicial foi concluído
    if (!bateriaCompletaResponse) {
        return <PacienteLayout>Carregando...</PacienteLayout>;
    }



    return (
        <PacienteLayout>
            <Container maxWidth="md" sx={{ marginTop: 4 }}>

                <Paper elevation={1} sx={{ padding: 2, margin: 2, textAlign: "center" }}>
                    <Typography variant="h5" component="h2">
                        {bateriaCompletaResponse.questionario.titulo}
                    </Typography>
                    <Typography variant="body1" component="p">
                        {bateriaCompletaResponse.questionario.descricao}
                    </Typography>
                </Paper>
                <Divider sx={{ margin: 2 }} />

                <Box sx={{ paddingX: 5 }}>

                    <ProgressBar total={totalPerguntas} current={respondidas} />
                </Box>

                <Fade in={fade} timeout={300}>
                    <Box>
                        <Paper elevation={1} sx={{ padding: 2, margin: 2 }}>
                            <Typography variant="h6" component="h3">
                                Sessão: {currentSessao.titulo}
                            </Typography>
                            <Typography variant="body1" component="p">
                                {currentSessao.descricao}
                            </Typography>
                        </Paper>

                        <Paper elevation={1} sx={{ padding: 2, margin: 2 }}>
                            <Typography variant="h6" component="h3">
                                {currentPergunta.texto}
                            </Typography>
                     
                            <Box sx={{ display: "flex", flexDirection: "column", marginTop: 2 }}>
                                {
                                    currentPergunta.tipo_resposta === "texto_puro" && (
                                        <Box sx={{ display: "flex", flexDirection: "column" }}>
                                            <TextField
                                                label="Resposta"
                                                variant="outlined"
                                                value={respostas[currentPergunta.id] || ""}
                                                onChange={(e) => {
                                                    setRespostas({ ...respostas, [currentPergunta.id]: e.target.value });
                                                }}
                                                multiline
                                                rows={4}
                                                fullWidth
                                                sx={{ marginBottom: 2 }}
                                            />
                                        </Box>
                                    )
                                }
                                {currentPergunta.tipo_resposta === "numerica" && (

                                    <Box sx={{ display: "flex", flexDirection: "column" }}>
                                        <TextField
                                            label="Resposta"
                                            variant="outlined"
                                            value={respostas[currentPergunta.id] || ""}
                                            onChange={(e) => {
                                                setRespostas({ ...respostas, [currentPergunta.id]: e.target.value });
                                            }}
                                            type="number"
                                            fullWidth
                                            sx={{ marginBottom: 2 }}
                                        />
                                    </Box>
                                )}
                                {currentPergunta.tipo_resposta === "data" && (
                                    <Box sx={{ display: "flex", flexDirection: "column" }}>
                                        <TextField
                                            label="Resposta"
                                            variant="outlined"
                                            value={respostas[currentPergunta.id] || ""}
                                            onChange={(e) => {
                                                setRespostas({ ...respostas, [currentPergunta.id]: e.target.value });
                                            }}
                                            type="date"
                                            fullWidth
                                            sx={{ marginBottom: 2 }}
                                        />
                                    </Box>
                                )}
                                {currentPergunta.tipo_resposta === "multipla_escolha" && (
                                    <Box>
                                        {alternativas.map((alternativa) => (
                                            <AlternativaCheckItem
                                                key={alternativa.id}
                                                alternativa={alternativa}
                                                respostas={Array.isArray(respostas[currentPergunta.id]) ? respostas[currentPergunta.id] as string[] : []}
                                                onChange={(alternativaId, checked) => {
                                                    // Obtém o array atual de respostas ou cria um novo
                                                    const respostasPergunta = Array.isArray(respostas[currentPergunta.id])
                                                        ? [...(respostas[currentPergunta.id] as string[])]
                                                        : [];

                                                    if (checked) {
                                                        // Adiciona a alternativa às respostas
                                                        respostasPergunta.push(alternativaId);
                                                    } else {
                                                        // Remove a alternativa das respostas
                                                        const index = respostasPergunta.indexOf(alternativaId);
                                                        if (index > -1) {
                                                            respostasPergunta.splice(index, 1);
                                                        }
                                                    }

                                                    setRespostas({ ...respostas, [currentPergunta.id]: respostasPergunta });
                                                }}
                                            />
                                        ))}
                                    </Box>
                                )}
                                {
                                    currentPergunta.tipo_resposta != "multipla_escolha" && 
                                    currentPergunta.tipo_resposta != "texto_puro" && 
                                    currentPergunta.tipo_resposta != "numerica" &&
                                    currentPergunta.tipo_resposta != "data" &&
                                    (
                                        <RadioGroup
                                            value={respostas[currentPergunta.id] || ""}
                                            onChange={(e) => {
                                                setRespostas({ ...respostas, [currentPergunta.id]: e.target.value });
                                            }}
                                        >
                                            {alternativas.map((alternativa) => (
                                                <AlternativaRadioItem
                                                    key={alternativa.id}
                                                    alternativa={alternativa}
                                                    selected={respostas[currentPergunta.id] === alternativa.id}
                                                    onChange={(alternativaId) => {
                                                        setRespostas({ ...respostas, [currentPergunta.id]: alternativaId });
                                                    }}
                                                />
                                            ))}
                                        </RadioGroup>
                                    )
                                    
                                }
                            </Box>
                        </Paper>
                    </Box>
                </Fade>

                <Box sx={{ display: "flex", justifyContent: "space-between", marginTop: 2, marginBottom: 4 }}>
                    <Button
                        variant="contained"
                        color="primary"
                        startIcon={<ArrowBack />}
                        onClick={handlePrevious}
                        disabled={isFirstPergunta()}
                    >
                        Anterior
                    </Button>
                    {

                        isComplete ? (
                            <Button
                                variant="contained"
                                color="success"
                                onClick={handleCompleteBateria}
                            >
                                Concluir
                            </Button>
                        ) : (
                            <Button
                                variant="contained"
                                color="primary"
                                endIcon={<ArrowForward />}
                                onClick={handleNext}
                                disabled={isLastPergunta() || !respostas[currentPergunta.id]}
                            >
                                Próxima
                            </Button>
                        )
                    }

                </Box>

                {/* FAB para navegar para /paciente-baterias-list */}
                <Fab
                    color="primary"
                    aria-label="voltar para lista"
                    sx={{ position: "fixed", bottom: 32, right: 32, zIndex: 9999 }}
                    onClick={() => navigate("/paciente-baterias-list")}
                >
                    <HomeIcon />
                </Fab>

            </Container>
        </PacienteLayout>
    )
}