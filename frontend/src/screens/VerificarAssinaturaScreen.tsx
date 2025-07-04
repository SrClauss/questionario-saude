import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, CircularProgress, Alert, Paper, Container, Link } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface VerificacaoInfo {
    medico_nome?: string;
    medico_crm?: string;
    data_assinatura?: string;
    mensagem?: string;
}

export default function VerificarAssinaturaScreen() {
    const { dados_criptografados } = useParams<{ dados_criptografados: string }>();
    const [verificacao, setVerificacao] = useState<VerificacaoInfo | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (dados_criptografados) {
            const fetchVerificacao = async () => {
                setLoading(true);
                setError(null);
                try {
                    // A URL do backend é prefixada com /backend/laudos/
                    let backendUrl = import.meta.env.VITE_BACKEND_URL || ''; // Garante que backendUrl não seja undefined
                    // Remove /backend do final de backendUrl se já estiver presente, para evitar duplicação
                    if (backendUrl.endsWith('/backend')) {
                        backendUrl = backendUrl.slice(0, -'/backend'.length);
                    }
                    // Constrói a URL final corretamente
                    const apiUrl = `${backendUrl}/backend/laudos/verificar_assinatura_qr/${dados_criptografados}`;
                    const response = await fetch(apiUrl);
                    const data = await response.json();

                    if (response.ok) {
                        setVerificacao(data);
                    } else {
                        setError(data.error || 'Erro ao verificar assinatura.');
                    }
                } catch (err) {
                    setError('Não foi possível conectar ao servidor para verificar a assinatura.');
                    console.error("Erro na chamada de verificação:", err);
                } finally {
                    setLoading(false);
                }
            };
            fetchVerificacao();
        } else {
            setError("Dados de verificação não fornecidos na URL.");
            setLoading(false);
        }
    }, [dados_criptografados]);

    if (loading) {
        return (
            <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <CircularProgress />
                <Typography sx={{ mt: 2 }}>Verificando assinatura...</Typography>
            </Box>
        );
    }

    return (
        <Container component="main" maxWidth="sm" sx={{ mt: 8, mb: 4 }}>
            <Paper elevation={3} sx={{ p: { xs: 2, sm: 4 }, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Typography variant="h5" component="h1" gutterBottom textAlign="center">
                    Verificação de Assinatura do Laudo
                </Typography>
                {error && (
                    <Alert severity="error" icon={<ErrorOutlineIcon fontSize="inherit" />} sx={{ width: '100%', mb: 2 }}>
                        {error}
                    </Alert>
                )}
                {verificacao && !error && (
                    <Alert severity="success" icon={<CheckCircleOutlineIcon fontSize="inherit" />} sx={{ width: '100%', mb: 2, textAlign: 'left' }}>
                        <Typography variant="subtitle1" component="div"><strong>{verificacao.mensagem || 'Assinatura Válida'}</strong></Typography>
                        <Typography variant="body2"><strong>Médico:</strong> {verificacao.medico_nome || 'N/A'}</Typography>
                        <Typography variant="body2"><strong>CRM:</strong> {verificacao.medico_crm || 'N/A'}</Typography>
                        <Typography variant="body2">
                            <strong>Data da Assinatura (Referência):</strong> {verificacao.data_assinatura ? new Date(verificacao.data_assinatura).toLocaleString('pt-BR') : 'N/A'}
                        </Typography>
                    </Alert>
                )}
                <Link href="/" variant="body2" sx={{ mt: 2 }}>Voltar para a página inicial</Link>
            </Paper>
        </Container>
    );
}