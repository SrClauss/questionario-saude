import React, { useState, useLayoutEffect, useEffect } from 'react';
import { Box, Typography, TextField, Button, Snackbar, Alert, useTheme, useMediaQuery } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode'; // Certifique-se de instalar: npm install jwt-decode
import logoLaranja from '../assets/img/logo-laranja.png';

interface TokenPayload {
  user_id: string;
  nome: string;
  exp: number;
}

export default function ConfirmPasswordScreen() {
  const navigate = useNavigate();
  const { token } = useParams<{ token: string }>(); // Exemplo: rota /confirm-password/:token
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [containerSize, setContainerSize] = useState(500);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [userName, setUserName] = useState('');
  const [userId, setUserId] = useState<string | null>(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [feedbackSeverity, setFeedbackSeverity] = useState<'success' | 'error'>('success');

  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  // A chave secreta não será utilizada aqui, pois jwt-decode não realiza verificação
  // const secretKey = import.meta.env.VITE_SECRET_KEY;

  // Responsividade similar à LoginScreen
  useLayoutEffect(() => {
    const calculateSize = () => {
      const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      if (vw >= 1920) setContainerSize(600);
      else if (vw >= 1366) setContainerSize(500);
      else if (vw >= 1024) setContainerSize(400);
      else if (vw >= 768) setContainerSize(350);
      else setContainerSize(300);
    };
    calculateSize();
    window.addEventListener('resize', calculateSize);
    return () => window.removeEventListener('resize', calculateSize);
  }, []);

  // Decodifica o token utilizando jwt-decode para extrair id e nome
  useEffect(() => {
    if (!token) return;
    try {
      const decoded = jwtDecode<TokenPayload>(token);
      setUserName(decoded.nome);
      setUserId(decoded.user_id);
    } catch (err: any) {
      setFeedback('Token inválido.');
      setFeedbackSeverity('error');
      setOpenSnackbar(true);
    }
  }, [token]);

  const handleSubmit = async () => {
    if (password !== confirmPassword) {
      setFeedback('As senhas não coincidem.');
      setFeedbackSeverity('error');
      setOpenSnackbar(true);
      return;
    }
    if (!userId) {
      setFeedback('Informações do usuário ausentes.');
      setFeedbackSeverity('error');
      setOpenSnackbar(true);
      return;
    }
    try {
      const response = await fetch(`${backendUrl}/user/users/set_password`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: userId, password }),
      });
      if (response.ok) {
        setFeedback('Senha atualizada com sucesso!');
        setFeedbackSeverity('success');
        setOpenSnackbar(true);
        setTimeout(() => navigate('/login'), 2000);
      } else {
        const errorData = await response.json();
        setFeedback(errorData.message || 'Erro ao atualizar senha.');
        setFeedbackSeverity('error');
        setOpenSnackbar(true);
      }
    } catch (error: any) {
      setFeedback('Erro de conexão.');
      setFeedbackSeverity('error');
      setOpenSnackbar(true);
    }
  };

  const handleCloseSnackbar = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') return;
    setOpenSnackbar(false);
  };

  return (
    <Box sx={{ ...styles.mainContainer, p: isMobile ? 2 : 0 }}>
      <Box sx={styles.formContainer(isMobile, containerSize)}>
        {!isMobile && (
          <Box sx={styles.imageBox(containerSize)}>
            <Box
              component="img"
              src={logoLaranja}
              alt="Logo"
              sx={styles.image}
            />
          </Box>
        )}
        <Box sx={styles.formBox(isMobile, containerSize)}>
          <Typography variant={"h6"} component="h1" sx={styles.title}>
            {userName ? `Bem-vindo, ${userName}` : 'Confirmação de Senha'}
          </Typography>
          <TextField
            label="Nova Senha"
            type="password"
            variant="outlined"
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={styles.textField}
            required
          />
          <TextField
            label="Confirmar Nova Senha"
            type="password"
            variant="outlined"
            fullWidth
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            sx={styles.textField}
            required
          />
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleSubmit}
            sx={styles.button}
          >
            Atualizar Senha
          </Button>
        </Box>
      </Box>
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
        <Alert onClose={handleCloseSnackbar} severity={feedbackSeverity} sx={{ width: '100%' }}>
          {feedback}
        </Alert>
      </Snackbar>
    </Box>
  );
}

const styles = {
  mainContainer: {
    position: 'fixed' as const,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  formContainer: (isMobile: boolean, containerSize: number) => ({
    display: 'flex',
    boxShadow: 3,
    borderRadius: isMobile ? '8px' : '16px',
    overflow: 'hidden',
    height: isMobile ? 'auto' : containerSize,
    width: isMobile ? '100%' : containerSize * 2,
    flexDirection: isMobile ? 'column' : 'row',
  }),
  imageBox: (containerSize: number) => ({
    width: containerSize,
    height: '100%',
  }),
  image: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  formBox: (isMobile: boolean, containerSize: number) => ({
    width: isMobile ? '100%' : containerSize,
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: isMobile ? 3 : 7,
    boxSizing: 'border-box',
    height: isMobile ? 'auto' : '100%',
    minHeight: isMobile ? '50vh' : 'none',
  }),
  title: {
    mb: 4,
    fontWeight: 600,
    textAlign: 'center',
    color: '#fc9e22',
  },
  textField: {
    mb: 4,
    '& label': { color: '#fc9e22' },
    '& label.Mui-focused': { color: '#fc9e22' },
    '& .MuiOutlinedInput-root': {
      '& fieldset': { borderColor: '#fc9e22' },
      '&:hover fieldset': { borderColor: '#fc9e22' },
      '&.Mui-focused fieldset': { borderColor: '#fc9e22' },
      '&.Mui-disabled': {
        backgroundColor: 'rgba(0, 0, 0, 0.05)',
        '& fieldset': { borderColor: 'rgba(0, 0, 0, 0.26)' },
      },
      '& input:disabled': {
        color: 'rgba(0, 0, 0, 0.38)',
        WebkitTextFillColor: 'rgba(0, 0, 0, 0.38)',
      },
    },
    '& label.Mui-disabled': {
      color: 'rgba(0, 0, 0, 0.38)',
    },
  },
  button: {
    mt: 2,
    backgroundColor: '#fc9e22',
    '&:hover': { backgroundColor: '#e68a1a' },
    '&.Mui-disabled': {
      backgroundColor: 'rgba(0, 0, 0, 0.12)',
      color: 'rgba(0, 0, 0, 0.26)',
    },
  },
};