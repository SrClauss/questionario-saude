import { Box, Typography, TextField, Button, useTheme, useMediaQuery, Snackbar, Alert } from "@mui/material"
import { useState, useLayoutEffect } from 'react'
import logoLaranja from '../assets/img/logo-laranja.png'
import { useNavigate } from "react-router-dom"
import { auth } from "../utils/auth"

export default function LoginScreen() {
    const navigate = useNavigate()
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [containerSize, setContainerSize] = useState(500);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [feedback, setFeedback] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [feedbackSeverity, setFeedbackSeverity] = useState<'success' | 'error' | 'warning' | 'info'>('error');

    useLayoutEffect(() => {
        const calculateSize = () => {
            const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

            if (vw >= 1920) {
                setContainerSize(600);
            } else if (vw >= 1366) {
                setContainerSize(500);
            } else if (vw >= 1024) {
                setContainerSize(400);
            } else if (vw >= 768) {
                setContainerSize(350);
            } else {
                setContainerSize(300);
            }
        };

        calculateSize();
        window.addEventListener('resize', calculateSize);

        return () => window.removeEventListener('resize', calculateSize);
    }, []);

    const handleLogin = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL
        setLoading(true)
        setFeedback('')
        setOpenSnackbar(false)
        setFeedbackSeverity('error')

        try {
            const response = await fetch(`${baseUrl}/user/users/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setFeedback('Login realizado com sucesso!');
                setFeedbackSeverity('success');
                setOpenSnackbar(true);


             
            
                auth.setToken(data);
                setTimeout(() => {
                    navigate('/');
                }, 1500);
            } else {
                setFeedback(data.message || 'Falha ao realizar o login');
                setFeedbackSeverity('error');
                setOpenSnackbar(true);
            }

        } catch (error: any) {
            setFeedback(`Erro ao realizar o login: ${error.message}`);
            setFeedbackSeverity('error');
            setOpenSnackbar(true);
        } finally {
            setLoading(false);
        }
    }
    
    const handleCloseSnackbar = (event?: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }
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
                            alt="Mental Health Logo"
                            sx={styles.image}
                        />
                    </Box>
                )}

                <Box sx={styles.formBox(isMobile, containerSize)}>
                    <Typography
                        variant={isMobile ? "h5" : "h4"}
                        component="h1"
                        sx={styles.title}>
                        Login
                    </Typography>

                    <TextField
                        label="Email"
                        variant="outlined"
                        fullWidth
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        sx={styles.textField}
                        disabled={loading}
                    />

                    <TextField
                        label="Senha"
                        variant="outlined"
                        fullWidth
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        type="password"
                        sx={styles.textField}
                        disabled={loading}
                    />

                    <Button
                        variant="contained"
                        color="primary"
                        fullWidth
                        onClick={handleLogin}
                        size="large"
                        sx={styles.button}
                        disabled={loading}
                    >
                        {loading ? 'Entrando...' : 'Entrar'}
                    </Button>
                </Box>
            </Box>
            <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
                <Alert onClose={handleCloseSnackbar} severity={feedbackSeverity} sx={{ width: '100%' }}>
                    {feedback}
                </Alert>
            </Snackbar>
        </Box>
    )
}

const styles = {
    mainContainer: {
        position: 'fixed',
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
    logo: {
        width: '8vh',
        marginRight: '8px',
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
    }
}