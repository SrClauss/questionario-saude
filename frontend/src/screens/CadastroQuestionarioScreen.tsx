import React, { useState, useEffect, useCallback } from "react"; // Adicionado useCallback
import {
  Box,
  Button,
  TextField,
  Typography,
  Snackbar,
  Alert,
  Divider,
  IconButton,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  styled,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  CircularProgress,
  ListItemIcon,
  ListItemButton,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import DeleteIcon from '@mui/icons-material/Delete';

import EditIcon from '@mui/icons-material/Edit';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import AdminLayout from "../layouts/AdminLayout";
import FontesLiteraturaModal from "../modals/FontesLiteraturaModal";
import SessaoModal from "../modals/SessaoModal";
import PerguntaModal from "../modals/PerguntaModal";
import AlternativaModal from "../modals/AlternativaModal";
import AlternativaEscolhaUnicaModal from "../modals/AlternativaEscolhaUnicaModal";
import { Sessao, Pergunta, Alternativa } from "../types/questionario";


const CompactReadOnlyBox = styled(Box)(({ theme }) => ({
  border: '1px solid #ccc',
  borderRadius: 4,
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const LabelBold = styled('span')({
  fontWeight: 'bold',
});

const StyledAccordion = styled(Accordion)(({
  backgroundColor: "#fbfbfb",
  boxShadow: '2px 4px 2px rgba(0, 0, 0, 0.1)',
  '&:before': {
    display: 'none',
  },
}));

export default function CadastroQuestionarioScreen() {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [versao, setVersao] = useState("");
  const [fontesLiteratura, setFontesLiteratura] = useState<any[]>([]);
  const [isFontesModalOpen, setIsFontesModalOpen] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: "", type: "" });
  const [questionarioCriado, setQuestionarioCriado] = useState<any>(null);
  const [sessoes, setSessoes] = useState<Sessao[]>([]);
  const [isSessaoModalOpen, setIsSessaoModalOpen] = useState(false);
  const [isPerguntaModalOpen, setIsPerguntaModalOpen] = useState(false);
  const [selectedSessaoId, setSelectedSessaoId] = useState<string | null>(null);
  const [perguntas, setPerguntas] = useState<Pergunta[]>([]);
  const [alternativas, setAlternativas] = useState<Alternativa[]>([]);

  // Estados para alternativas normais
  const [isAlternativaModalOpen, setIsAlternativaModalOpen] = useState(false);
  const [selectedPerguntaIdForAlternativa, setSelectedPerguntaIdForAlternativa] = useState<string | null>(null);

  // Estados para alternativas de escolha única
  const [isEscolhaUnicaModalOpen, setIsEscolhaUnicaModalOpen] = useState(false);
  const [escolhaUnicaData, setEscolhaUnicaData] = useState<{
    opcaoPositiva: string;
    valorPositivo: number;
    opcaoNegativa: string;
    valorNegativo: number;
  } | null>(null);

  // Armazenar a última configuração de escolha única usada
  const [ultimaEscolhaUnicaData, setUltimaEscolhaUnicaData] = useState<{
    opcaoPositiva: string;
    valorPositivo: number;
    opcaoNegativa: string;
    valorNegativo: number;
  } | null>(null);
  const [isReutilizarAlternativasDialogOpen, setIsReutilizarAlternativasDialogOpen] = useState(false);

  // Estados para o auto-preenchimento de alternativas
  const [isAutoPreencherOpen, setIsAutoPreencherOpen] = useState(false);
  const [selectedPerguntaId, setSelectedPerguntaId] = useState<string | null>(null);
  const [alternativasDisponiveis, setAlternativasDisponiveis] = useState<Alternativa[]>([]);
  const [alternativasSelecionadas, setAlternativasSelecionadas] = useState<string[]>([]);
  const [isLoadingAlternativas, setIsLoadingAlternativas] = useState(false);



  useEffect(() => {
    if (alternativasDisponiveis.length > 0) {
      setAlternativasSelecionadas(alternativasDisponiveis.map(alt => alt.id));
    }
  }, [alternativasDisponiveis]);

  const fetchPerguntas = useCallback(async () => {
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/perguntas/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
      });

      const data = await response.json();

      if (response.ok) {
        setPerguntas(data);
      } else {
        setSnackbar({ open: true, type: "error", message: "Erro ao carregar perguntas" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, []);

  const fetchAlternativas = useCallback(async () => {
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/alternativas/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
      });

      const data = await response.json();

      if (response.ok) {
        setAlternativas(data);
      } else {
        setSnackbar({ open: true, type: "error", message: "Erro ao carregar alternativas" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, []);
  useEffect(() => {
    // Carregar as perguntas existentes ao montar o componente
    if (sessoes.length > 0) {
      fetchPerguntas();
      fetchAlternativas();
    }
  }, [sessoes, fetchPerguntas, fetchAlternativas]);
  const handleSave = useCallback(async () => {
    const payload = {
      titulo,
      descricao,
      versao,
      fontes_literatura: fontesLiteratura
    };

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/questionario/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      const data = await response.json();

      if (response.ok) {
        setSnackbar({
          open: true,
          type: "success",
          message: "Questionário cadastrado com sucesso!"
        });
        setQuestionarioCriado(data);
      } else {
        setSnackbar({
          open: true,
          type: "error",
          message: data.message || "Erro ao cadastrar questionário"
        });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, [titulo, descricao, versao, fontesLiteratura]);

  const handleAddSessao = useCallback(async (sessaoData: { titulo: string; descricao?: string }) => {
    if (!questionarioCriado?.id) {
      setSnackbar({ open: true, type: "warning", message: "Crie o questionário primeiro!" });
      return;
    }

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/sessoes/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          questionario_id: questionarioCriado.id,
          titulo: sessaoData.titulo,
          descricao: sessaoData.descricao,
          ordem: sessoes.length + 1
        })
      });

      const data = await response.json();

      if (response.ok) {
        setSessoes([...sessoes, data]);
        setSnackbar({ open: true, type: "success", message: "Sessão adicionada com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: data.message || "Erro ao adicionar sessão" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
    setIsSessaoModalOpen(false);
  }, [questionarioCriado, sessoes]);

  // Função para adicionar alternativa - verifica o tipo de pergunta
  const handleAddAlternativa = useCallback((perguntaId: string) => {
    const pergunta = perguntas.find(p => p.id === perguntaId);
    if (!pergunta) return;

    setSelectedPerguntaIdForAlternativa(perguntaId);

    if (pergunta.tipo_resposta === "escolha_unica") {
      // Para escolha única, verificamos se já existem alternativas
      const perguntaAlternativas = alternativas.filter(alt => alt.pergunta_id === perguntaId);

      if (perguntaAlternativas.length === 0) {
        // Se não houver alternativas, abre o modal de escolha única
        setIsEscolhaUnicaModalOpen(true);
      } else {
        // Se já houver alternativas, carregamos os dados para o modal
        const positiva = perguntaAlternativas.find(alt => Number(alt.valor) === 1);
        const negativa = perguntaAlternativas.find(alt => Number(alt.valor) === 0);

        if (positiva && negativa) {
          setEscolhaUnicaData({
            opcaoPositiva: positiva.texto,
            valorPositivo: Number(positiva.valor),
            opcaoNegativa: negativa.texto,
            valorNegativo: Number(negativa.valor)
          });
          setIsEscolhaUnicaModalOpen(true);
        } else {
          // Se por algum motivo as alternativas estiverem inconsistentes
          setIsEscolhaUnicaModalOpen(true);
        }
      }
    } else if (pergunta.tipo_resposta === "multipla_escolha") {
      // Para múltipla escolha, abre o modal normal de alternativa
      setIsAlternativaModalOpen(true);
    }
  }, [perguntas, alternativas]);

  // Função para salvar alternativas de escolha única
  const handleSaveEscolhaUnica = useCallback(async (data: {
    opcaoPositiva: string;
    valorPositivo: number;
    opcaoNegativa: string;
    valorNegativo: number;
  }) => {
    if (!selectedPerguntaIdForAlternativa) {
      setSnackbar({ open: true, type: "warning", message: "Selecione uma pergunta primeiro!" });
      return;
    }

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Verificar se já existem alternativas para esta pergunta
      const perguntaAlternativas = alternativas.filter(alt =>
        alt.pergunta_id === selectedPerguntaIdForAlternativa
      );

      if (perguntaAlternativas.length === 0) {
        // Se não existirem, criamos duas novas alternativas
        await Promise.all([
          fetch(`${baseUrl}/alternativas/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              pergunta_id: selectedPerguntaIdForAlternativa,
              texto: data.opcaoPositiva,
              valor: data.valorPositivo,
              ordem: 1
            })
          }),
          fetch(`${baseUrl}/alternativas/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              pergunta_id: selectedPerguntaIdForAlternativa,
              texto: data.opcaoNegativa,
              valor: data.valorNegativo,
              ordem: 2
            })
          })
        ]);
      } else {
        // Se existirem, atualizamos as alternativas existentes
        const positiva = perguntaAlternativas.find(alt => Number(alt.valor) === 1) || perguntaAlternativas[0];
        const negativa = perguntaAlternativas.find(alt => Number(alt.valor) === 0) || perguntaAlternativas[1];

        await Promise.all([
          fetch(`${baseUrl}/alternativas/${positiva.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              ...positiva,
              texto: data.opcaoPositiva,
              valor: data.valorPositivo
            })
          }),
          fetch(`${baseUrl}/alternativas/${negativa.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              ...negativa,
              texto: data.opcaoNegativa,
              valor: data.valorNegativo
            })
          })
        ]);
      }

      // Recarregar alternativas
      await fetchAlternativas();
      // Salvar os valores para uso futuro
      setUltimaEscolhaUnicaData(data);
      setSnackbar({ open: true, type: "success", message: "Alternativas de escolha única salvas com sucesso!" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao salvar alternativas" });
    }
    setIsEscolhaUnicaModalOpen(false);
    setEscolhaUnicaData(null);
  }, [selectedPerguntaIdForAlternativa, alternativas, fetchAlternativas]);

  // Função para salvar a alternativa (para múltipla escolha)
  const handleSaveAlternativa = useCallback(async (alternativaData: { texto: string; valor: number }) => {
    if (!selectedPerguntaIdForAlternativa) {
      setSnackbar({ open: true, type: "warning", message: "Selecione uma pergunta primeiro!" });
      return;
    }

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Calcular a ordem da alternativa como a próxima disponível para esta pergunta
      const perguntaAlternativas = alternativas.filter(alt =>
        alt.pergunta_id === selectedPerguntaIdForAlternativa
      );
      const ordem = perguntaAlternativas.length + 1;

      const response = await fetch(`${baseUrl}/alternativas/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          pergunta_id: selectedPerguntaIdForAlternativa,
          texto: alternativaData.texto,
          valor: alternativaData.valor,
          ordem
        })
      });

      const data = await response.json();

      if (response.ok) {
        setAlternativas([...alternativas, data]);
        setSnackbar({ open: true, type: "success", message: "Alternativa adicionada com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: data.message || "Erro ao adicionar alternativa" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
    setIsAlternativaModalOpen(false);
  }, [selectedPerguntaIdForAlternativa, alternativas]);

  const handleSavePergunta = useCallback(async (perguntaData: { texto: string; tipo_resposta: string; is_obrigatoria: boolean }) => {
    if (!selectedSessaoId) {
      setSnackbar({ open: true, type: "warning", message: "Selecione uma sessão primeiro!" });
      return;
    }

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/perguntas/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          sessao_id: selectedSessaoId,
          texto: perguntaData.texto,
          tipo_resposta: perguntaData.tipo_resposta,
          is_obrigatoria: perguntaData.is_obrigatoria,
          ordem: perguntas.filter(p => p.sessao_id === selectedSessaoId).length + 1
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Atualizar o estado local das perguntas
        setPerguntas([...perguntas, data]);

        // Se for pergunta de escolha_unica, verificar se temos valores anteriores
        if (perguntaData.tipo_resposta === "escolha_unica") {
          setSelectedPerguntaIdForAlternativa(data.id);

          if (ultimaEscolhaUnicaData) {
            // Se já existem valores usados anteriormente, perguntar se quer reutilizá-los
            setIsReutilizarAlternativasDialogOpen(true);
          } else {
            // Caso contrário, usar os valores padrão
            handleSaveEscolhaUnica({
              opcaoPositiva: "Sim",
              valorPositivo: 1,
              opcaoNegativa: "Não",
              valorNegativo: 0
            });
          }
        }

        setSnackbar({ open: true, type: "success", message: "Pergunta adicionada com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: data.message || "Erro ao adicionar pergunta" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
    setIsPerguntaModalOpen(false);
  }, [selectedSessaoId, perguntas, ultimaEscolhaUnicaData, handleSaveEscolhaUnica]);

  // Versão melhorada da função handleMoveUp para Sessões
  const handleMoveUp = useCallback(async (id: string) => {
    // Encontre a posição atual e verifique se não é a primeira sessão
    const index = sessoes.findIndex(sessao => sessao.id === id);
    if (index <= 0) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a primeira sessão" });
      return;
    }

    // Clone o array para manipulação
    const newSessoes = [...sessoes];

    // Obtenha as duas sessões que vão trocar de lugar
    const sessaoAtual = { ...newSessoes[index] };
    const sessaoAnterior = { ...newSessoes[index - 1] };

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(sessaoAtual.ordem);
    const ordemAnterior = Number(sessaoAnterior.ordem);

    sessaoAtual.ordem = ordemAnterior;
    sessaoAnterior.ordem = ordemAtual;

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/sessoes/${sessaoAtual.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(sessaoAtual)
        }),
        fetch(`${baseUrl}/sessoes/${sessaoAnterior.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(sessaoAnterior)
        })
      ]);

      // Atualize no estado local (troque as posições)
      newSessoes[index] = sessaoAnterior;
      newSessoes[index - 1] = sessaoAtual;

      // Atualiza o estado ordenando pelo campo ordem numérico
      setSessoes([...newSessoes].sort((a, b) => Number(a.ordem) - Number(b.ordem)));
      setSnackbar({ open: true, type: "success", message: "Sessão movida para cima com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover sessão para cima" });
    }
  }, [sessoes]);

  // Versão melhorada da função handleMoveDown para Sessões
  const handleMoveDown = useCallback(async (id: string) => {
    // Encontre a posição atual e verifique se não é a última sessão
    const index = sessoes.findIndex(sessao => sessao.id === id);
    if (index >= sessoes.length - 1) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a última sessão" });
      return;
    }

    // Clone o array para manipulação
    const newSessoes = [...sessoes];

    // Obtenha as duas sessões que vão trocar de lugar
    const sessaoAtual = { ...newSessoes[index] };
    const sessaoSeguinte = { ...newSessoes[index + 1] };

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(sessaoAtual.ordem);
    const ordemSeguinte = Number(sessaoSeguinte.ordem);

    sessaoAtual.ordem = ordemSeguinte;
    sessaoSeguinte.ordem = ordemAtual;

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/sessoes/${sessaoAtual.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(sessaoAtual)
        }),
        fetch(`${baseUrl}/sessoes/${sessaoSeguinte.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(sessaoSeguinte)
        })
      ]);

      // Atualize no estado local (troque as posições)
      newSessoes[index] = sessaoSeguinte;
      newSessoes[index + 1] = sessaoAtual;

      // Atualiza o estado ordenando pelo campo ordem numérico
      setSessoes([...newSessoes].sort((a, b) => Number(a.ordem) - Number(b.ordem)));
      setSnackbar({ open: true, type: "success", message: "Sessão movida para baixo com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover sessão para baixo" });
    }
  }, [sessoes]);

  const handleDeleteSessao = useCallback(async (id: string) => {
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/sessoes/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        setSessoes(sessoes.filter(sessao => sessao.id !== id));
        setSnackbar({ open: true, type: "success", message: "Sessão excluída com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: "Erro ao excluir sessão" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, [sessoes]);

  const handleDeleteFonte = useCallback((index: number) => {
    const newFontes = [...fontesLiteratura];
    newFontes.splice(index, 1);
    setFontesLiteratura(newFontes);
  }, [fontesLiteratura]);

  const handleAddPergunta = useCallback((sessaoId: string) => {
    setSelectedSessaoId(sessaoId);
    setIsPerguntaModalOpen(true);
  }, []);

  // Versão melhorada da função handleMoveUpPergunta
  const handleMoveUpPergunta = useCallback(async (id: string) => {
    // Encontre a posição atual e a sessão desta pergunta
    const perguntaAtual = perguntas.find(p => p.id === id);
    if (!perguntaAtual) return;

    // Filtre perguntas da mesma sessão e ordene numericamente
    const perguntasDaSessao = perguntas
      .filter(p => p.sessao_id === perguntaAtual.sessao_id)
      .sort((a, b) => Number(a.ordem) - Number(b.ordem));

    // Encontre o índice dentro das perguntas da sessão
    const indexNaSessao = perguntasDaSessao.findIndex(p => p.id === id);

    // Verifica se já é a primeira pergunta da sessão
    if (indexNaSessao <= 0) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a primeira pergunta da sessão" });
      return;
    }

    // Obtenha a pergunta anterior na mesma sessão
    const perguntaAnterior = perguntasDaSessao[indexNaSessao - 1];

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(perguntaAtual.ordem);
    const ordemAnterior = Number(perguntaAnterior.ordem);

    const perguntaAtualAtualizada = { ...perguntaAtual, ordem: ordemAnterior };
    const perguntaAnteriorAtualizada = { ...perguntaAnterior, ordem: ordemAtual };

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/perguntas/${perguntaAtualAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(perguntaAtualAtualizada)
        }),
        fetch(`${baseUrl}/perguntas/${perguntaAnteriorAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(perguntaAnteriorAtualizada)
        })
      ]);

      // Atualize no estado local
      const newPerguntas = perguntas.map(p => {
        if (p.id === perguntaAtual.id) return perguntaAtualAtualizada;
        if (p.id === perguntaAnterior.id) return perguntaAnteriorAtualizada;
        return p;
      });

      setPerguntas(newPerguntas);
      setSnackbar({ open: true, type: "success", message: "Pergunta movida para cima com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover pergunta para cima" });
    }
  }, [perguntas]);

  // Versão melhorada da função handleMoveDownPergunta
  const handleMoveDownPergunta = useCallback(async (id: string) => {
    // Encontre a posição atual e a sessão desta pergunta
    const perguntaAtual = perguntas.find(p => p.id === id);
    if (!perguntaAtual) return;

    // Filtre perguntas da mesma sessão e ordene numericamente
    const perguntasDaSessao = perguntas
      .filter(p => p.sessao_id === perguntaAtual.sessao_id)
      .sort((a, b) => Number(a.ordem) - Number(b.ordem));

    // Encontre o índice dentro das perguntas da sessão
    const indexNaSessao = perguntasDaSessao.findIndex(p => p.id === id);

    // Verifica se já é a última pergunta da sessão
    if (indexNaSessao >= perguntasDaSessao.length - 1) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a última pergunta da sessão" });
      return;
    }

    // Obtenha a próxima pergunta na mesma sessão
    const perguntaSeguinte = perguntasDaSessao[indexNaSessao + 1];

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(perguntaAtual.ordem);
    const ordemSeguinte = Number(perguntaSeguinte.ordem);

    const perguntaAtualAtualizada = { ...perguntaAtual, ordem: ordemSeguinte };
    const perguntaSeguinteAtualizada = { ...perguntaSeguinte, ordem: ordemAtual };

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/perguntas/${perguntaAtualAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(perguntaAtualAtualizada)
        }),
        fetch(`${baseUrl}/perguntas/${perguntaSeguinteAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(perguntaSeguinteAtualizada)
        })
      ]);

      // Atualize no estado local
      const newPerguntas = perguntas.map(p => {
        if (p.id === perguntaAtual.id) return perguntaAtualAtualizada;
        if (p.id === perguntaSeguinte.id) return perguntaSeguinteAtualizada;
        return p;
      });

      setPerguntas(newPerguntas);
      setSnackbar({ open: true, type: "success", message: "Pergunta movida para baixo com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover pergunta para baixo" });
    }
  }, [perguntas]);

  const handleDeletePergunta = useCallback(async (id: string) => {
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/perguntas/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        setPerguntas(perguntas.filter(pergunta => pergunta.id !== id));
        setSnackbar({ open: true, type: "success", message: "Pergunta excluída com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: "Erro ao excluir pergunta" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, [perguntas]);

  // Versão melhorada da função handleMoveUpAlternativa
  const handleMoveUpAlternativa = useCallback(async (id: string) => {
    // Encontre a alternativa atual
    const alternativaAtual = alternativas.find(alt => alt.id === id);
    if (!alternativaAtual) return;

    // Filtre alternativas da mesma pergunta e ordene numericamente
    const alternativasDaPergunta = alternativas
      .filter(alt => alt.pergunta_id === alternativaAtual.pergunta_id)
      .sort((a, b) => Number(a.ordem) - Number(b.ordem));

    // Encontre o índice dentro das alternativas da pergunta
    const indexNaPergunta = alternativasDaPergunta.findIndex(alt => alt.id === id);

    // Verifica se já é a primeira alternativa
    if (indexNaPergunta <= 0) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a primeira alternativa" });
      return;
    }

    // Obtenha a alternativa anterior na mesma pergunta
    const alternativaAnterior = alternativasDaPergunta[indexNaPergunta - 1];

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(alternativaAtual.ordem);
    const ordemAnterior = Number(alternativaAnterior.ordem);

    const alternativaAtualAtualizada = { ...alternativaAtual, ordem: ordemAnterior };
    const alternativaAnteriorAtualizada = { ...alternativaAnterior, ordem: ordemAtual };

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/alternativas/${alternativaAtualAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(alternativaAtualAtualizada)
        }),
        fetch(`${baseUrl}/alternativas/${alternativaAnteriorAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(alternativaAnteriorAtualizada)
        })
      ]);

      // Atualize no estado local
      const newAlternativas = alternativas.map(alt => {
        if (alt.id === alternativaAtual.id) return alternativaAtualAtualizada;
        if (alt.id === alternativaAnterior.id) return alternativaAnteriorAtualizada;
        return alt;
      });

      setAlternativas(newAlternativas);
      setSnackbar({ open: true, type: "success", message: "Alternativa movida para cima com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover alternativa para cima" });
    }
  }, [alternativas]);

  // Versão melhorada da função handleMoveDownAlternativa
  const handleMoveDownAlternativa = useCallback(async (id: string) => {
    // Encontre a alternativa atual
    const alternativaAtual = alternativas.find(alt => alt.id === id);
    if (!alternativaAtual) return;

    // Filtre alternativas da mesma pergunta e ordene numericamente
    const alternativasDaPergunta = alternativas
      .filter(alt => alt.pergunta_id === alternativaAtual.pergunta_id)
      .sort((a, b) => Number(a.ordem) - Number(b.ordem));

    // Encontre o índice dentro das alternativas da pergunta
    const indexNaPergunta = alternativasDaPergunta.findIndex(alt => alt.id === id);

    // Verifica se já é a última alternativa
    if (indexNaPergunta >= alternativasDaPergunta.length - 1) {
      setSnackbar({ open: true, type: "info", message: "Esta já é a última alternativa" });
      return;
    }

    // Obtenha a próxima alternativa na mesma pergunta
    const alternativaSeguinte = alternativasDaPergunta[indexNaPergunta + 1];

    // Troque as ordens - garantindo que sejam números
    const ordemAtual = Number(alternativaAtual.ordem);
    const ordemSeguinte = Number(alternativaSeguinte.ordem);

    const alternativaAtualAtualizada = { ...alternativaAtual, ordem: ordemSeguinte };
    const alternativaSeguinteAtualizada = { ...alternativaSeguinte, ordem: ordemAtual };

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      // Atualize no backend
      await Promise.all([
        fetch(`${baseUrl}/alternativas/${alternativaAtualAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(alternativaAtualAtualizada)
        }),
        fetch(`${baseUrl}/alternativas/${alternativaSeguinteAtualizada.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(alternativaSeguinteAtualizada)
        })
      ]);

      // Atualize no estado local
      const newAlternativas = alternativas.map(alt => {
        if (alt.id === alternativaAtual.id) return alternativaAtualAtualizada;
        if (alt.id === alternativaSeguinte.id) return alternativaSeguinteAtualizada;
        return alt;
      });

      setAlternativas(newAlternativas);
      setSnackbar({ open: true, type: "success", message: "Alternativa movida para baixo com sucesso" });
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro ao mover alternativa para baixo" });
    }
  }, [alternativas]);

  const handleDeleteAlternativa = useCallback(async (id: string) => {
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/alternativas/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        setAlternativas(alternativas.filter(alt => alt.id !== id));
        setSnackbar({ open: true, type: "success", message: "Alternativa excluída com sucesso!" });
      } else {
        setSnackbar({ open: true, type: "error", message: "Erro ao excluir alternativa" });
      }
    } catch (error) {
      setSnackbar({ open: true, type: "error", message: "Erro de conexão" });
    }
  }, [alternativas]);

  // Funções para o auto-preenchimento de alternativas
  const handleOpenAutoPreenchimento = useCallback((perguntaId: string, sessaoId: string) => {
    const pergunta = perguntas.find(p => p.id === perguntaId);
    if (!pergunta || pergunta.tipo_resposta === "texto" || pergunta.tipo_resposta === "numero") {
      setSnackbar({ open: true, type: "info", message: "Este tipo de pergunta não aceita alternativas" });
      return;
    }

    setSelectedPerguntaId(perguntaId);
    setSelectedSessaoId(sessaoId);
    setAlternativasDisponiveis([]);
    setAlternativasSelecionadas([]);
    setIsAutoPreencherOpen(true);
    buscarAlternativasDaSessao(sessaoId, perguntaId);
  }, [perguntas]);

  const buscarAlternativasDaSessao = useCallback(async (sessaoId: string, perguntaId: string) => {
    setIsLoadingAlternativas(true);
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/sessoes/detailed/${sessaoId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        const sessao = await response.json();
        // Filtrar alternativas de outras perguntas na mesma sessão
        const alternativas: Alternativa[] = [];

        if (sessao.perguntas) {
          sessao.perguntas.forEach((p: any) => {
            if (p.id !== perguntaId && p.alternativas) {
              p.alternativas.forEach((alt: any) => {
                alternativas.push({
                  id: alt.id,
                  pergunta_id: alt.pergunta_id,
                  texto: alt.texto,
                  valor: alt.valor,
                  ordem: alt.ordem,
                  created_at: alt.created_at,
                  updated_at: alt.updated_at
                });
              });
            }
          });
        }

        if (alternativas.length > 0) {
          setAlternativasDisponiveis(alternativas);
        } else {
          // Se não encontrar na sessão, buscar no questionário
          buscarAlternativasDoQuestionario(sessaoId, perguntaId);
        }
      } else {
        console.error("Erro ao buscar sessão:", await response.text());
        buscarAlternativasDoQuestionario(sessaoId, perguntaId);
      }
    } catch (error) {
      console.error("Erro ao buscar alternativas:", error);
      buscarAlternativasDoQuestionario(sessaoId, perguntaId);
    } finally {
      setIsLoadingAlternativas(false);
    }
  }, []);

  const buscarAlternativasDoQuestionario = useCallback(async (sessaoId: string, perguntaId: string) => {
    if (!questionarioCriado?.id) return;

    setIsLoadingAlternativas(true);
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");
      const response = await fetch(`${baseUrl}/questionario/detailed/${questionarioCriado.id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.ok) {
        const questionario = await response.json();
        // Filtrar alternativas de perguntas de outras sessões
        const alternativas: Alternativa[] = [];

        if (questionario.sessoes) {
          questionario.sessoes.forEach((s: any) => {
            if (s.perguntas) {
              s.perguntas.forEach((p: any) => {
                if (p.id !== perguntaId && p.alternativas) {
                  p.alternativas.forEach((alt: any) => {
                    alternativas.push({
                      id: alt.id,
                      pergunta_id: alt.pergunta_id,
                      texto: alt.texto,
                      valor: alt.valor,
                      ordem: alt.ordem,
                      created_at: alt.created_at,
                      updated_at: alt.updated_at
                    });
                  });
                }
              });
            }
          });
        }

        setAlternativasDisponiveis(alternativas);
      } else {
        console.error("Erro ao buscar questionário:", await response.text());
        setSnackbar({ open: true, type: "error", message: "Erro ao buscar alternativas no questionário" });
      }
    } catch (error) {
      console.error("Erro ao buscar alternativas do questionário:", error);
      setSnackbar({ open: true, type: "error", message: "Erro ao buscar alternativas no questionário" });
    } finally {
      setIsLoadingAlternativas(false);
    }
  }, [questionarioCriado]);

  const handleToggleAlternativa = useCallback((id: string) => {
    setAlternativasSelecionadas(prev => {
      if (prev.includes(id)) {
        return prev.filter(item => item !== id);
      } else {
        return [...prev, id];
      }
    });
  }, []);

  const handleAdicionarAlternativasSelecionadas = useCallback(async () => {
    if (!selectedPerguntaId) return;

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const token = localStorage.getItem("@App:token");

      let adicionadas = 0;

      for (const altId of alternativasSelecionadas) {
        const alternativa = alternativasDisponiveis.find(alt => alt.id === altId);
        if (alternativa) {
          const novaAlternativa = {
            pergunta_id: selectedPerguntaId,
            texto: alternativa.texto,
            valor: alternativa.valor,
            ordem: Math.floor(Math.random() * 1000) // Valor temporário para ordem
          };

          const response = await fetch(`${baseUrl}/alternativas/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(novaAlternativa)
          });

          if (response.ok) {
            adicionadas++;
          }
        }
      }

      setIsAutoPreencherOpen(false);
      setSnackbar({
        open: true,
        type: "success",
        message: `${adicionadas} alternativas adicionadas com sucesso!`
      });

      // Recarregar alternativas para refletir as novas
      fetchAlternativas();
    } catch (error) {
      console.error("Erro ao adicionar alternativas:", error);
      setSnackbar({ open: true, type: "error", message: "Erro ao adicionar alternativas" });
    }
  }, [selectedPerguntaId, alternativasDisponiveis, alternativasSelecionadas, fetchAlternativas]);

  // Função para evitar propagação do evento de clique nos botões dentro do AccordionSummary
  const handleButtonClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
  }, []);

  // Função para editar alternativas de escolha única
  const handleEditAlternativasEscolhaUnica = useCallback((perguntaId: string) => {
    const perguntaAlternativas = alternativas.filter(alt => alt.pergunta_id === perguntaId);
    if (perguntaAlternativas.length === 2) {
      const positiva = perguntaAlternativas.find(alt => Number(alt.valor) === 1) || perguntaAlternativas[0];
      const negativa = perguntaAlternativas.find(alt => Number(alt.valor) === 0) || perguntaAlternativas[1];

      setEscolhaUnicaData({
        opcaoPositiva: positiva.texto,
        valorPositivo: Number(positiva.valor),
        opcaoNegativa: negativa.texto,
        valorNegativo: Number(negativa.valor)
      });

      setSelectedPerguntaIdForAlternativa(perguntaId);
      setIsEscolhaUnicaModalOpen(true);
    } else {
      // Caso as alternativas estejam inconsistentes, cria novas
      setSelectedPerguntaIdForAlternativa(perguntaId);
      setIsEscolhaUnicaModalOpen(true);
    }
  }, [alternativas]);

  return (
    <AdminLayout>
      <Box sx={{ maxWidth: 600, margin: "auto", padding: 2 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Cadastro de Questionário
        </Typography>

        {questionarioCriado ? (
          <CompactReadOnlyBox>
            <Typography>
              <LabelBold>Título:</LabelBold> {titulo}
            </Typography>
            <Typography>
              <LabelBold>Descrição:</LabelBold> {descricao}
            </Typography>
            <Typography>
              <LabelBold>Versão:</LabelBold> {versao}
            </Typography>

            <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
              <LabelBold> Fontes de Literatura: </LabelBold>
            </Typography>
            {fontesLiteratura.length > 0 ? (
              fontesLiteratura.map((fonte, index) => (
                <Typography key={index}>
                  {`${fonte.autores} . ${fonte.titulo} (${fonte.ano}), ${fonte.editora}`}
                </Typography>
              ))
            ) : (
              <Typography variant="body2" color="textSecondary">
                Nenhuma fonte adicionada
              </Typography>
            )}
          </CompactReadOnlyBox>
        ) : (
          <>
            <TextField
              label="Título"
              fullWidth
              value={titulo}
              onChange={(e) => setTitulo(e.target.value)}
              margin="normal"
            />
            <TextField
              label="Descrição"
              fullWidth
              multiline
              rows={4}
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              margin="normal"
            />
            <TextField
              label="Versão"
              fullWidth
              value={versao}
              onChange={(e) => setVersao(e.target.value)}
              margin="normal"
            />

            <Box sx={{ my: 2, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <Typography variant="subtitle1" sx={{ mr: 1 }}>
                Fontes de Literatura
              </Typography>
              <Divider sx={{ flexGrow: 1, mr: 1 }} />
              <Tooltip title="Inserir Fonte de Literatura">
                <IconButton
                  onClick={() => setIsFontesModalOpen(true)}
                >
                  <AddIcon color="info" />
                </IconButton>
              </Tooltip>
            </Box>

            {fontesLiteratura.length > 0 ? (
              fontesLiteratura.map((fonte, index) => (
                <Box
                  key={index}
                  sx={{
                    p: 1,
                    border: "1px solid #ccc",
                    borderRadius: 1,
                    mb: 1,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <Typography variant="body2">
                    {fonte.autores} . {fonte.titulo} ({fonte.ano}), {fonte.editora}
                  </Typography>
                  <Tooltip title="Excluir Fonte">
                    <IconButton onClick={() => handleDeleteFonte(index)}>
                      <DeleteIcon color="error" />
                    </IconButton>
                  </Tooltip>
                </Box>
              ))
            ) : (
              <Typography variant="body2" color="textSecondary">
                Nenhuma fonte adicionada
              </Typography>
            )}

            {!questionarioCriado && (
              <Button variant="contained" color="primary" fullWidth onClick={handleSave}>
                Salvar Questionário
              </Button>
            )}
          </>
        )}

        <Divider sx={{ my: 2 }} />

        {questionarioCriado && (
          <Box sx={{ my: 2 }}>
            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <Typography variant="subtitle1" sx={{ mr: 1 }}>
                Sessões
              </Typography>
              <Divider sx={{ flexGrow: 1, mr: 1 }} />
              <Tooltip title="Adicionar Sessão">
                <IconButton
                  onClick={() => setIsSessaoModalOpen(true)}
                >
                  <AddIcon color="info" />
                </IconButton>
              </Tooltip>
            </Box>

            {sessoes.map((sessao) => (
              <StyledAccordion key={sessao.id}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-around' }}>
                  <Box sx={{ backgroundColor: 'white', display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                    <Typography variant="subtitle1">{sessao.titulo}</Typography>

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Tooltip title="Mover para cima">
                        <IconButton onClick={(e) => { handleButtonClick(e); handleMoveUp(sessao.id); }}>
                          <ArrowUpwardIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Mover para baixo">
                        <IconButton onClick={(e) => { handleButtonClick(e); handleMoveDown(sessao.id); }}>
                          <ArrowDownwardIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton onClick={(e) => { handleButtonClick(e); handleDeleteSessao(sessao.id); }}>
                          <DeleteIcon color="error" />
                        </IconButton>
                      </Tooltip>

                    </Box>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2" sx={{ mb: 1, fontWeight: "bold" }}>Descricão: </Typography>

                  <Typography style={{ whiteSpace: 'pre-line' }} variant="body2">
                    {sessao.descricao || "Sem descrição"}
                  </Typography>

                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%", mt: 2 }}>
                    <Typography variant="body2">Perguntas</Typography>
                    <Divider sx={{ flexGrow: 1, mx: 2, borderBottomWidth: 2 }} />
                    <Tooltip title="Adicionar Pergunta">
                      <IconButton onClick={() => handleAddPergunta(sessao.id)}>
                        <AddIcon color="info" />
                      </IconButton>
                    </Tooltip>
                  </Box>

                  {/* Renderizar as perguntas aqui */}
                  {perguntas
                    .filter((pergunta) => pergunta.sessao_id === sessao.id)
                    .map((pergunta) => (
                      <StyledAccordion key={pergunta.id}>
                        <AccordionSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls={`panel-${pergunta.id}-content`}
                          id={`panel-${pergunta.id}-header`}
                          sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            alignItems: 'center',
                            justifyContent: 'space-between'
                          }}
                        >
                          <Typography variant="body1" sx={{ flex: 1 }}>{pergunta.texto}</Typography>
                          <Box sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1,
                            marginLeft: 'auto',
                            marginRight: 2
                          }}>
                            <Tooltip title="Mover para cima">
                              <IconButton
                                size="small"
                                onClick={(e) => { handleButtonClick(e); handleMoveUpPergunta(pergunta.id); }}
                              >
                                <ArrowUpwardIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Mover para baixo">
                              <IconButton
                                size="small"
                                onClick={(e) => { handleButtonClick(e); handleMoveDownPergunta(pergunta.id); }}
                              >
                                <ArrowDownwardIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Excluir">
                              <IconButton
                                size="small"
                                onClick={(e) => { handleButtonClick(e); handleDeletePergunta(pergunta.id); }}
                              >
                                <DeleteIcon fontSize="small" color="error" />
                              </IconButton>
                            </Tooltip>

                            {/* Auto-preenchimento apenas para múltipla escolha */}
                            {pergunta.tipo_resposta === "multipla_escolha" && (
                              <Tooltip title="Auto-preencher alternativas">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={(e) => {
                                    handleButtonClick(e);
                                    handleOpenAutoPreenchimento(pergunta.id, sessao.id);
                                  }}
                                >
                                  <AutoAwesomeIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            )}

                            {/* Botão de adicionar/editar alternativas - comportamento dinâmico */}
                            {pergunta.tipo_resposta === "texto" || pergunta.tipo_resposta === "numero" ? (
                              <Tooltip title="Este tipo de pergunta não permite alternativas">
                                <span>
                                  <IconButton
                                    size="small"
                                    disabled
                                  >
                                    <AddIcon fontSize="small" />
                                  </IconButton>
                                </span>
                              </Tooltip>
                            ) : pergunta.tipo_resposta === "escolha_unica" ? (
                              <Tooltip title="Editar opções de escolha única">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={(e) => {
                                    handleButtonClick(e);
                                    handleEditAlternativasEscolhaUnica(pergunta.id);
                                  }}
                                >
                                  <EditIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            ) : (
                              <Tooltip title="Adicionar alternativa">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={(e) => {
                                    handleButtonClick(e);
                                    handleAddAlternativa(pergunta.id);
                                  }}
                                >
                                  <AddIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            )}
                          </Box>
                        </AccordionSummary>
                        <AccordionDetails>
                          <Typography variant="body2">
                            Tipo de Resposta: {
                              pergunta.tipo_resposta === "texto" ? "Texto" :
                                pergunta.tipo_resposta === "numero" ? "Número" :
                                  pergunta.tipo_resposta === "escolha_unica" ? "Escolha Única (Sim/Não)" :
                                    "Múltipla Escolha"
                            }
                            <br />
                            Obrigatória: {pergunta.is_obrigatoria ? 'Sim' : 'Não'}
                          </Typography>

                          {/* Lista de alternativas - exibir apenas para tipos que usam alternativas */}
                          {pergunta.tipo_resposta !== "texto" && pergunta.tipo_resposta !== "numero" && (
                            <>
                              <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                                Alternativas:
                              </Typography>
                              {alternativas
                                .filter((alt) => alt.pergunta_id === pergunta.id)
                                .sort((a, b) => Number(a.ordem) - Number(b.ordem))
                                .map((alt) => (
                                  <Box
                                    key={alt.id}
                                    sx={{
                                      p: 1,
                                      border: "1px solid #eee",
                                      borderRadius: 1,
                                      mb: 1,
                                      display: "flex",
                                      alignItems: "center",
                                      justifyContent: "space-between",
                                      backgroundColor: "#f9f9f9"
                                    }}
                                  >
                                    <Typography variant="body2">
                                      {alt.texto} (Valor: {alt.valor})
                                    </Typography>
                                    <Box sx={{ display: 'flex', gap: 1 }}>
                                      <Tooltip title="Mover para cima">
                                        <IconButton
                                          size="small"
                                          onClick={() => handleMoveUpAlternativa(alt.id)}
                                        >
                                          <ArrowUpwardIcon fontSize="small" />
                                        </IconButton>
                                      </Tooltip>
                                      <Tooltip title="Mover para baixo">
                                        <IconButton
                                          size="small"
                                          onClick={() => handleMoveDownAlternativa(alt.id)}
                                        >
                                          <ArrowDownwardIcon fontSize="small" />
                                        </IconButton>
                                      </Tooltip>
                                      <Tooltip title="Excluir">
                                        <IconButton
                                          size="small"
                                          onClick={() => handleDeleteAlternativa(alt.id)}
                                        >
                                          <DeleteIcon fontSize="small" color="error" />
                                        </IconButton>
                                      </Tooltip>
                                    </Box>
                                  </Box>
                                ))}
                            </>
                          )}
                        </AccordionDetails>
                      </StyledAccordion>
                    ))}

                </AccordionDetails>
              </StyledAccordion>
            ))}

          </Box>
        )}
      </Box>

      <FontesLiteraturaModal
        open={isFontesModalOpen}
        onClose={() => setIsFontesModalOpen(false)}
        onSave={(fontes) => {
          setFontesLiteratura(fontes);
          setIsFontesModalOpen(false);
        }}
      />

      <SessaoModal
        open={isSessaoModalOpen}
        onClose={() => setIsSessaoModalOpen(false)}
        onSave={handleAddSessao}
      />

      <PerguntaModal
        open={isPerguntaModalOpen}
        onClose={() => setIsPerguntaModalOpen(false)}
        onSave={handleSavePergunta}
      />

      {/* Modal de alternativa */}
      <AlternativaModal
        open={isAlternativaModalOpen}
        onClose={() => setIsAlternativaModalOpen(false)}
        onSave={handleSaveAlternativa}
      />

      {/* Modal de Escolha Única */}
      <AlternativaEscolhaUnicaModal
        open={isEscolhaUnicaModalOpen}
        onClose={() => setIsEscolhaUnicaModalOpen(false)}
        onSave={handleSaveEscolhaUnica}
        initialData={escolhaUnicaData || undefined}
      />

      {/* Diálogo para auto-preenchimento de alternativas */}
      <Dialog
        open={isAutoPreencherOpen}
        onClose={() => setIsAutoPreencherOpen(false)}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>
          Auto-Preenchimento de Alternativas
        </DialogTitle>
        <DialogContent>
          {isLoadingAlternativas ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : alternativasDisponiveis.length > 0 ? (
            <>
              <Typography variant="body2" gutterBottom sx={{ mb: 2 }}>
                Selecione as alternativas que deseja adicionar à pergunta:
              </Typography>
              <List>
                {alternativasDisponiveis.map((alt) => (
                  <ListItem
                    key={alt.id}
                    component="div"
                    disablePadding
                    sx={{ borderBottom: '1px solid #f0f0f0' }}
                  >
                    <ListItemButton onClick={() => handleToggleAlternativa(alt.id)} dense>
                      <ListItemIcon>
                        <Checkbox
                          edge="start"
                          checked={alternativasSelecionadas.includes(alt.id)}
                          tabIndex={-1}
                          disableRipple
                        />
                      </ListItemIcon>
                      <ListItemText
                        primary={alt.texto}
                        secondary={`Valor: ${alt.valor}`}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </>
          ) : (
            <Typography>Nenhuma alternativa encontrada para reaproveitamento.</Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsAutoPreencherOpen(false)} color="inherit">
            Cancelar
          </Button>
          <Button
            onClick={handleAdicionarAlternativasSelecionadas}
            color="primary"
            variant="contained"
            disabled={alternativasSelecionadas.length === 0}
          >
            Adicionar Selecionadas ({alternativasSelecionadas.length})
          </Button>
        </DialogActions>
      </Dialog>

      {/* Diálogo para reutilizar alternativas */}
      <Dialog
        open={isReutilizarAlternativasDialogOpen}
        onClose={() => setIsReutilizarAlternativasDialogOpen(false)}
      >
        <DialogTitle>Reutilizar Alternativas</DialogTitle>
        <DialogContent>
          <Typography>
            Deseja utilizar as mesmas opções da última pergunta de escolha única?
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">
              <strong>Opção Positiva:</strong> {ultimaEscolhaUnicaData?.opcaoPositiva} (Valor: {ultimaEscolhaUnicaData?.valorPositivo})
            </Typography>
            <Typography variant="body2">
              <strong>Opção Negativa:</strong> {ultimaEscolhaUnicaData?.opcaoNegativa} (Valor: {ultimaEscolhaUnicaData?.valorNegativo})
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setIsReutilizarAlternativasDialogOpen(false);
            // Usa valores padrão
            handleSaveEscolhaUnica({
              opcaoPositiva: "Sim",
              valorPositivo: 1,
              opcaoNegativa: "Não",
              valorNegativo: 0
            });
          }}>
            Usar Padrão (Sim/Não)
          </Button>
          <Button onClick={() => {
            setIsReutilizarAlternativasDialogOpen(false);
            // Abre o modal para editar manualmente
            setIsEscolhaUnicaModalOpen(true);
          }}>
            Personalizar
          </Button>
          <Button
            variant="contained"
            onClick={() => {
              setIsReutilizarAlternativasDialogOpen(false);
              // Reutiliza as últimas alternativas
              if (ultimaEscolhaUnicaData) {
                handleSaveEscolhaUnica(ultimaEscolhaUnicaData);
              }
            }}
          >
            Reutilizar
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.type as "error" | "success" | "info" | "warning"}
          sx={{ width: "100%" }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </AdminLayout>
  );
}