import React from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
  IconButton,
  Tooltip,
  Snackbar,
  Alert,
  Divider
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EditIcon from '@mui/icons-material/Edit';
import { AddCircle, AutoAwesome, Delete, PostAdd, Warning, VisibilityOutlined as VisibilityIcon } from '@mui/icons-material';
import PerguntaInfoCard from './PerguntaInfoCard';
import PerguntaModal from '../modals/ModalsCadastroQuestionario/PerguntaModal';
import PerguntasEmLoteModal, { PerguntaData } from '../modals/ModalsCadastroQuestionario/PerguntasEmLoteModal';
import AlternativasLoteModal from '../modals/ModalsCadastroQuestionario/AlternativasLoteModal';
import { Sessao, Pergunta } from '../types/questionario';
import { useQuestionarioContext } from '../contexts/QuestionarioContext';
import CustomTooltip from '../components/CustomTooltip';

interface BatchAlternativa {
  id?: string;
  texto: string;
  valor: number;
  ordem: number;
}

interface BatchAlternativasPayload {
  tipo_resposta: string;
  alternativas: BatchAlternativa[];
}

interface SessaoInfoCardProps {
  sessao: Sessao;
  onDelete: () => void;
  onEdit: (sessao: Sessao) => void;
  onUpdate: () => void; // callback para atualizar o questionário detalhado (pelo componente pai)
}

const SessaoInfoCard: React.FC<SessaoInfoCardProps> = ({ sessao, onDelete, onEdit, onUpdate }) => {
  const [isPerguntaModalOpen, setIsPerguntaModalOpen] = React.useState(false);
  const [selectedPergunta, setSelectedPergunta] = React.useState<Pergunta | null>(null);
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
  const [snackbarMessage, setSnackbarMessage] = React.useState('');
  const [openBatchModal, setOpenBatchModal] = React.useState(false);
  const [openAlternativasModal, setOpenAlternativasModal] = React.useState(false);

  const { hasBaterias } = useQuestionarioContext();

  // Abre o modal para editar a pergunta
  const handleOpenPerguntaModal = (e: React.MouseEvent<HTMLButtonElement>, pergunta: Pergunta) => {
    e.stopPropagation();
    e.preventDefault();
    setSelectedPergunta(pergunta);
    setIsPerguntaModalOpen(true);
  };

  // Abre o modal para criar uma nova pergunta
  const handleOpenNewPerguntaModal = (e: React.MouseEvent<HTMLButtonElement>): void => {
    e.stopPropagation();
    e.preventDefault();
    setSelectedPergunta(null);
    setIsPerguntaModalOpen(true);
  };

  const handleSavePergunta = async (perguntaAtualizada: { 
    texto: string; 
    tipo_resposta: string; 
    metodo_pontuacao: string;
    ordem?: number; // Adicionando ordem aqui para tipagem correta
    alternativas?: { texto: string; valor: number; ordem: number }[];
  }) => {
    const token = localStorage.getItem('@App:token');
    let questionResponse;
    try {
      if (selectedPergunta?.id) {
        // Atualiza pergunta existente, enviando alternativas no mesmo payload
        questionResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/${selectedPergunta.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ // Inclui alternativas diretamente
            ...perguntaAtualizada,
            sessao_id: sessao.id, // Garante que sessao_id seja enviado
            ordem: perguntaAtualizada.ordem ?? selectedPergunta.ordem, // Adiciona ordem
          }),
        });
      } else {
        // Cria nova pergunta, enviando alternativas no mesmo payload
        questionResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ // Inclui alternativas diretamente
            ...perguntaAtualizada,
            sessao_id: sessao.id, // Garante que sessao_id seja enviado
            ordem: perguntaAtualizada.ordem ?? (sessao.perguntas?.length ?? 0) + 1, // Adiciona ordem
          }),
        });
      }
      
      if (questionResponse.ok) {
       
        let message = selectedPergunta ? "Pergunta atualizada" : "Pergunta criada";
        if (perguntaAtualizada.alternativas && perguntaAtualizada.alternativas.length > 0) {
          message += " com suas alternativas";
        } else {
          message += " com sucesso";
        }
        setSnackbarMessage(message);
        setOpenSnackbar(true);
      } else {
        const data = await questionResponse.json();
        setSnackbarMessage(`Erro ao salvar pergunta: ${data.message || "Erro desconhecido"}`);
        setOpenSnackbar(true);
      }
    } catch (error) {
      setSnackbarMessage(`Erro na requisição: ${error}`);
      setOpenSnackbar(true);
    }
    onUpdate();
    handleClosePerguntaModal();
  };

  // Fecha o modal de pergunta
  const handleClosePerguntaModal = () => {
    setIsPerguntaModalOpen(false);
    setSelectedPergunta(null);
  };

  // Exclui uma pergunta
  const handleDeletePergunta = async (e: React.MouseEvent<HTMLButtonElement>, pergunta: Pergunta) => {
    e.stopPropagation();
    e.preventDefault();
    const token = localStorage.getItem('@App:token');
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/${pergunta.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.status === 204) {
        setSnackbarMessage("Pergunta excluída com sucesso");
        setOpenSnackbar(true);
      } else {
        const data = await response.json();
        setSnackbarMessage(`Erro ao excluir pergunta: ${data.message || "Erro desconhecido"}`);
        setOpenSnackbar(true);
      }
    } catch (error) {
      setSnackbarMessage(`Erro na requisição de exclusão: ${error}`);
      setOpenSnackbar(true);
    }
    onUpdate();
  };

  // Modal para perguntas em lote - agora com implementação de criação em batch
  const handleOpenBatchModal = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    e.preventDefault();
    setOpenBatchModal(true);
  };

  // Fecha o modal de perguntas em lote
  const handleCloseBatchModal = () => {
    setOpenBatchModal(false);
  };

  // Implementação da criação em batch de perguntas com retorno de erros/sucessos em Snackbar
  const handleSaveBatchPerguntas = async (perguntas: PerguntaData[]) => {
    const token = localStorage.getItem('@App:token');
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/${sessao.id}/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ perguntas }),
      });
      
      if (response.ok) {
        const data = await response.json();
        const perguntasCriadas = data.length || 0;
        setSnackbarMessage(`${perguntasCriadas} perguntas criadas com sucesso`);
        setOpenSnackbar(true);
        onUpdate();
      } else {
        const errorData = await response.json();
        setSnackbarMessage(`Erro no backend: ${errorData.error || errorData.message || "Erro desconhecido"}`);
        setOpenSnackbar(true);
      }
    } catch (error) {
      setSnackbarMessage(`Falha na conexão: ${error}`);
      setOpenSnackbar(true);
    }
    setOpenBatchModal(false);
  };

  // Funcionalidade para salvar alternativas em lote
  const handleSaveBatchAlternativas = async (payload: BatchAlternativasPayload) => {
    const token = localStorage.getItem('@App:token');
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/sessoes/${sessao.id}/alternativas-lote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        const data = await response.json();
        setSnackbarMessage(data.message || "Alternativas atualizadas com sucesso.");
        setOpenSnackbar(true);
        onUpdate();
      } else {
        const errorData = await response.json();
        setSnackbarMessage(`Erro: ${errorData.error || errorData.message || "Erro desconhecido"}`);
        setOpenSnackbar(true);
      }
    } catch (error: any) {
      setSnackbarMessage(`Falha na conexão: ${error}`);
      setOpenSnackbar(true);
    }
    setOpenAlternativasModal(false);
  };

  const handleCloseSnackbar = (_e?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') return;
    setOpenSnackbar(false);
  };

  return (
    <>
      <Accordion onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}>
        <AccordionSummary
          component="div"
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
            <Box sx={{ width: { xs: "100%", md: "70%" }}}>
            <Typography variant="h6">{sessao.titulo}</Typography>
            </Box>
            { !hasBaterias ? (
              <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row"} }}>
                <Tooltip title="Alterar Alternativas em Lote">
                  <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); setOpenAlternativasModal(true); }}>
                    <AutoAwesome color="info" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Inserir Perguntas em Lote">
                  <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); handleOpenBatchModal(e); }}>
                    <PostAdd color="info" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Editar Sessão">
                  <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); onEdit(sessao); }}>
                    <EditIcon color="primary" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Deletar Sessão">
                  <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); onDelete(); }}>
                    <Delete color="error" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Adicionar Pergunta">
                  <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); handleOpenNewPerguntaModal(e); }}>
                    <AddCircle color="info" />
                  </IconButton>
                </Tooltip>
              </Box>
            ) : (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <CustomTooltip
                  arrow
                  title="Não é possível editar as sessões deste questionário, pois ele possui baterias de testes vinculadas, duplique o teste ou apague todos as baterias vinculadas a este teste (Não Recomendado)."
                >
                  <IconButton>
                    <Warning htmlColor="black" />
                  </IconButton>
                </CustomTooltip>
              </Box>
            )}
          </Box>
    
        </AccordionSummary>
        <AccordionDetails onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}>
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'start' }}>
              <Typography variant="body1" sx={{ mr: 1, fontWeight: 'bold' }}>Descrição:</Typography>
              <Typography variant="body1">{sessao.descricao || 'Sem descrição'}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'start' }}>
              <Typography variant="body1" sx={{ mr: 1, fontWeight: 'bold' }}>Ordem:</Typography>
              <Typography variant="body1">{sessao.ordem}</Typography>
            </Box>

                  {/* Indicador de Regras de Visibilidade Ativas */}
          {sessao.regras_visibilidade && sessao.regras_visibilidade.length > 0 && (
            <Box 
              sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'flex-start', // Alinha à esquerda abaixo do título
                width: '100%', 
                mt: 1, 
                p: 0.5,
                backgroundColor: 'action.hover', // Um fundo sutil
                borderRadius: 1,
              }}>
              <VisibilityIcon color="action" sx={{ mr: 0.5, fontSize: '1rem' }} />
              <Typography variant="caption" color="text.secondary">
                Esta sessão possui regras de visibilidade. Clique em <EditIcon sx={{ fontSize: '0.9rem', verticalAlign: 'middle', mx: 0.25 }} /> para ver/editar.
              </Typography>
            </Box>
          )}
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <Divider sx={{ flexGrow: 1, mr: 2 }} />
            <Typography variant="h6" sx={{ my: 2 }}>Perguntas</Typography>
            <Divider sx={{ flexGrow: 1, ml: 2 }} />
          </Box>
          {sessao.perguntas?.map((pergunta) => (
            <PerguntaInfoCard
              key={pergunta.id}
              pergunta={pergunta}
              onEdit={handleOpenPerguntaModal}
              onDelete={handleDeletePergunta}
            />
          ))}
          <PerguntaModal
            open={isPerguntaModalOpen}
            onClose={handleClosePerguntaModal}
            onSave={(e)=>{handleSavePergunta(e)}}
            initialData={selectedPergunta || undefined}
          />
          <PerguntasEmLoteModal
            open={openBatchModal}
            onClose={handleCloseBatchModal}
            onSave={handleSaveBatchPerguntas}
            sessaoId={sessao.id}
          />
          <AlternativasLoteModal
            open={openAlternativasModal}
            onClose={() => {setOpenAlternativasModal(false); }}
            onSave={(e) => {
              handleSaveBatchAlternativas(e);
              setOpenAlternativasModal(false);
            }}
            sessaoId={sessao.id}
          />
        </AccordionDetails>
      </Accordion>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="success">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
};

export default SessaoInfoCard;