import React, { useState, useEffect, useCallback } from "react";
import {
  Accordion,
  Box,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material";
import AdminLayout from "../layouts/AdminLayout";
import {
  Sessao,
  Pergunta,
  Alternativa,
  Questionario,
  FonteBibliografica,
} from "../types/questionario";
import { useParams } from "react-router-dom";
import QuestionarioInfoCard from "../components/QuestionarioInfoCard";
import QuestionarioForm from "../components/QuestionarioForm";
import {
  AddCircle,
  AddCircleSharp,
  AddRounded,
  PlusOneOutlined,
} from "@mui/icons-material";
import SessaoInfoCard from "../components/SessoesInfoCard";
import SessaoModal from "../modals/ModalsCadastroQuestionario/SessaoModal";

export default function CadastroQuestionarioScreen() {
  const { id } = useParams<{ id: string }>();
  const [questionario, setQuestionario] = useState<Questionario | null>(null);
  const [isViewMode, setIsViewMode] = useState<boolean>(false);

  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const token = localStorage.getItem("@App:token");

  // Estado para controlar o modal de edição de sessão
  const [isSessaoModalOpen, setIsSessaoModalOpen] = useState(false);
  const [selectedSessao, setSelectedSessao] = useState<Sessao | null>(null);

  const handleSave = async (data: Questionario) => {
    try {
      const url = id
        ? `${backendUrl}/questionario/${id}`
        : `${backendUrl}/questionario/`;
      const method = id ? "PUT" : "POST";

      const response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(
          `Erro ao ${id ? "atualizar" : "criar"} questionário: ${
            response.status
          }`
        );
      }

      const savedQuestionario = await response.json();
      // Aqui está a correção: mescla os dados retornados com o questionario existente
      setQuestionario({ ...questionario, ...savedQuestionario });
      setIsViewMode(true);
    } catch (error: any) {
      console.error("Erro ao salvar questionário:", error);
      // Aqui você pode adicionar uma lógica para exibir uma mensagem de erro ao usuário
    }
  };

  const handleEdit = (questionario: Questionario) => {
    setIsViewMode(false);
    console.log("Editando questionário:", questionario);
  };

  const prepareFormData = () => {
    if (!questionario) return undefined;

    return {
      titulo: questionario.titulo || "",
      descricao: questionario.descricao || "",
      versao: questionario.versao || "",
      fontes_literatura: Array.isArray(questionario.fontes_literatura)
        ? questionario.fontes_literatura.map((fonte) => {
            if (typeof fonte === "string") {
              return {
                titulo: fonte,
                autores: "",
                ano: "",
              };
            }
            return {
              titulo: fonte.titulo || "",
              autores: fonte.autores || "",
              ano: fonte.ano || "",
              editora: fonte.editora,
              local: fonte.local,
            };
          })
        : [],
    };
  };

  useEffect(() => {
    setIsViewMode(!!id);

    if (!id) return;

    const fetchQuestionario = async () => {
      try {
        const url = `${backendUrl}/questionario/detailed/${id}`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Erro ao buscar questionário");
        }

        const data = await response.json();
        setQuestionario(data);
      } catch (error) {
        console.error("Erro:", error);
        setIsViewMode(false);
      }
    };

    fetchQuestionario();
  }, [id, backendUrl, token]);

  // Funções para controlar o modal de edição de sessão
  const handleOpenSessaoModal = (sessao: Sessao) => {
    setSelectedSessao(sessao);
    setIsSessaoModalOpen(true);
  };

  const handleCloseSessaoModal = () => {
    setIsSessaoModalOpen(false);
    setSelectedSessao(null);
  };

  // Função para salvar as alterações na sessão
  const handleSaveSessao = (sessaoAtualizada: { titulo: string; descricao?: string | undefined; }) => {
    // Lógica para atualizar a sessão no estado do questionário
    const updatedSessoes = questionario?.sessoes?.map(sessao =>
      sessao.id === selectedSessao?.id
        ? { ...sessao, titulo: sessaoAtualizada.titulo, descricao: sessaoAtualizada.descricao }
        : sessao
    ) || [];

    setQuestionario(prevQuestionario => ({
      ...prevQuestionario,
      sessoes: updatedSessoes,
    } as Questionario));

    // Fechar o modal
    handleCloseSessaoModal();
  };

  return (
    <AdminLayout>
      
      <Box
        sx={{
          maxWidth: "100vh",
          margin: { xs: "0", md: "auto" },
          padding: { xs: "0", md: "auto" },
        }}
      >
      <Box sx={{ display: "flex", alignItems: "center" , marginBottom: 2 }}>
        <Typography variant="h5">Questionario</Typography>
        <Box sx={{ width: "100%" }}>
          <Divider sx={{marginLeft: 1}} />
        </Box>
      </Box>
        {isViewMode && questionario ? (
          <QuestionarioInfoCard
            questionario={questionario}
            onEdit={handleEdit}
          />
        ) : (
          <QuestionarioForm
            initialData={prepareFormData()}
            onSave={handleSave}
          />
        )}
        <Box sx={{display: 'flex', flexDirection: 'column', gap: 2, marginTop: 2}}>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Typography variant="h5">
              Sessões
            </Typography>
            <Box sx={{width: "100%", marginX: 2}}>
              <Divider/>
            </Box>
       
            <Tooltip title="Adicionar nova sessão">
              <IconButton onClick={() => console.log("Adicionar nova sessão")}>
                <AddCircleSharp color="info" />
              </IconButton>
            </Tooltip>
          </Box>
        {questionario &&
          questionario.sessoes &&
          questionario.sessoes.length > 0 &&
          questionario.sessoes.map((sessao: Sessao) => (
            <SessaoInfoCard
              key={sessao.id}
              sessao={sessao}
              onAdd={() => {
                console.log("Adicionar nova sessão");
              }}
              onDelete={() => {
                console.log("Deletar sessão");
              }}
              onEdit={(sessao: Sessao) => {
                handleOpenSessaoModal(sessao);
              }}
            />
          ))}
          </Box>
      </Box>

      {/* Modal de edição de sessão */}
      <SessaoModal
        open={isSessaoModalOpen}
        onClose={handleCloseSessaoModal}
        onSave={handleSaveSessao}
        initialData={selectedSessao || undefined}
      />
    </AdminLayout>
  );
}
