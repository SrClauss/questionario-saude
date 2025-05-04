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
  Divider,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EditIcon from '@mui/icons-material/Edit';
import { AddCircle, AutoAwesome, Delete } from '@mui/icons-material';
import PerguntaInfoCard from './PerguntaInfoCard';
import PerguntaModal from '../modals/ModalsCadastroQuestionario/PerguntaModal';
import PerguntasEmLoteModal, { PerguntaData } from '../modals/ModalsCadastroQuestionario/PerguntasEmLoteModal';
import { Sessao, Pergunta } from '../types/questionario';

interface SessaoInfoCardProps {
  sessao: Sessao;
  onDelete: () => void;
  onEdit: (sessao: Sessao) => void;
  onUpdate: () => void; // callback para atualizar o questionário detalhado (pelo componente pai)
}

const SessaoInfoCard: React.FC<SessaoInfoCardProps> = ({ sessao,  onDelete, onEdit, onUpdate }) => {
  const [isPerguntaModalOpen, setIsPerguntaModalOpen] = React.useState(false);
  const [selectedPergunta, setSelectedPergunta] = React.useState<Pergunta | null>(null);
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
  const [snackbarMessage, setSnackbarMessage] = React.useState('');
  const [openBatchModal, setOpenBatchModal] = React.useState(false);

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

  // Salva a pergunta (cria ou atualiza)
  const handleSavePergunta = async (perguntaAtualizada: { texto: string; tipo_resposta: string; }) => {
    const token = localStorage.getItem('@App:token');
    if (selectedPergunta?.id) {
      // Atualiza pergunta existente
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/${selectedPergunta.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            texto: perguntaAtualizada.texto,
            tipo_resposta: perguntaAtualizada.tipo_resposta,
            sessao_id: sessao.id,
          }),
        });
        if (response.ok) {
          setSnackbarMessage("Pergunta atualizada com sucesso");
          setOpenSnackbar(true);
        } else {
          const data = await response.json();
          setSnackbarMessage(`Erro ao atualizar pergunta: ${data.message || "Erro desconhecido"}`);
          setOpenSnackbar(true);
        }
      } catch (error) {
        setSnackbarMessage(`Erro na requisição de atualização: ${error}`);
        setOpenSnackbar(true);
      }
    } else {
      // Cria nova pergunta
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            texto: perguntaAtualizada.texto,
            tipo_resposta: perguntaAtualizada.tipo_resposta,
            sessao_id: sessao.id,
          }),
        });
        if (response.ok) {
          setSnackbarMessage("Pergunta criada com sucesso");
          setOpenSnackbar(true);
        } else {
          const data = await response.json();
          setSnackbarMessage(`Erro ao criar pergunta: ${data.message || "Erro desconhecido"}`);
          setOpenSnackbar(true);
        }
      } catch (error) {
        setSnackbarMessage(`Erro na requisição de criação: ${error}`);
        setOpenSnackbar(true);
      }
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

  const handleCloseSnackbar = (e?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') return;
    setOpenSnackbar(false);
  };

  return (
    <Accordion onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}>
      <AccordionSummary
        component="div"
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
        onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <Typography variant="h6">{sessao.titulo}</Typography>
          <Box>
            <Tooltip title="Inserir Perguntas em Lote">
              <IconButton onClick={(e) => { e.stopPropagation(); e.preventDefault(); handleOpenBatchModal(e); }}>
                <AutoAwesome color="primary" />
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
          
          {/* Exibe pergunta condicional apenas se existir */}
          {sessao.pergunta_condicional && (
            <Box sx={{ display: 'flex', justifyContent: 'start', mt: 1 }}>
              <Typography variant="body1" sx={{ mr: 1, fontWeight: 'bold' }}>Pergunta condicional:</Typography>
              <Typography variant="body1">
                {sessao.pergunta_condicional.texto} 
                <Typography component="span" color="text.secondary" sx={{ fontSize: '0.8rem', ml: 1 }}>
                  (ID: {sessao.pergunta_condicional.id})
                </Typography>
              </Typography>
            </Box>
          )}
          
          {/* Exibe respostas condicionais apenas se existirem */}
          {sessao.respostas_condicionais && sessao.respostas_condicionais.length > 0 && (
            <Box sx={{ display: 'flex', flexDirection: 'column', mt: 1 }}>
              <Typography variant="body1" sx={{ fontWeight: 'bold' }}>Respostas condicionais:</Typography>
              <Box sx={{ ml: 2 }}>
                {sessao.respostas_condicionais.map((resposta: {id: string, texto: string}, index: number) => (
                  <Typography key={resposta.id} variant="body1">
                    • {resposta.texto}
                    <Typography component="span" color="text.secondary" sx={{ fontSize: '0.8rem', ml: 1 }}>
                      (ID: {resposta.id})
                    </Typography>
                  </Typography>
                ))}
              </Box>
            </Box>
          )}
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <Divider sx={{ flexGrow: 1, mr: 2 }} />
          <Typography variant="h6" sx={{ my: 2 }}>Perguntas</Typography>
          <Divider sx={{ flexGrow: 1, ml: 2 }} />
        </Box>
        {sessao.perguntas.map((pergunta) => (
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
          onSave={handleSavePergunta}
          initialData={selectedPergunta || undefined}
        />
        <PerguntasEmLoteModal
          open={openBatchModal}
          onClose={handleCloseBatchModal}
          onSave={handleSaveBatchPerguntas}
          sessaoId={sessao.id}
          
        />
      </AccordionDetails>
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
    </Accordion>
  );
};

export default SessaoInfoCard;