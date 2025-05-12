import React from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
  IconButton,
  Tooltip,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Delete, Warning } from '@mui/icons-material';
import { Pergunta } from '../types/questionario';
import { useQuestionarioContext } from '../contexts/QuestionarioContext';
import CustomTooltip from './CustomTooltip';


interface PerguntaInfoCardProps {
  pergunta: Pergunta;
  onEdit: (e: React.MouseEvent<HTMLButtonElement>, pergunta: Pergunta) => void;
  onDelete: (e: React.MouseEvent<HTMLButtonElement>, pergunta: Pergunta) => void;
}

const PerguntaInfoCard: React.FC<PerguntaInfoCardProps> = ({ pergunta, onEdit, onDelete }) => {
  const { hasBaterias } = useQuestionarioContext();

  return (
    <Accordion>
      <AccordionSummary
        component="div"
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <Typography variant="subtitle1">{pergunta.texto}</Typography>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' } }}>
            { !hasBaterias ? (
              <>
                <Tooltip title="Editar Pergunta">
                  <IconButton onClick={(e) => onEdit(e, pergunta)}>
                    <EditIcon color="primary" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Deletar Pergunta">
                  <IconButton onClick={(e) => onDelete(e, pergunta)}>
                    <Delete color="error" />
                  </IconButton>
                </Tooltip>
              </>
            ) : (
              <CustomTooltip
                arrow
                title="Não é possível editar as perguntas deste questionário, pois ele possui baterias de testes vinculadas, duplique o teste ou apague todos as baterias vinculadas a este teste (Não Recomendado)."
              >
                <IconButton>
                  <Warning htmlColor='black' />
                </IconButton>
              </CustomTooltip>
            )}
          </Box>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Typography>
          Tipo de resposta: {pergunta.tipo_resposta}
        </Typography>
      </AccordionDetails>
    </Accordion>
  );
};

export default PerguntaInfoCard;