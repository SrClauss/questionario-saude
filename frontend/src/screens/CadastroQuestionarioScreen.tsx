import React, { useState, useEffect} from "react";
import {
  Box,
  Divider,
  IconButton,
  Tooltip,
  Typography,
  Snackbar,
  Alert,
} from "@mui/material";
import VariableLayout from "../layouts/VariableLayout";
import { Sessao, Questionario } from "../types/questionario";
import { useNavigate, useParams } from "react-router-dom";
import QuestionarioInfoCard from "../components/QuestionarioInfoCard";
import QuestionarioForm from "../components/QuestionarioForm";
import { AddCircleSharp } from "@mui/icons-material";
import SessaoInfoCard from "../components/SessoesInfoCard";
import SessaoModal from "../modals/ModalsCadastroQuestionario/SessaoModal";
import DeleteModal from "../modals/DeleteDialog";
import { QuestionarioProvider } from "../contexts/QuestionarioContext";
import { useQuestionarioContext } from "../contexts/QuestionarioContext";
import { SessaoData } from "../modals/ModalsCadastroQuestionario/SessaoModal";
export interface PerguntaCondicional {
  id: string;
  texto: string;
}


export default function CadastroQuestionarioScreen() {
  return (
    <QuestionarioProvider>
      <CadastroQuestionarioContent />
    </QuestionarioProvider>
  );
}

function CadastroQuestionarioContent() {
  const { id: urlId } = useParams<{ id: string }>();
  const [questionarioId, setQuestionarioId] = useState<string | undefined>(urlId);
  const [questionario, setQuestionario] = useState<Questionario | null>(null);
  const [isViewMode, setIsViewMode] = useState<boolean>(false);
  const navigate = useNavigate();

  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const token = localStorage.getItem("@App:token");

  const {  setHasBaterias } = useQuestionarioContext();

  
  const [isSessaoModalOpen, setIsSessaoModalOpen] = useState(false);
  const [selectedSessao, setSelectedSessao] = useState<Sessao | null>(null);

  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [sessaoToDelete, setSessaoToDelete] = useState<string | null>(null);

  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error" | "warning" | "info">("success");


  const handleSave = async (data: Questionario) => {
    try {
      const url = urlId
        ? `${backendUrl}/questionario/${urlId}`
        : `${backendUrl}/questionario`;
      const method = urlId ? "PUT" : "POST";

      const response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Erro ao ${urlId ? "atualizar" : "criar"} questionário: ${response.status}`);
      }

      const savedQuestionario = await response.json();
      savedQuestionario.sessoes = questionario?.sessoes || [];
      setQuestionario(savedQuestionario);
      setIsViewMode(true);

      if (!urlId) {
        setQuestionarioId(savedQuestionario.id);
        navigate(`/cadastro-questionario/${savedQuestionario.id}`, { replace: true });
      }

      setSnackbarMessage(`Questionário "${savedQuestionario.titulo}" ${urlId ? "atualizado" : "criado"} com sucesso!`);
      setSnackbarSeverity("success");
      setOpenSnackbar(true);
    } catch (error: any) {
      console.error("Erro ao salvar questionário:", error);
      setSnackbarMessage(`Erro ao salvar questionário: ${error.message}`);
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    }
  };

  const fetchHasBaterias = async () => {
    if (!questionarioId) return;
    try {
      const url = `${backendUrl}/questionario/has_baterias/${questionarioId}`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        console.error("Erro ao verificar baterias");
        return;
      }
      const data = await response.json();
      setHasBaterias(data.has_baterias);
    } catch (error) {
      console.error("Erro no fetch has_baterias:", error);
    }
  };
  const prepareFormData = () => {
    if (!questionario) return undefined;
    return {
      titulo: questionario.titulo || "",
      descricao: questionario.descricao || "",
      versao: questionario.versao || "",
      fontes_literatura: Array.isArray(questionario.fontes_literatura)
        ? questionario.fontes_literatura.map((fonte) =>
            typeof fonte === "string"
              ? { titulo: fonte, autores: "", ano: "" }
              : {
                  titulo: fonte.titulo || "",
                  autores: fonte.autores || "",
                  ano: fonte.ano || "",
                  editora: fonte.editora,
                  local: fonte.local,
                }
          )
        : [],
    };
  };

  const fetchQuestionarioDetalhado = async () => {
    if (!questionarioId) return;
    try {
      const url = `${backendUrl}/questionario/detailed/${questionarioId}`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Erro ao buscar questionário detalhado");
      }

      const data = await response.json();
      setQuestionario(data);
    } catch (error) {
      console.error("Erro:", error);
    }
  };

  useEffect(() => {
    setIsViewMode(!!urlId);
    setQuestionarioId(urlId);

    if (!urlId) return;

    fetchQuestionarioDetalhado();
  }, [urlId, backendUrl, token]);

  // Fetch hasBaterias when questionarioId changes
  useEffect(() => {
    if (!questionarioId) return;
    fetchHasBaterias();
  }, [questionarioId, backendUrl, token]);

  const handleOpenSessaoModal = (sessao: Sessao) => {
    setSelectedSessao(sessao);
    setIsSessaoModalOpen(true);
  };

  const handleOpenNewSessaoModal = () => {
    setSelectedSessao(null);
    setIsSessaoModalOpen(true);
  };

  const handleCloseSessaoModal = () => {
    setIsSessaoModalOpen(false);
    setSelectedSessao(null);
  };

  const handleSaveSessao = async (sessaoData: SessaoData) => {
    if (!questionarioId) {
      setSnackbarMessage("ID do Questionário não encontrado para salvar a sessão.");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
      return;
    }

    const url = sessaoData.id
      ? `${backendUrl}/sessoes/${sessaoData.id}`
      : `${backendUrl}/sessoes`;
    const method = sessaoData.id ? "PUT" : "POST";

    // Adiciona questionario_id ao payload
    const payload = {
      ...sessaoData,
      questionario_id: questionarioId,
    };

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `Erro ao salvar sessão: ${response.status}`);
      }

      const savedSessao = await response.json();

      // Atualiza o questionário detalhado para refletir a sessão salva/atualizada
      await fetchQuestionarioDetalhado();

      setSnackbarMessage(`Sessão "${savedSessao.titulo}" salva com sucesso!`);
      setSnackbarSeverity("success");
      setOpenSnackbar(true);
      handleCloseSessaoModal();

    } catch (error: any) {
      console.error("Erro ao salvar sessão:", error);
      setSnackbarMessage(error.message || "Erro desconhecido ao salvar sessão.");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    }
  };

  

  const handleConfirmDeleteSessao = (sessaoId: string) => {
    setSessaoToDelete(sessaoId);
    setIsDeleteDialogOpen(true);
  };

  const handleCancelDelete = () => {
    setSessaoToDelete(null);
    setIsDeleteDialogOpen(false);
  };

  const handleDeleteSessao = async () => {
    try {
      if (!sessaoToDelete) return;
      const sessaoTitle = questionario?.sessoes?.find((s) => s.id === sessaoToDelete)?.titulo || "Sessão";
      const response = await fetch(`${backendUrl}/sessoes/${sessaoToDelete}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Erro ao deletar sessão: ${response.status}`);
      }

      setQuestionario((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          sessoes: prev.sessoes.filter((sessao) => sessao.id !== sessaoToDelete),
        };
      });

      setSnackbarMessage(`A sessão "${sessaoTitle}" foi excluída com sucesso!`);
      setSnackbarSeverity("success");
      setOpenSnackbar(true);

      setIsDeleteDialogOpen(false);
      setSessaoToDelete(null);
    } catch (error: any) {
      console.error("Erro ao deletar sessão:", error);
      setSnackbarMessage(`Erro ao excluir sessão: ${error.message}`);
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
      setIsDeleteDialogOpen(false);
      setSessaoToDelete(null);
    }
  };

  const handleCloseSnackbar = (_event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === "clickaway") return;
    setOpenSnackbar(false);
  };

  return (
    <VariableLayout>
      <Box
        sx={{
          maxWidth: "100vh",
          margin: { xs: "0", md: "auto" },
          padding: { xs: "0", md: "auto" },
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", marginBottom: 2 }}>
          <Typography variant="h5">Questionario</Typography>
          <Box sx={{ width: "100%" }}>
            <Divider sx={{ marginLeft: 1 }} />
          </Box>
        </Box>
        {isViewMode && questionario ? (
          <QuestionarioInfoCard
            questionario={questionario}
            onEdit={() => setIsViewMode(false)}
            // Call both fetchQuestionarioDetalhado and fetchHasBaterias on refresh
            onRefresh={async () => { await fetchQuestionarioDetalhado(); await fetchHasBaterias(); }}
          />
        ) : (
          <QuestionarioForm initialData={prepareFormData()} onSave={handleSave} />
        )}
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2, marginTop: 2 }}>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Typography variant="h5">Sessões</Typography>
            <Box sx={{ width: "100%", marginX: 2 }}>
              <Divider />
            </Box>
            <Tooltip title="Adicionar nova sessão">
              <IconButton onClick={handleOpenNewSessaoModal}>
                <AddCircleSharp color="info" />
              </IconButton>
            </Tooltip>
          </Box>
          {questionario &&
            questionario.sessoes &&
            questionario.sessoes.map((sessao: Sessao) => (
              <SessaoInfoCard
                key={sessao.id}
                sessao={sessao}
                onDelete={() => handleConfirmDeleteSessao(sessao.id)}
                onEdit={(sessao: Sessao) => handleOpenSessaoModal(sessao)}
                onUpdate={fetchQuestionarioDetalhado}
              />
            ))}
        </Box>
      </Box>

      <SessaoModal
        open={isSessaoModalOpen}
        onClose={handleCloseSessaoModal}
        onSave={handleSaveSessao}
        initialData={selectedSessao || undefined}
        questionarioId={questionarioId || ""}
        ordem={questionario?.sessoes?.length  || 0}
      />

      <DeleteModal
        open={isDeleteDialogOpen}
        onClose={handleCancelDelete}
        onConfirm={handleDeleteSessao}
        itemName={
          questionario?.sessoes?.find((s) => s.id === sessaoToDelete)?.titulo || "esta sessão"
        }
      />

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: "100%" }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </VariableLayout>
  );
}