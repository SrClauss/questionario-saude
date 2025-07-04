import { Card, CardContent, Divider, Typography, Box, Chip, Accordion, AccordionSummary, AccordionDetails, List, ListItem, ListItemText, Button } from "@mui/material";
import {AvaliacaoFetch} from "./ComponenteAvaliacao"
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { CheckCircleOutline, HourglassEmpty, Person, Assignment, LibraryBooks, Analytics } from '@mui/icons-material';
import { useNavigate } from "react-router-dom";
interface ComponenteAvaliacaoMedicoProps {
  avaliacaoFetch: AvaliacaoFetch;
}

export default function ComponenteAvaliacaoMedico({ avaliacaoFetch }: ComponenteAvaliacaoMedicoProps){
    const { avaliacao, paciente, baterias_testes } = avaliacaoFetch;
    const navigate = useNavigate();
    const formatDate = (dateString: string | null | undefined) => {
        if (!dateString) return 'N/A';
        try {
            return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
        } catch {
            return 'Data inválida';
        }
    };

    return(
        <Card sx={{ margin: 2, boxShadow: 3, borderRadius: 2 }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Person sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        Paciente: {paciente.nome}
                    </Typography>
                </Box>

                <Box sx={{ display: 'flex', flexWrap: 'wrap', mb: 2, gap: 2 }}>
                    <Box sx={{ width: { xs: '100%', sm: 'calc(50% - 8px)'} }}> {/* Ajuste para o gap */}
                        <Typography variant="body1"><strong>CPF:</strong> {paciente.cpf || "Não informado"}</Typography>
                    </Box>
                    <Box sx={{ width: { xs: '100%', sm: 'calc(50% - 8px)'} }}> {/* Ajuste para o gap */}
                        <Typography variant="body1"><strong>Data de Nascimento:</strong> {formatDate(paciente.data_nascimento)}</Typography>
                    </Box>
                </Box>

                <Accordion sx={{ boxShadow: 'none', '&:before': { display: 'none' }, borderTop: '1px solid', borderColor: 'divider', mt: 2 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        sx={{ 
                            flexDirection: 'row-reverse', // Mantém o ícone à esquerda do texto
                            paddingLeft: 0, // Encosta o conjunto (ícone + texto) à borda esquerda do AccordionSummary
                            '& .MuiAccordionSummary-content': { marginLeft: 1 } // Mantém o espaçamento que você já tinha entre o ícone e o texto
                        }}
                    >
                        <Typography sx={{ fontWeight: 'medium', color: 'text.secondary' }}>Mais Detalhes</Typography>
                    </AccordionSummary>
                    <AccordionDetails sx={{ pt: 0, px:0 }}> {/* Remover padding padrão para alinhar com o CardContent */}
                        <Box>
                            <Divider sx={{ mb: 2 }} />

                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Assignment sx={{ mr: 1, color: 'secondary.main' }} />
                                <Typography variant="h6" sx={{ fontWeight: 'medium', color: 'secondary.main' }}>
                                    Detalhes da Avaliação
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', mb: 2, gap: 1 }}>
                                <Box sx={{ width: { xs: '100%', sm: 'calc(50% - 4px)' } }}> {/* Ajuste para o gap */}
                                    <Typography variant="body1"><strong>ID da Avaliação:</strong> {avaliacao.id}</Typography>
                                </Box>
                                <Box sx={{ width: { xs: '100%', sm: 'calc(50% - 4px)' } }}> {/* Ajuste para o gap */}
                                    <Typography variant="body1"><strong>Data de Início:</strong> {formatDate(avaliacao.data_inicio)}</Typography>
                                </Box>
                            </Box>

                            {baterias_testes && baterias_testes.length > 0 && (
                                <>
                                    <Divider sx={{ my: 2 }} />
                                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                        <LibraryBooks sx={{ mr: 1, color: 'info.main' }} />
                                        <Typography variant="h6" sx={{ fontWeight: 'medium', color: 'info.main' }}>
                                            Baterias de Testes Aplicadas ({baterias_testes.length})
                                        </Typography>
                                    </Box>
                                    {baterias_testes.map((bateria, index) => (
                                        <Accordion key={bateria.id || index} sx={{ mb: 1, '&:before': { display: 'none' }, border: '1px solid', borderColor: 'divider' }}>
                                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                                <Typography sx={{ fontWeight: 'medium' }}>{bateria.questionario?.titulo || "Questionário não identificado"}</Typography>
                                            </AccordionSummary>
                                            <AccordionDetails sx={{ bgcolor: 'action.hover' }}>
                                                <List dense>
                                                    <ListItem>
                                                        <ListItemText primary="Data de Aplicação" secondary={formatDate(bateria.data_aplicacao)} />
                                                    </ListItem>
                                                    <ListItem>
                                                        <ListItemText 
                                                            primary="Status" 
                                                            secondary={
                                                                <Chip
                                                                    label={bateria.is_completo ? "Completo" : "Incompleto"}
                                                                    color={bateria.is_completo ? "success" : "warning"}
                                                                    size="small"
                                                                    icon={bateria.is_completo ? <CheckCircleOutline fontSize="small"/> : <HourglassEmpty fontSize="small"/>}
                                                                />}
                                                            slotProps={{ secondary: { component: 'div' } }} // Alterado para a nova API slotProps
                                                        />
                                                    </ListItem>
                                                    {bateria.observacoes && <ListItem><ListItemText primary="Observações" secondary={bateria.observacoes} /></ListItem>}
                                                    <ListItem>
                                                        <ListItemText primary="Respostas Registradas" secondary={bateria.respostas ? Object.keys(bateria.respostas).length : 0} />
                                                    </ListItem>
                                                </List>
                                            </AccordionDetails>
                                        </Accordion>
                                    ))}
                                    <Button variant="contained" fullWidth sx={{ mt: 2 }} startIcon={<Analytics />} onClick={() => navigate(`/estatisticas/${avaliacao.id}`)} >Ver Estatísticas</Button>
                                    
                                </>
                            )}
                        </Box>
                    </AccordionDetails>
                </Accordion>
            </CardContent>
        </Card>
    )
}