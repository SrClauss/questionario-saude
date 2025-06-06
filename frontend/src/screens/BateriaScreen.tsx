import { useParams } from "react-router-dom";
import { Questionario, Sessao, Alternativa, Pergunta,  RespostasEspecificasInterface, FaixaDePontuacaoInterface, RoleDoUsuarioInterface } from "../types/questionario";
import { useState, useEffect } from "react";
import PacienteLayout from "../layouts/PacienteLayout";
import { Box, Button, Container, Divider, Paper, RadioGroup, Typography, Fade, Fab, TextField } from "@mui/material";
import { ArrowBack, ArrowForward } from "@mui/icons-material";
import HomeIcon from "@mui/icons-material/Home";
import ProgressBar from "../components/ProgressBar";
import { useNavigate } from "react-router-dom";
import AlternativaRadioItem from "../components/AlternativaRadioItem";
import { auth } from "../utils/auth";
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
    regras_visibilidade: [],
    logica_principal_entre_regras: "OR",
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
    const [alternativas, setAlternativas] = useState<Alternativa[]>([]); // TODO: verificar se esta linha está correta
    const [respostas, setRespostas] = useState<{ [key: string]: string | number | string[] | null }>({});
    const [fade, setFade] = useState(true);
    const [isComplete, setIsComplete] = useState(false);
    const [todasPerguntas, setTodasPerguntas] = useState<Pergunta[]>([]);
    const [perfilUsuario, setPerfilUsuario] = useState<any>(null);

    useEffect(() => {
        const userData = auth.getUserData();
        setPerfilUsuario(userData);
    }, []);

    // Helper para calcular pontuação (simplificado)
    const calcularPontuacao = (
        perguntasParaCalculoIds: string[],
        resps: { [key: string]: string | number | string[] | null },
        todasP: Pergunta[]
    ): number => {
        let pontuacaoTotal = 0;
        for (const perguntaId of perguntasParaCalculoIds) {
            const respostaDada = resps[perguntaId];
            if (respostaDada !== undefined) {
                const pergunta = todasP.find(p => p.id === perguntaId);
                if (pergunta?.alternativas) {
                    const alternativaSelecionada = pergunta.alternativas.find(
                        alt => alt.id === respostaDada || alt.texto === respostaDada
                    );
                    if (alternativaSelecionada && typeof alternativaSelecionada.valor === 'number') {
                        pontuacaoTotal += alternativaSelecionada.valor;
                    }
                } else if (typeof respostaDada === 'number') {
                    pontuacaoTotal += respostaDada;
                }
            }
        }
        return pontuacaoTotal;
    };

    const avaliarRegrasDeVisibilidade = (
        sessao: Sessao,
        resps: { [key: string]: string | number | string[] | null },
        todasP: Pergunta[],
        perfilUser?: any
    ): boolean => {
        if (!sessao.regras_visibilidade || sessao.regras_visibilidade.length === 0) {
            return true; // Sem regras, sempre visível
        }

        const resultadosRegras: boolean[] = sessao.regras_visibilidade.map(regra => {
            switch (regra.tipo_regra) {
                case "RESPOSTA_ESPECIFICA":
                    const rResp = regra as RespostasEspecificasInterface;
                    const respAlvo = resps[rResp.pergunta_alvo_id];
                    if (respAlvo === undefined) return false;
                    if (Array.isArray(respAlvo)) { // Múltipla escolha
                        return rResp.logica_respostas === "AND"
                            ? rResp.respostas_necessarias_ids.every(idNec => respAlvo.includes(idNec))
                            : rResp.respostas_necessarias_ids.some(idNec => respAlvo.includes(idNec));
                    } else { // Resposta única
                        return rResp.logica_respostas === "AND"
                            ? rResp.respostas_necessarias_ids.every(idNec => idNec === respAlvo)
                            : rResp.respostas_necessarias_ids.includes(respAlvo as string);
                    }
                case "FAIXA_DE_PONTUACAO":
                    const rPont = regra as FaixaDePontuacaoInterface;
                    const pontuacao = calcularPontuacao(rPont.perguntas_para_calculo_ids, resps, todasP);
                    return pontuacao >= rPont.pontuacao_minima_exigida && pontuacao <= rPont.pontuacao_maxima_exigida;
                case "ROLE_USUARIO":
                    const rRole = regra as RoleDoUsuarioInterface;
                    return perfilUser?.role ? rRole.roles_permitidos.includes(perfilUser.role) : false;
                default:
                    return false;
            }
        });

        return sessao.logica_principal_entre_regras === "AND"
            ? resultadosRegras.every(r => r)
            : resultadosRegras.some(r => r);
    };

    const getSessoesVisiveis = (): Sessao[] => {
        if (!bateriaCompletaResponse?.questionario?.sessoes || todasPerguntas.length === 0 || perfilUsuario === undefined) return [];
        return bateriaCompletaResponse.questionario.sessoes
            .filter(s => avaliarRegrasDeVisibilidade(s, respostas, todasPerguntas, perfilUsuario))
            .sort((a, b) => a.ordem - b.ordem);
    };

    const isFirstPergunta = () => {
        const sessoesVisiveis = getSessoesVisiveis();
        if (sessoesVisiveis.length === 0) return true;
        const primeiraSessaoVisivel = sessoesVisiveis[0];
        if (!primeiraSessaoVisivel.perguntas || primeiraSessaoVisivel.perguntas.length === 0) return true;
        const primeiraPerguntaDaSessao = [...primeiraSessaoVisivel.perguntas].sort((a, b) => a.ordem - b.ordem)[0];
        return currentSessao.id === primeiraSessaoVisivel.id && currentPergunta.id === primeiraPerguntaDaSessao.id;
    };

    const isLastPergunta = () => {
        const sessoesVisiveis = getSessoesVisiveis();
        if (sessoesVisiveis.length === 0) return true;
        const ultimaSessaoVisivel = sessoesVisiveis[sessoesVisiveis.length - 1];
        if (!ultimaSessaoVisivel.perguntas || ultimaSessaoVisivel.perguntas.length === 0) return true;
        const perguntasDaSessao = [...ultimaSessaoVisivel.perguntas].sort((a, b) => a.ordem - b.ordem);
        const ultimaPerguntaDaSessao = perguntasDaSessao[perguntasDaSessao.length - 1];
        return currentSessao.id === ultimaSessaoVisivel.id && currentPergunta.id === ultimaPerguntaDaSessao.id;
    };

    const primeiraPerguntaNaoRespondida = () => {
        if (!bateriaCompletaResponse || todasPerguntas.length === 0 || perfilUsuario === undefined) return;

        const sessoesVisiveisOrdenadas = getSessoesVisiveis();

        for (const sessao of sessoesVisiveisOrdenadas) {
            const perguntasOrdenadas = [...(sessao.perguntas || [])]
                .sort((a, b) => a.ordem - b.ordem);

            for (const pergunta of perguntasOrdenadas) {
                if (!respostas[pergunta.id]) {
                    setCurrentSessao(sessao);
                    setCurrentPergunta(pergunta);
                    setAlternativas(pergunta.alternativas || []);
                    return true;
                }
            }
        }

        if (sessoesVisiveisOrdenadas.length > 0) {
            const ultimaSessaoVisivel = sessoesVisiveisOrdenadas[sessoesVisiveisOrdenadas.length - 1];
            const perguntasUltimaSessao = [...(ultimaSessaoVisivel.perguntas || [])].sort((a, b) => a.ordem - b.ordem);
            if (perguntasUltimaSessao.length > 0) {
                const ultimaPergunta = perguntasUltimaSessao[perguntasUltimaSessao.length - 1];
                setCurrentSessao(ultimaSessaoVisivel);
                setCurrentPergunta(ultimaPergunta);
                setAlternativas(ultimaPergunta.alternativas || []);
            } else {
                setCurrentSessao(ultimaSessaoVisivel);
                setCurrentPergunta(emptyPergunta);
                setAlternativas([]);
            }
        } else {
            setCurrentSessao(emptySessao);
            setCurrentPergunta(emptyPergunta);
            setAlternativas([]);
        }
        return false;
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
            if (data && data.questionario && data.questionario.sessoes) {

                setBateriaCompletaResponse(data);
                setRespostas(data.bateria.respostas || {});

                const perguntasList: Pergunta[] = [];
                data.questionario.sessoes.forEach((s: Sessao) => {
                    if (s.perguntas) {
                        perguntasList.push(...s.perguntas);
                    }
                });
                setTodasPerguntas(perguntasList);
                // A definição da sessão/pergunta inicial será feita pelo useEffect que chama primeiraPerguntaNaoRespondida
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
        fetchBateriaCompleta(); // Busca inicial dos dados da bateria
    }, [bateriaId]); // Adiciona bateriaId como dependência para refazer o fetch se o ID mudar

    useEffect(() => {
        if (bateriaCompletaResponse && todasPerguntas.length > 0 && perfilUsuario !== undefined) {
            const sessoesDoQuestionario = bateriaCompletaResponse.questionario.sessoes;
            let respostasModificadas = false;
            const respostasCopia = { ...respostas }; // Trabalhar com uma cópia

            // Etapa 1: Deletar respostas de sessões que se tornaram NÃO visíveis
            sessoesDoQuestionario.forEach(sessao => {
                // Avalia a visibilidade com base na cópia atual das respostas
                const isVisivel = avaliarRegrasDeVisibilidade(sessao, respostasCopia, todasPerguntas, perfilUsuario);
                if (!isVisivel && sessao.perguntas) {
                    sessao.perguntas.forEach(pergunta => {
                        if (pergunta.id in respostasCopia) { // Se existe uma resposta para esta pergunta
                            delete respostasCopia[pergunta.id]; // Deleta a resposta
                            respostasModificadas = true;
                        }
                    });
                }
            });

            // Etapa 2: Limpar 'null' de perguntas em sessões que se tornaram VISÍVEIS
            sessoesDoQuestionario.forEach(sessao => {
                const isVisivel = avaliarRegrasDeVisibilidade(sessao, respostasCopia, todasPerguntas, perfilUsuario);
                if (isVisivel && sessao.perguntas) {
                    sessao.perguntas.forEach(pergunta => {
                        if (pergunta.id in respostasCopia && respostasCopia[pergunta.id] === null) {
                            delete respostasCopia[pergunta.id]; // Remove a resposta 'null', tornando-a "não respondida"
                            respostasModificadas = true;
                        }
                    });
                }
            });

            if (respostasModificadas) {
                setRespostas(respostasCopia); // Atualiza o estado com a cópia modificada
                return; // Retorna para esperar a re-execução do useEffect com o estado 'respostas' atualizado
            } // Não chama primeiraPerguntaNaoRespondida aqui para evitar auto-avanço desnecessário
        }
    }, [bateriaCompletaResponse, respostas, todasPerguntas, perfilUsuario]);

    // useEffect para inicializar a primeira pergunta não respondida
    useEffect(() => {
        if (bateriaCompletaResponse && todasPerguntas.length > 0 && perfilUsuario !== undefined && !currentPergunta.id) {
            // Apenas na inicialização, se não houver pergunta atual e os dados estiverem carregados
            primeiraPerguntaNaoRespondida();
        }
    }, [bateriaCompletaResponse, todasPerguntas, perfilUsuario, currentPergunta.id, bateriaId]); // bateriaId para re-inicializar se o componente for reutilizado para outra bateria

    // Cálculo do total de perguntas e respondidas
    const totalPerguntasVisiveis = getSessoesVisiveis().reduce((acc, sessao) => acc + (sessao.perguntas?.length || 0), 0);
    const respondidas = Object.keys(respostas).length;

    const encontrarProximaPerguntaVisivel = (
        sessaoAtualId: string,
        perguntaAtualId: string,
        direcao: 'next' | 'prev'
    ): { sessao: Sessao, pergunta: Pergunta } | null => {
        if (!bateriaCompletaResponse?.questionario?.sessoes || todasPerguntas.length === 0 || perfilUsuario === undefined) return null;

        const sessoesGlobaisOrdenadas = [...bateriaCompletaResponse.questionario.sessoes].sort((a, b) => a.ordem - b.ordem);
        let sessaoAtualIdx = sessoesGlobaisOrdenadas.findIndex(s => s.id === sessaoAtualId);

        if (sessaoAtualIdx === -1 && sessoesGlobaisOrdenadas.length > 0) { // Fallback se currentSessao for emptySessao
            sessaoAtualIdx = direcao === 'next' ? -1 : sessoesGlobaisOrdenadas.length;
        }

        if (direcao === 'next') {
            let perguntaAtualIdx = sessaoAtualIdx === -1 ? -1 : (sessoesGlobaisOrdenadas[sessaoAtualIdx].perguntas || []).sort((a, b) => a.ordem - b.ordem).findIndex(p => p.id === perguntaAtualId);
            perguntaAtualIdx++;

            for (let i = sessaoAtualIdx === -1 ? 0 : sessaoAtualIdx; i < sessoesGlobaisOrdenadas.length; i++) {
                const candidataSessao = sessoesGlobaisOrdenadas[i];
                if (i > sessaoAtualIdx) perguntaAtualIdx = 0;

                if (!avaliarRegrasDeVisibilidade(candidataSessao, respostas, todasPerguntas, perfilUsuario)) continue;

                const perguntasDaSessao = [...(candidataSessao.perguntas || [])].sort((a, b) => a.ordem - b.ordem);
                if (perguntaAtualIdx < perguntasDaSessao.length) {
                    return { sessao: candidataSessao, pergunta: perguntasDaSessao[perguntaAtualIdx] };
                }
            }
        } else { // prev
            let perguntaAtualIdx = sessaoAtualIdx === sessoesGlobaisOrdenadas.length ? Infinity : (sessoesGlobaisOrdenadas[sessaoAtualIdx].perguntas || []).sort((a, b) => a.ordem - b.ordem).findIndex(p => p.id === perguntaAtualId);
            perguntaAtualIdx--;

            for (let i = sessaoAtualIdx === sessoesGlobaisOrdenadas.length ? sessoesGlobaisOrdenadas.length - 1 : sessaoAtualIdx; i >= 0; i--) {
                const candidataSessao = sessoesGlobaisOrdenadas[i];
                if (i < sessaoAtualIdx) perguntaAtualIdx = (candidataSessao.perguntas || []).length - 1;

                if (!avaliarRegrasDeVisibilidade(candidataSessao, respostas, todasPerguntas, perfilUsuario)) continue;

                const perguntasDaSessao = [...(candidataSessao.perguntas || [])].sort((a, b) => a.ordem - b.ordem);
                if (perguntaAtualIdx >= 0 && perguntaAtualIdx < perguntasDaSessao.length) {
                    return { sessao: candidataSessao, pergunta: perguntasDaSessao[perguntaAtualIdx] };
                }
            }
        }
        return null;
    };

    const handleNext = async () => {
        if (isLastPergunta()) return;
        setFade(false);
        try {
            await fetchUpdateBateria();
            const proxima = encontrarProximaPerguntaVisivel(currentSessao.id, currentPergunta.id, 'next');
            if (proxima) {
                setCurrentSessao(proxima.sessao);
                setCurrentPergunta(proxima.pergunta);
                setAlternativas(proxima.pergunta.alternativas || []);
            }
            setFade(true);
        } catch (error) {
            console.error("Erro ao salvar resposta ou navegar:", error);
            setFade(true);
        }
    };

    const handlePrevious = async () => {
        if (isFirstPergunta()) return;
        setFade(false);
        try {
            await fetchUpdateBateria();
            const anterior = encontrarProximaPerguntaVisivel(currentSessao.id, currentPergunta.id, 'prev');
            if (anterior) {
                setCurrentSessao(anterior.sessao);
                setCurrentPergunta(anterior.pergunta);
                setAlternativas(anterior.pergunta.alternativas || []);
            }
            setFade(true);
        } catch (error) {
            console.error("Erro ao salvar resposta ou navegar:", error);
            setFade(true);
        }
    };

    useEffect(() => {
        const sessoesVisiveis = getSessoesVisiveis();
        if (sessoesVisiveis.length === 0 && totalPerguntasVisiveis > 0 && bateriaCompletaResponse) {
             setIsComplete(true); // Considera completo pois não há o que responder
             return;
        }
        const respondidasVisiveis = Object.keys(respostas).filter(perguntaId =>
            sessoesVisiveis.some(s => s.perguntas?.some(p => p.id === perguntaId))
        ).length;

        if (totalPerguntasVisiveis > 0 && respondidasVisiveis === totalPerguntasVisiveis) {
            setIsComplete(true);
        } else if (totalPerguntasVisiveis === 0 && bateriaCompletaResponse) { // Nenhuma pergunta em sessões visíveis
            setIsComplete(true);
        }
        else {
            setIsComplete(false);
        }
    }, [respostas, todasPerguntas, perfilUsuario, bateriaCompletaResponse]);

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
    if (!bateriaCompletaResponse || todasPerguntas.length === 0 || perfilUsuario === undefined) {
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

                    <ProgressBar total={totalPerguntasVisiveis} current={Object.keys(respostas).filter(pid => getSessoesVisiveis().some(s => s.perguntas?.some(p => p.id === pid))).length} />
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
                                    (currentPergunta.tipo_resposta === "texto"
                                    ||currentPergunta.tipo_resposta === "texto_puro"
                                    ) && (
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
                                            slotProps={{
                                                inputLabel:{
                                                    shrink: true
                                                }
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
