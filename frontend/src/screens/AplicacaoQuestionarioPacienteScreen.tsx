import { useState } from "react";
import {
  Snackbar,
  Alert,
  Button,
  Box,
} from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";
import { Paciente } from "../types/user";
import AdminLayout from "../layouts/AdminLayout";
import StylizedTitle from "../components/StylizedTitle";
import ResultPaciente from "../components/ResultPaciente";
import LabeledBox from "../components/LabeledBox";

export default function AplicacaoQuestionarioPacienteScreen() {
  const [snackBarProps, setSnackBarProps] = useState({
    open: false,
    type: "success",
    message: "",
  });
  const [resultadosPacientes, setResultadosPacientes] = useState<Paciente[]>([]);
  const [pacientesSelecionados, setPacientesSelecionados] = useState<Paciente[]>([]);
  const { id: questionarioId } = useParams();
  const navigate = useNavigate();

  const handleSearch = (query: string) => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    if (query.length < 3) {
      return;
    }
    const url = `${baseUrl}/pacientes/filter_by_name/${query}`;
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setResultadosPacientes(data);
      })
      .catch((error) => {
        console.error("Error fetching pacientes:", error);
      });
  };

  const handleSaveBateriaTestes = () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    const profissionalSaudeId = JSON.parse(localStorage.getItem("@App:profile") || "{}")['id'];
    const url = `${baseUrl}/baterias_testes/batch_save`;
    const payload = {
      profissional_saude_id: profissionalSaudeId,
      baterias: pacientesSelecionados.map((paciente) => ({
        paciente_id: paciente.id,
        colaborador_id: null,
        questionario_id: questionarioId,
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
            message: "Baterias de testes salvas com sucesso!",
          });
          // Navega para a tela questionarioscreen após 1,5s para exibir o snackbar
          setTimeout(() => {
            navigate("/questionario");
          }, 1500);
        } else {
          setSnackBarProps({
            open: true,
            type: "error",
            message: "Erro ao salvar baterias de testes.",
          });
        }
      })
      .catch((error) => {
        console.error("Error saving baterias de testes:", error);
        setSnackBarProps({
          open: true,
          type: "error",
          message: "Erro ao salvar baterias de testes.",
        });
      });
  };

  const handleSelect = (paciente: Paciente) => {
    const pacienteJaSelecionado = pacientesSelecionados.find(
      (p) => p.id === paciente.id
    );
    if (pacienteJaSelecionado) {
      setPacientesSelecionados((prev) =>
        prev.filter((p) => p.id !== paciente.id)
      );
      setResultadosPacientes((prev) => [...prev, paciente]);
    } else {
      setPacientesSelecionados((prev) => [...prev, paciente]);
      setResultadosPacientes((prev) =>
        prev.filter((p) => p.id !== paciente.id)
      );
    }
  };

  const handleUnselect = (paciente: Paciente) => {
    const pacienteJaSelecionado = pacientesSelecionados.find(
      (p) => p.id === paciente.id
    );
    if (pacienteJaSelecionado) {
      setPacientesSelecionados((prev) =>
        prev.filter((p) => p.id !== paciente.id)
      );
      setResultadosPacientes((prev) => [...prev, paciente]);
    } else {
      setPacientesSelecionados((prev) => [...prev, paciente]);
      setResultadosPacientes((prev) =>
        prev.filter((p) => p.id !== paciente.id)
      );
    }
  };

  const handleSnackbarClose = () => {
    setSnackBarProps({ ...snackBarProps, open: false });
  };

  return (
    <AdminLayout>
      <Box
        sx={{
          padding: { xs: 1, md: 6 },
          paddingTop: { xs: 4, md: 6 },
          height: "90vh",
          boxSizing: "border-box",
          width: "100%",
          maxWidth: "1200px",
          margin: "0 auto",
        }}
      >
        <StylizedTitle title="Aplicação de Questionário" />
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: 2,
            width: "100%",
          }}
        >
          <SearchBar onSearch={handleSearch} />
        </Box>

        <Box sx={{ width: "100%" }}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              flexDirection: { xs: "column", md: "row" },
              gap: 2,
              width: "100%",
            }}
          >
            <LabeledBox label="Resultados da Busca">
              <Box sx={{ flex: 1, width: "100%" }}>
                {resultadosPacientes.map((paciente) => (
                  <ResultPaciente
                    key={paciente.id}
                    paciente={paciente}
                    onSelect={handleSelect}
                  />
                ))}
              </Box>
            </LabeledBox>
            <LabeledBox label="Pacientes Selecionados">
              <Box sx={{ flex: 1, width: "100%" }}>
                {pacientesSelecionados.map((paciente) => (
                  <ResultPaciente
                    key={paciente.id}
                    paciente={paciente}
                    onSelect={handleUnselect}
                    left={false}
                  />
                ))}
              </Box>
            </LabeledBox>
          </Box>
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
          onClick={handleSaveBateriaTestes}
        >
          Salvar Baterias de Testes
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