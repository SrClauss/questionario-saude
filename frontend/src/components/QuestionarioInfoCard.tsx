import React, { useState } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  Snackbar,
  Alert,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Questionario } from '../types/questionario';
import { formatarFonteABNT } from '../utils/abntFormatter';
import { DeleteForever, Edit, FileCopy } from '@mui/icons-material';
import ConfirmActionModal from '../modals/ConfirmActionModal';
import DefineVersionModal from './DefineVersionModal';

interface QuestionarioInfoCardProps {
  questionario: Questionario;
  onEdit: () => void;
  onRefresh: () => void;

}

const QuestionarioInfoCard: React.FC<QuestionarioInfoCardProps> = ({ questionario,  onEdit, onRefresh }) => {
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [isVersionModalOpen, setIsVersionModalOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState<string | null>(null);
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error' | 'info' | 'warning'>('info');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const formatText = (text: string | undefined) => {
    if (!text) return 'Sem descrição';
    return text.split('\n').map((item, i) => (
      <React.Fragment key={i}>
        {item}
        <br />
      </React.Fragment>
    ));
  };

  const handleDuplicate = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    e.preventDefault();
    // Abre o modal para definir a nova versão
    setIsVersionModalOpen(true);
  };

  const handleConfirmDuplicate = async (novaVersao: string) => {
    try {
      const token = localStorage.getItem('@App:token');
      if (!token) {
        setSnackbarMessage("Token de autenticação não encontrado");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
        return;
      }

      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/questionario/duplicate/${questionario.id}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ versao: novaVersao }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        setSnackbarMessage(data.message || "Questionário duplicado com sucesso!");
        setSnackbarSeverity("success");
        setOpenSnackbar(true);
        // Atualize o estado ou execute um callback, se necessário.
      } else {
        const errorData = await response.json();
        setSnackbarMessage(errorData.error || "Erro ao duplicar questionário");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    } catch (error: any) {
      setSnackbarMessage(`Falha na requisição: ${error.message}`);
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    } finally {
      setIsVersionModalOpen(false);
    }
  };

  const handleDelete = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    e.preventDefault();
    // Abre o modal de confirmação para deletar baterias
    setIsConfirmOpen(true);
  };

  const handleRedefineBaterias = async () => {
    try {
      const token = localStorage.getItem("@App:token");
      if (!token) {
        setSnackbarMessage("Token de autenticação não encontrado");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
        return;
      }

      const response = await fetch(
        //Rota: /backend/questionario/<string:id>/delete-todas-baterias -> Métodos: DELETE, OPTIONS
        `${import.meta.env.VITE_BACKEND_URL}/questionario/${questionario.id}/delete-todas-baterias`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setSnackbarMessage(data.message || "Todas as baterias deletadas com sucesso!");
        setSnackbarSeverity("success");
        setOpenSnackbar(true);

      } else {
        const errorData = await response.json();
        setSnackbarMessage(errorData.error || "Erro ao deletar baterias");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    } catch (error: any) {
      setSnackbarMessage(`Falha na requisição: ${error.message}`);
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    } finally {
      setIsConfirmOpen(false);
      onRefresh();
    }
  };

  return (
    <>
      <Accordion>
        <AccordionSummary
          component="div"
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
            <Typography variant="h6">{questionario.titulo}</Typography>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' } }}>
                <Tooltip title="Editar Questionário">
                <IconButton onClick={(e) => onEdit()} color="primary">
                  <Edit color="secondary" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Duplicar Questionário">
                <IconButton onClick={(e) => handleDuplicate(e)} color="primary">
                  <FileCopy color="primary" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Deletar todos as baterias do questionário">
                <IconButton onClick={handleDelete} color="error">
                  <DeleteForever color="error" />
                </IconButton>
              </Tooltip>

        
            </Box>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Card>
            <CardContent>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                Versão: {questionario.versao || 'N/A'}
              </Typography>
              <Typography variant="body2">{formatText(questionario.descricao)}</Typography>
              {questionario.fontes_literatura && questionario.fontes_literatura.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2">Referências Bibliográficas:</Typography>
                  <List dense>
                    {questionario.fontes_literatura.map((fonte, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={formatarFonteABNT(fonte)} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </CardContent>
          </Card>
          <ConfirmActionModal
            open={isConfirmOpen}
            onClose={() => setIsConfirmOpen(false)}
            onConfirm={handleRedefineBaterias}
            title="Deletar baterias"
            description="Você tem certeza que deseja deletar todas as baterias deste questionário? Esta ação não pode ser desfeita."
            confirmationText="deletar todas as baterias"
          />
          <DefineVersionModal
            open={isVersionModalOpen}
            onClose={() => setIsVersionModalOpen(false)}
            onConfirm={handleConfirmDuplicate}
            title="Duplicar Questionário"
            description="Informe a nova versão para o questionário duplicado:"
          />
        </AccordionDetails>
      </Accordion>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={() => setOpenSnackbar(false)}
      >
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
};

export default QuestionarioInfoCard;