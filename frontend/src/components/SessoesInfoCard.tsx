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
import EditIcon from '@mui/icons-material/Edit';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Sessao } from '../types/questionario';
import { AddCircle, AutoAwesome, ContactsOutlined, Delete } from '@mui/icons-material';
import PerguntaInfoCard from './PerguntaInfoCard';
import PerguntaModal from '../modals/ModalsCadastroQuestionario/PerguntaModal';
import { Pergunta } from '../types/questionario';
interface SessaoInfoCardProps {
  sessao: Sessao;
  onAdd: () => void;
  onDelete: () => void;
  onEdit: (sessao: Sessao) => void;
}

const SessaoInfoCard: React.FC<SessaoInfoCardProps> = ({ sessao, onAdd, onDelete, onEdit }) => {
  const [isPerguntaModalOpen, setIsPerguntaModalOpen] = React.useState(false);
  const [selectedPergunta, setSelectedPergunta] = React.useState<Pergunta | null>(null);
  const [perguntas, setPerguntas] = React.useState<Pergunta[]>([]); // Estado para as perguntas
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
  const [snackbarMessage, setSnackbarMessage] = React.useState('');

     // Funções para controlar o modal de edição de pergunta
  const handleOpenPerguntaModal = (e:React.MouseEvent<HTMLButtonElement> , pergunta: Pergunta) => {
    e.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    setSelectedPergunta(pergunta);
    setIsPerguntaModalOpen(true);
  };
  const handleDeletePergunta = (e:React.MouseEvent<HTMLButtonElement> , pergunta: Pergunta) => {  
    e.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    
  }
  const handleOpenNewPerguntaModal = (event: React.MouseEvent<HTMLButtonElement>): void => {
    event.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    setSelectedPergunta(null); // Limpa a pergunta selecionada para adicionar uma nova
    setIsPerguntaModalOpen(true);
  };
  // Função para salvar as alterações na pergunta
  const handleSavePergunta = (perguntaAtualizada: { texto: string; tipo_resposta: string; }) => {
    if (selectedPergunta?.id){

      console.log('Selected Pergunta:', selectedPergunta.id);

      

    }
    else {
      console.log('Nova Pergunta:', perguntaAtualizada);
    }

    
   

  };


  const handleClosePerguntaModal = () => {
    setIsPerguntaModalOpen(false);
    setSelectedPergunta(null);
  };
  const handleEditClick = (event: React.MouseEvent<HTMLButtonElement>, sessao: Sessao) => {
    event.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    onEdit(sessao);
  };

  const handleDeleteClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    onDelete();
  };

  const handleAddPergunta = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation(); // Impede a propagação do evento para o AccordionSummary
    onAdd();
  };

  const handleCloseSnackbar = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpenSnackbar(false);
  };

  return (
    <Accordion>
      <AccordionSummary
        component="div"
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <Typography variant="h6">{sessao.titulo}</Typography>

          <Box>

            <Tooltip title="Adcionar Alternativas Padrões para perguntas">
              <IconButton onClick={handleAddPergunta}>
                <AutoAwesome color='primary' />
              </IconButton>
            </Tooltip>
            <Tooltip title="Editar Sessão">
              <IconButton onClick={(event) => handleEditClick(event, sessao)}>
                <EditIcon color='primary' />
              </IconButton>
            </Tooltip>
            <Tooltip title="Deletar Sessão">
              <IconButton onClick={handleDeleteClick}>
                <Delete color='error' />
              </IconButton>
            </Tooltip>
            <Tooltip title="Adicionar Pergunta">
              <IconButton onClick={handleOpenNewPerguntaModal}>
                <AddCircle color='info' />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Box>
         
            <Box sx={{display: 'flex', justifyContent: 'start'}}>
              <Typography variant='body1' sx={{marginRight: 1, fontWeight: 'bold'}} >
                Descrição: 
              </Typography>
              <Typography variant='body1' >
                {sessao.descricao || 'Sem descrição'}
              </Typography>
            </Box>

            <Box sx={{display: 'flex', justifyContent: 'start'}}>
              <Typography variant='body1' sx={{marginRight: 1, fontWeight: 'bold'}} >
                Ordem:
              </Typography>
              <Typography variant='body1' >
              {sessao.ordem}

              </Typography>
              </Box>
         </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <Divider sx={{ flexGrow: 1, marginRight: 2 }} />
          <Typography variant="h6" sx={{ marginTop: 2, marginBottom: 2 }}>
            Perguntas
          </Typography>
          <Divider sx={{ flexGrow: 1, marginLeft: 2 }} />
        </Box>
        
        


            {sessao.perguntas.map((pergunta) => (
              <PerguntaInfoCard
                key={pergunta.id}
                pergunta={pergunta}
                onEdit={handleOpenPerguntaModal}
                onDelete={handleDeletePergunta} // Passa a função de deletar pergunta
              />
            ))}
        <PerguntaModal
          open={isPerguntaModalOpen}
          onClose={handleClosePerguntaModal}
          onSave={handleSavePergunta}
          initialData={selectedPergunta || undefined}
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