import { Card, CardContent, CardHeader, Typography, Box, Chip, Accordion, AccordionSummary, AccordionDetails, Divider, useTheme, Fab, Tooltip, IconButton, Button } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HealingIcon from '@mui/icons-material/Healing'; // Ícone para médico
import BusinessIcon from '@mui/icons-material/Business'; // Ícone para unidade de saúde
import PersonIcon from '@mui/icons-material/Person'; // Ícone para paciente
import AssignmentIcon from '@mui/icons-material/Assignment'; // Ícone para laudo
import { Paciente, Medico } from "../types/user";
import { UnidadeSaude } from "../types/unidade_saude";
import { Avaliacao as AvaliacaoType, TipoPagamento } from "../types/avaliacao";
import { BateriaTestes } from "../types/baterias";
import { Questionario } from "../types/questionario";
import { auth } from "../utils/auth";
import { DeleteForever, MedicalInformationOutlined, MonetizationOn, PsychologyAltOutlined } from "@mui/icons-material";
import DoctorIconComponent from "./DoctorIconComponent";
import { MouseEvent, useState } from "react";
import DeleteModal from "../modals/DeleteDialog";
import PagamentoModal from "../modals/PagamentoModal";
// Tipos que já existem no seu AvaliacaoScreen.tsx
interface BateriasTestesJoin extends BateriaTestes {
    questionario: Questionario;
}

export interface AvaliacaoJoin {
    avaliacao: AvaliacaoType;
    baterias_testes: BateriasTestesJoin[];
    paciente: Paciente;
    unidade_saude: UnidadeSaude;
    medico: Medico | null; // Médico pode ser nulo
}

interface CardAvaliacaoProps {
    avaliacaoJoin: AvaliacaoJoin;
    onOpenBateriaModal: () => void;
    onOpenLaudoModal: () => void;
    onOpenMedicoModal: (avaliacaoId: string) => void;
    onRefresh: () => void;
    onDeleteAvaliacao: () => void;
}

export default function CardAvaliacao({ avaliacaoJoin, onOpenBateriaModal, onOpenLaudoModal, onOpenMedicoModal, onRefresh, onDeleteAvaliacao }: CardAvaliacaoProps) {
    const theme = useTheme();
    const role = auth.getUserData()?.role;
    const { avaliacao, baterias_testes, paciente, unidade_saude, medico } = avaliacaoJoin;
    const [bateriaToDelete, setBateriaToDelete] = useState<string | null>(null);
    const [isPagamentoModalOpen, setIsPagamentoModalOpen] = useState(false);
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
    };

    const formatCurrency = (value: number | null | undefined) => {
        if (value === null || value === undefined) {
            return 'Não definido';
        }
        return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    const formatPaymentType = (type: TipoPagamento | undefined) => {
        if (!type) return 'N/A';
        const paymentTypes: Record<TipoPagamento, string> = {
            'cartao_credito': 'Cartão de Crédito', 'debito': 'Débito', 'pix': 'PIX', 'dinheiro': 'Dinheiro', '': 'Não especificado'
        };
        return paymentTypes[type] || type;
    };

    const handleClosePagamentoModal = (shouldRefresh?: boolean) => {
        setIsPagamentoModalOpen(false);
        if (shouldRefresh) {
            onRefresh();
        }
    };

    const [openDeleteModal, setOpenDeleteModal] = useState(false);
    
    const handleOpenDeleteModal = (e: MouseEvent, bateriaId: string) => {
        e.stopPropagation();
        setBateriaToDelete(bateriaId);
        setOpenDeleteModal(true);
    }
    const handleDeleteBateria = async () => {


        

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/baterias_testes/${bateriaToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${auth.getToken()}`,
                },
            });
            if (response.status === 204) {
                console.log('Bateria excluida com sucesso');
            } else {
                const data = await response.json();
                console.error(`Erro ao excluir bateria: ${data.message || 'Erro desconhecido'}`);
            }
        } catch (error) {
            console.error(`Erro na requisicao de exclusao: ${error}`);
        }
        finally {
            setBateriaToDelete(null);
            setOpenDeleteModal(false);
            onRefresh();
        }
    }
    return (
        <Card sx={{
            backgroundColor: "white",
        
            position: 'relative', // Essencial para o posicionamento absoluto do Fab
            paddingBottom: 7
        }}>
            <CardHeader
                title={`Avaliação`}
            
                subheader={`Iniciada em: ${formatDate(avaliacao.data_inicio)}`}
                action={


                    // Ícone foi removido do Chip, pois o Chip já tem um comportamento visual para "success" e "warning"
                    <Chip
                        label={avaliacao.fechada ? "Concluída" : "Em Aberto"}
                        color={avaliacao.fechada ? "success" : "warning"}
                        size="small"
                    />
           
        
                }
            />
            <CardContent>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <PersonIcon color="action" />
                        <Typography variant="body1">
                            <strong>Paciente:</strong> {paciente?.nome || "N/A"}
                        </Typography>
                    </Box>
                    {medico && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <HealingIcon color="action" />
                            <Typography variant="body1">
                                <strong>Médico Responsável:</strong> {medico.nome} (CRM: {medico.crm})
                            </Typography>
                        </Box>
                    )}
                    {unidade_saude && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <BusinessIcon color="action" />
                            <Typography variant="body1">
                                <strong>Unidade de Saúde:</strong> {unidade_saude.nome}
                            </Typography>
                        </Box>
                    )}

                    {avaliacao.laudo_id && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <AssignmentIcon color="action" />
                            <Typography variant="body1">
                                <strong>Laudo ID:</strong> {avaliacao.laudo_id}
                            </Typography>
                        </Box>
                    )}
                </Box>

                {/* Seção de Pagamento - Visível apenas para Admin e Colaborador */}
                {(role === 'admin' || role === 'colaborador') && (
                    <Accordion sx={{ mt: 2, boxShadow: 'none', '&:before': { display: 'none' }, borderTop: '1px solid', borderColor: 'divider' , backgroundColor: "white"}}>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="payment-panel-content"
                            id="payment-panel-header"
                            
                        >
                            <Typography sx={{ fontWeight: 'medium', color: 'text.secondary' }}>Informações Financeiras</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <MonetizationOn color="action" />
                                    <Typography variant="body1">
                                        <strong>Valor:</strong> {formatCurrency(avaliacao.valor_cobranca)}
                                    </Typography>
                                </Box>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Chip
                                        label={avaliacao.pago ? "Pago" : "Pendente"}
                                        color={avaliacao.pago ? "success" : "warning"}
                                        size="small"
                                    />
                                    {avaliacao.pago && avaliacao.tipo_pagamento && (
                                        <Typography variant="body2" sx={{ ml: 1 }}>({formatPaymentType(avaliacao.tipo_pagamento)})</Typography>
                                    )}
                                </Box>
                                <Button
                                    variant="contained"
                                    size="small"
                                    onClick={() => setIsPagamentoModalOpen(true)}
                                    sx={{ mt: 1, alignSelf: 'flex-start' }}
                                >
                                    {avaliacao.pago ? 'Editar Pagamento' : 'Registrar Pagamento'}
                                </Button>
                            </Box>
                        </AccordionDetails>
                    </Accordion>
                )}

                {baterias_testes && baterias_testes.length > 0 && (
                    <>

                        <Divider sx={{ marginY: 2 }} />
                        <Typography variant="h6" gutterBottom sx={{ color: theme.palette.primary.main }}>
                            Baterias de Testes Aplicadas
                        </Typography>
                        {baterias_testes.map((bateria, index) => (
                            <Accordion key={bateria.id || index} sx={{
                                border: `1px solid ${theme.palette.divider}`,
                                '&:not(:last-child)': {
                                    borderBottom: 0,
                                },
                                '&:before': {
                                    display: 'none',
                                },
                                mb: 1,
                                backgroundColor: "white"
                            }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls={`panel${index}-content`}
                                    id={`panel${index}-header`}
                                    sx={{ backgroundColor: "white" }}
                                >
                                    <Typography sx={{ fontWeight: 'medium' }}>
                                        {bateria.questionario?.titulo || "Questionário não identificado"}
                                    </Typography>
                                    <Chip
                                        label={bateria.is_completo ? "Completo" : "Incompleto"}
                                        color={bateria.is_completo ? "success" : "default"}
                                        size="small"
                                        sx={{ marginLeft: 'auto', marginRight: 1 }}
                                    />
                                    <IconButton onClick={(e) => handleOpenDeleteModal(e, bateria.id)}>
                                        <DeleteForever color="error" />
                                   </IconButton>
                                </AccordionSummary>
                                <AccordionDetails sx={{ backgroundColor: theme.palette.background.default }}>
                                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                                        <Typography variant="body2">
                                            <strong>Questionário:</strong> {bateria.questionario?.titulo} (Versão: {bateria.questionario?.versao || 'N/A'})
                                        </Typography>
                                        <Typography variant="body2">
                                            <strong>Data de Aplicação:</strong> {formatDate(bateria.data_aplicacao)}
                                        </Typography>
                                        <Typography variant="body2">
                                            <strong>Observações:</strong> {bateria.observacoes || "Nenhuma"}
                                        </Typography>

                                    </Box>
                                </AccordionDetails>
                            </Accordion>
                        ))}
                    </>
                )}
            </CardContent>
            {
                (role === "profissional_saude" || role === "admin") && (

                    <Tooltip title="Adicionar Bateria de Testes" placement="top-end">
                        <Fab
                            color="secondary"
                            size="small"
                            aria-label="add"
                            sx={{
                                position: 'absolute',
                                bottom: 16,
                                right: 16
                            }}
                            onClick={(e)=>{
                                e.preventDefault();
                                onOpenBateriaModal();
                            }}
                            
                            >
                            <PsychologyAltOutlined /> {/* Adicione um ícone ao Fab */}
                        </Fab>
                    </Tooltip>
                )
            }
            {
                (role === "medico" || role === "admin" || role === "profissional_saude") && (
                    <Tooltip title={role === 'medico' ? "Adicionar Laudo" : "Apenas médicos podem adicionar laudos"} placement="top-end">
                        {/* O Tooltip precisa de um wrapper (span) para funcionar em botões desabilitados */}
                        <span>
                            <Fab
                                color="secondary"
                                size="small"
                                aria-label="add"
                                disabled={role !== 'medico'}
                                onClick={(e) => {
                                    if (role === 'medico') {
                                        e.preventDefault();
                                        onOpenLaudoModal();
                                    }
                                }}
                                sx={{
                                    position: 'absolute',
                                    bottom: 16,
                                    right: 66
                                }}>
                                <MedicalInformationOutlined />
                            </Fab>
                        </span>
                    </Tooltip>
                )
            }
            {
                (role === "admin" || role === "colaborador" || role === "profissional_saude") && (

                    <Tooltip title="Atribuir Medico" placement="top-end">
                        <Fab
                            color="secondary"
                            size="small"
                            aria-label="add"
                            onClick={(e)=>{
                                e.preventDefault();
                                onOpenMedicoModal(avaliacaoJoin.avaliacao.id);
                            }}

                            sx={{
                                position: 'absolute',
                                bottom: 16,
                                right: 116


                            }}>
                            <DoctorIconComponent dimension={26} box={"30 30 512 512"}/>
                        </Fab>
                        
                    </Tooltip>
                )
            }

            {
                role === "admin"  && (
                    <Tooltip title="Deletar Avaliacao" placement="top-end">
                        <Fab
                            color="error"
                            size="small"
                            aria-label="add"
                            onClick={(e)=>{
                                e.preventDefault();
                                onDeleteAvaliacao();
                            }}
                           
                            sx={{
                                position: 'absolute',
                                bottom: 16,
                                right: 166


                            }}
                            >
                                <DeleteForever/>
                            </Fab>
                    </Tooltip>
                    
                )
            }
        <DeleteModal
            open={openDeleteModal}
            onClose={() => setOpenDeleteModal(false)}
            onConfirm={() =>handleDeleteBateria()}
            itemName="esta bateria de testes"
           />
           <PagamentoModal
                open={isPagamentoModalOpen}
                onClose={handleClosePagamentoModal}
                avaliacao={avaliacao}
           />
            
        </Card>
    );
}
