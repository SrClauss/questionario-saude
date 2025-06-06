import React, { useState } from 'react';
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    IconButton,
    CircularProgress,
    Alert
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { auth } from '../utils/auth';

interface ChangePasswordModalProps {
    open: boolean;
    onClose: () => void;
    userId: string | null;
    userName?: string; // Opcional, para exibir o nome do usuário no modal
}

const modalStyle = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    borderRadius: 2,
};

export default function ChangePasswordModal({ open, onClose, userId, userName }: ChangePasswordModalProps) {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);

        if (!userId) {
            setError("ID do usuário não fornecido.");
            return;
        }

        if (password !== confirmPassword) {
            setError("As senhas não coincidem.");
            return;
        }

        if (password.length < 5) {
            setError("A senha deve ter pelo menos 5 caracteres.");
            return;
        }

        setIsLoading(true);

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken(); // Ou localStorage.getItem("@App:token");
        const url = `${baseUrl}/user/set_password`;

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ id: userId, password: password }),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess("Senha alterada com sucesso!");
                setPassword('');
                setConfirmPassword('');
                setTimeout(() => {
                    onClose();
                    setSuccess(null);
                }, 2000);
            } else {
                setError(data.error || "Erro ao alterar a senha.");
            }
        } catch (err) {
            setError("Erro de conexão ao tentar alterar a senha.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClose = () => {
        setError(null);
        setSuccess(null);
        setPassword('');
        setConfirmPassword('');
        onClose();
    }

    return (
        <Modal open={open} onClose={handleClose}>
            <Box sx={modalStyle}>
                <IconButton onClick={handleClose} sx={{ position: 'absolute', right: 8, top: 8 }}>
                    <CloseIcon />
                </IconButton>
                <Typography variant="h6" component="h2" gutterBottom>
                    Alterar Senha {userName && `de ${userName}`}
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Nova Senha"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        fullWidth
                        margin="normal"
                        required
                    />
                    <TextField
                        label="Confirmar Nova Senha"
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        fullWidth
                        margin="normal"
                        required
                    />
                    {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
                    <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={isLoading}>
                        {isLoading ? <CircularProgress size={24} /> : "Alterar Senha"}
                    </Button>
                </form>
            </Box>
        </Modal>
    );
}