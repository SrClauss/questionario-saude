import React, { useState, useEffect} from "react";
import {
  Box,
  Typography,
  Snackbar,
  Alert,
  Button,
  useTheme,
  Divider
} from "@mui/material";
import { auth } from "../utils/auth";
import { BateriaTestes } from "../types/baterias";
import { Questionario } from "../types/questionario";
import { Paciente } from "../types/user";
import AvatarProgresso from "../components/AvatarProgresso";
import {
  BallotRounded,
  FactCheckRounded,
} from "@mui/icons-material";
import PacienteLayout from "../layouts/PacienteLayout";
import { useNavigate } from "react-router-dom";
export interface BateriaTestesState {
  bateria: BateriaTestes;
  qtd_perguntas: number;
  questionario: Questionario;
}

const PacienteHomeScreen: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const userId = auth.getUserData()?.id;
  const [baterias, setBaterias] = useState<BateriaTestesState[]>([]);
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<
    "success" | "error" | "warning" | "info"
  >("success");
  const [userImage, setUserImage] = useState<string | null>(null);
  const [loadingImage, setLoadingImage] = useState(false);
  const [perfilCompleto, setPerfilCompleto] = useState(false);

     const fetchBaterias = async () => {
      if (!paciente) return;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/paciente/${paciente.id
          }`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
            },
          }
        );
        const data = await response.json();
        setBaterias(data);
      } catch (error) {
        console.error("Erro ao buscar baterias:", error);
        setSnackbarMessage("Erro ao buscar baterias");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    };

    const fetchUserImage = async () => {
      if (!userId) return;
      setLoadingImage(true);
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/user/${userId}/image`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
            },
          }
        );
        if (response.ok) {
          const imageBlob = await response.blob();
          setUserImage(URL.createObjectURL(imageBlob));
        } else {
          console.error("Erro ao buscar imagem do usuário:", response.status);
          setUserImage(null);
        }
      } catch (error) {
        console.error("Erro ao buscar imagem do usuário:", error);
        setUserImage(null);
      } finally {
        setLoadingImage(false);
      }
    };

  useEffect(() => {
    const fetchPaciente = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL
          }/pacientes/get_paciente_by_user_id/${userId}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
            },
          }
        );
        const data = await response.json();
        setPaciente(data);
      } catch (error) {
        console.error("Error fetching paciente:", error);
      }
    };
    if (userId) fetchPaciente();
  }, [userId]);

  useEffect(() => {
    const ensurePerfilSaude = async () => {
      if (!paciente) return;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL
          }/baterias_testes/ensure_perfil_de_saude/${paciente.id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("@App:token")}`,
            },
            body: JSON.stringify({ paciente_id: paciente.id }),
          }
        );
        const data = await response.json();
        console.log("Perfil de saúde:", data);
        // Se a chamada foi bem-sucedida, atualiza a lista de baterias
        // para incluir o novo perfil de saúde, se criado.
        await fetchBaterias();

      } catch (error) {
        console.error("Erro ensuring perfil de saúde:", error);
        setSnackbarMessage("Erro ao garantir perfil de saúde");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    };

    if (paciente) {
      ensurePerfilSaude();
      // fetchBaterias() foi movido para dentro de ensurePerfilSaude para garantir que execute após
    }
    if (userId) {
      fetchUserImage();
    }
  }, [paciente, userId]);

  const navigateToPerfilDeSaude = () => {
    if (perfilDeSaudeBateria) {
      navigate(`/bateria/${perfilDeSaudeBateria.bateria.id}`);
    }
  };

  const handleCloseSnackbar = (
    _event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") return;
    setOpenSnackbar(false);
  };

  // Filtra a bateria cujo questionário tenha o título "Perfil de Saúde"
  const perfilDeSaudeBateria = baterias.find(
    (b) => b.questionario.titulo === "Questionário Detalhado de Perfil Básico de Saúde"
  );

  useEffect(() => {
    console.log(perfilDeSaudeBateria)
    const quantidade_respostas = Object.keys(perfilDeSaudeBateria?.bateria.respostas ?? {}).length;

    if (quantidade_respostas === 0) {
      setPerfilCompleto(false);
    } else {
      setPerfilCompleto(true);
    }
    
  }, [perfilDeSaudeBateria]);

  return (
    <PacienteLayout>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          height: "100vh",
          backgroundColor: "white",
          padding: 2,
          borderRadius: 2,
        }}
      >
        <Typography variant="h6" gutterBottom>
          Olá, {paciente?.nome}! 
        </Typography>
        <AvatarProgresso
          perfilDeSaudeBateria={perfilDeSaudeBateria}
          loadingImage={loadingImage}
          userImage={userImage}
          pacienteNome={paciente?.nome}
          onReload={fetchUserImage}

        />

        
        {!perfilCompleto && (
          <Button variant="contained" color="primary" onClick={navigateToPerfilDeSaude}>
            Continuar Perfil de Saúde
          </Button>
        )}
        <Divider sx={{ width: "100%", marginY: 2 }} />
        
        
        
        
        <Box sx={{ marginTop: 2, display: "flex", flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
          <Box
            sx={{
              backgroundColor: theme.palette.info.main,
              display: "flex",
              gap: 6,
              borderRadius: 2,
              padding: 1,
            }}
          >
            <Box
              sx={{ padding: 1, textAlign: "left", flexGrow: 1, color: "white" }}
            >
              <Typography variant="h3" sx={{ marginLeft: 1 }}>
                {baterias.length}
              </Typography>
              <Typography variant="body1">
                {baterias.length > 1 ? "Testes Aplicados" : "Teste Aplicado"}
              </Typography>
            </Box>
            <BallotRounded sx={{ fontSize: "4em" }} htmlColor="white" />
          </Box>

          <Box
            sx={{
              backgroundColor: theme.palette.success.main,
              display: "flex",
              gap: 6,
              borderRadius: 2,
              padding: 1,
            }}
          >
            <Box
              sx={{ padding: 1, textAlign: "left", flexGrow: 1, color: "white" }}
            >
              <Typography variant="h3" sx={{ marginLeft: 1 }}>
                {baterias.filter((b) => b.bateria.is_completo === true).length}
              </Typography>
              <Typography variant="body1">
                {baterias.length > 1 ? "Testes Completos" : "Teste Completo"}
              </Typography>
            </Box>
            <FactCheckRounded sx={{ fontSize: "4em" }} htmlColor="white" />
          </Box>
        </Box>



      </Box>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbarSeverity}
          sx={{ width: "100%" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </PacienteLayout>
  );
};

export default PacienteHomeScreen;
