import React, { useState, useEffect } from 'react';
import { Box, Typography, Container, Avatar, Fab, Snackbar, Alert, CircularProgress, Button } from '@mui/material';
import { auth } from '../utils/auth';
import { BateriaTestes } from '../types/baterias';
import { Questionario } from '../types/questionario';
import { Paciente } from '../types/user';
import { useNavigate } from 'react-router-dom';
import PieChartResultados from '../components/PieChartResultados';
import AvatarProgresso from '../components/AvatarProgresso';
import { ExitToApp } from '@mui/icons-material';

export interface BateriaTestesState {
  bateria: BateriaTestes;
  qtd_perguntas: number;
  questionario: Questionario;
}

const PacienteHomeScreen: React.FC = () => {
  const userId = auth.getUserData()?.id;
  const [baterias, setBaterias] = useState<BateriaTestesState[]>([]);
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error" | "warning" | "info">("success");
  const [userImage, setUserImage] = useState<string | null>(null);
  const [loadingImage, setLoadingImage] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPaciente = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/pacientes/get_paciente_by_user_id/${userId}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
            },
          }
        );
        const data = await response.json();
        setPaciente(data);
      } catch (error) {
        console.error('Error fetching paciente:', error);
      }
    };
    if (userId) fetchPaciente();
  }, [userId]);

  useEffect(() => {
    const ensurePerfilSaude = async () => {
      if (!paciente) return;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/ensure_perfil_de_saude/${paciente.id}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
            },
            body: JSON.stringify({ paciente_id: paciente.id }),
          }
        );
        const data = await response.json();
        console.log('Perfil de saúde:', data);
      } catch (error) {
        console.error('Erro ensuring perfil de saúde:', error);
        setSnackbarMessage("Erro ao garantir perfil de saúde");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    };
    const fetchBaterias = async () => {
      if (!paciente) return;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/baterias_testes/paciente/${paciente.id}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
            },
          }
        );
        const data = await response.json();
        setBaterias(data);
      } catch (error) {
        console.error('Erro ao buscar baterias:', error);
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
            method: 'GET',
            headers: {
              Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
            },
          }
        );
        if (response.ok) {
          const imageBlob = await response.blob();
          setUserImage(URL.createObjectURL(imageBlob));
        } else {
          console.error('Erro ao buscar imagem do usuário:', response.status);
          setUserImage(null);
        }
      } catch (error) {
        console.error('Erro ao buscar imagem do usuário:', error);
        setUserImage(null);
      } finally {
        setLoadingImage(false);
      }
    };

    if (paciente) {
      ensurePerfilSaude();
      fetchBaterias();
    }
    if (userId) {
      fetchUserImage();
    }
  }, [paciente, userId]);

  const handleLogout = () => {
    localStorage.removeItem('@App:token');
    navigate('/login');
  };

  const handleCloseSnackbar = (_event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') return;
    setOpenSnackbar(false);
  };

  // Filtra a bateria cujo questionário tenha o título "Perfil de Saúde"
  const perfilDeSaudeBateria = baterias.find(
    (b) => b.questionario.titulo === "Perfil de Saúde"
  );

  // Verifica se o perfil de saúde tem 100% das respostas
  const perfilCompleto = perfilDeSaudeBateria
    ? perfilDeSaudeBateria.bateria.respostas.length === perfilDeSaudeBateria.qtd_perguntas
    : false;

  return (
    <Container maxWidth="lg" sx={{ padding: 2, height: '90vh' }}>
      <Fab
        color="primary"
        aria-label="logout"
        sx={{
          position: 'absolute',
          bottom: { xs: 55, sm: 100 },
          right: { xs: 32, sm: 150 },
        }}
        onClick={handleLogout}
      >
        <ExitToApp fontSize='large' />
      </Fab>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          backgroundColor: 'white',
          height: '100%',
          padding: 2,
          borderRadius: 2,
          boxShadow: 3,
          overflow: 'auto',
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
        />
        {!perfilCompleto && (
          <Button variant="contained" color="primary">
            Continuar Perfil de Saúde
          </Button>
        )}
      </Box>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default PacienteHomeScreen;