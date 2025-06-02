import { useEffect, useState } from "react";
import {
  Snackbar,
  Alert,
  Button,
  Box,
} from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import StylizedTitle from "../components/StylizedTitle";
import LabeledBox from "../components/LabeledBox";
import ResultQuestionario from "../components/ResultQuestionario";
import { Questionario } from "../types/questionario"; // defina esse tipo conforme necessário
import { auth } from "../utils/auth";
import { Paciente } from "../types/user";

export default function AplicacaoQuestionarioPacienteScreen() {
  const [snackBarProps, setSnackBarProps] = useState({
    open: false,
    type: "success",
    message: "",
  });
  const [resultadosQuestionarios, setResultadosQuestionarios] = useState<Questionario[]>([]);
  const [questionariosSelecionados, setQuestionariosSelecionados] = useState<Questionario[]>([]);
  // Aqui assumimos que o id passado na rota é o do paciente
  const { id: pacienteId } = useParams();
  const navigate = useNavigate();
  const [paciente, setPaciente] = useState<Paciente | null>(null);
useEffect(() => {

  const baseUrl = import.meta.env.VITE_BACKEND_URL;
  const token = localStorage.getItem("@App:token");
  const url = `${baseUrl}/pacientes/${pacienteId}`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      setPaciente(data);
    })
    .catch((error) => {
      console.error("Error fetching paciente:", error);
    });
}
, [pacienteId]);
  
  const handleSearch = (query: string) => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    if (query.length < 3) return;
   
    const url = `${baseUrl}/questionario/find_by_title_or_description/${query}/0/10`;
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setResultadosQuestionarios(data);
      })
      .catch((error) => {
        console.error("Error fetching questionários:", error);
      });
  };

  // Alterna questionário entre resultados e selecionados
  const handleSelect = (questionario: Questionario) => {
    const jaSelecionado = questionariosSelecionados.find(q => q.id === questionario.id);
    if (jaSelecionado) {
      setQuestionariosSelecionados(prev => prev.filter(q => q.id !== questionario.id));
      setResultadosQuestionarios(prev => [...prev, questionario]);
    } else {
      setQuestionariosSelecionados(prev => [...prev, questionario]);
      setResultadosQuestionarios(prev => prev.filter(q => q.id !== questionario.id));
    }
  };

  const handleSaveAplicacao = () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    const profissionalSaudeId = auth.getProfile()?.id
  
    const url = `${baseUrl}/baterias_testes/batch_save`;
    const payload = {
      profissional_saude_id: profissionalSaudeId,
      baterias: questionariosSelecionados.map((questionario) => ({
        paciente_id: pacienteId,
        questionario_id: questionario.id,
        data_aplicacao: new Date().toISOString().split("T")[0],
        respostas: {},
        observacoes: "",
        is_completo: false,
      })),
    };

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (response.ok) {
          setSnackBarProps({
            open: true,
            type: "success",
            message: "Questionários aplicados com sucesso!",
          });
          // Após breve delay, navega para a tela de questionários (ou outra tela de confirmação)
          setTimeout(() => {
            navigate("/questionario");
          }, 1500);
        } else {
          console.error("Error saving aplicação de questionários:", response.status);
          if (response.status === 403) {
            setSnackBarProps({
              open: true,
              type: "error",
              message: "Você não tem permissão para aplicar questionários a este paciente.",
            });
          }
          setSnackBarProps({
            open: true,
            type: "error",
            message: "Erro ao aplicar questionários.",
          });
        }
      })
      .catch((error) => {
        console.error("Error saving aplicação de questionários:", error);
        setSnackBarProps({
          open: true,
          type: "error",
          message: "Erro ao aplicar questionários.",
        });
      });
  };

  const handleSnackbarClose = () => {
    setSnackBarProps({ ...snackBarProps, open: false });
  };

  return (
    <AdminLayout>
      <Box
        sx={{
          padding: { xs: 2, md: 6 },
          paddingTop: { xs: 4, md: 6 },
          minHeight: "90vh",
          boxSizing: "border-box",
          width: "100%",
          maxWidth: "1200px",
          margin: "0 auto",
        }}
      >
        <StylizedTitle title={paciente?.nome ?? "Paciente"} />
        <Box
          sx={{
            marginBottom: 2,
            width: "100%",
          }}
        >
          <SearchBar onSearch={handleSearch} />
        </Box>
        {/* Layout em colunas empilhadas (sempre vertical) */}
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2, width: "100%" }}>
          <LabeledBox label="Resultados da Pesquisa">
            <Box sx={{ width: "100%" }}>
              {resultadosQuestionarios.map((questionario) => (
                <ResultQuestionario
                  key={questionario.id}
                  questionario={questionario}
                  onSelect={handleSelect}
                />
              ))}
            </Box>
          </LabeledBox>
          <LabeledBox label="Questionários Selecionados">
            <Box sx={{ width: "100%" }}>
              {questionariosSelecionados.map((questionario) => (
                <ResultQuestionario
                  key={questionario.id}
                  questionario={questionario}
                  onSelect={handleSelect}
                  left={false}
                />
              ))}
            </Box>
          </LabeledBox>
        </Box>
        <Button
          sx={{
            marginTop: 2,
            backgroundColor: "primary.main",
            color: "white",
            width: "100%",
          }}
          fullWidth
          variant="contained"
          onClick={handleSaveAplicacao}
        >
          Aplicar Questionários
        </Button>
      </Box>
      <Snackbar
        open={snackBarProps.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackBarProps.type as "success" | "error" | "info" | "warning"}
          sx={{ width: "100%" }}
        >
          {snackBarProps.message}
        </Alert>
      </Snackbar>
    </AdminLayout>
  );
}