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

export interface AddAdminModalProps {
    open: boolean;
    onClose: () => void;
    onAdminAdded: () => void; // Callback para atualizar a lista de admins
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

export default function AddAdminModal({ open, onClose, onAdminAdded }: AddAdminModalProps) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);

        if (password !== confirmPassword) {
            setError("As senhas não coincidem.");
            return;
        }

        if (password.length < 5) {
            setError("A senha deve ter pelo menos 5 caracteres.");
            return;
        }

        // Validação simples de email
        if (!email.includes('@') || !email.includes('.')) {
            setError("Formato de email inválido.");
            return;
        }

        setIsLoading(true);

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/user/`; // Endpoint para criar usuário

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    email: email,
                    senha: password,
                    role: 'admin', // Definindo a role como admin
                    is_active: true // Admin já nasce ativo
                }),
            });

            const data = await response.json();

            if (response.ok || response.status === 201) {
                setSuccess("Administrador adicionado com sucesso!");
                setEmail('');
                setPassword('');
                setConfirmPassword('');
                onAdminAdded(); // Chama o callback para atualizar a lista
                setTimeout(() => {
                    onClose();
                    setSuccess(null);
                }, 2000);
            } else {
                setError(data.error || "Erro ao adicionar administrador.");
            }
        } catch (err) {
            setError("Erro de conexão ao tentar adicionar administrador.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClose = () => {
        setError(null);
        setSuccess(null);
        setEmail('');
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
                    Adicionar Novo Administrador
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} fullWidth margin="normal" required />
                    <TextField label="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth margin="normal" required />
                    <TextField label="Confirmar Senha" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} fullWidth margin="normal" required />
                    {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
                    <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={isLoading}>
                        {isLoading ? <CircularProgress size={24} /> : "Adicionar Administrador"}
                    </Button>
                </form>
            </Box>
        </Modal>
    );
}