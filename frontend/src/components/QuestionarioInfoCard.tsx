import React from 'react';
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
  CardContent
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Questionario } from '../types/questionario';
import { formatarFonteABNT } from '../utils/abntFormatter';

interface QuestionarioInfoCardProps {
  questionario: Questionario;
}

const QuestionarioInfoCard: React.FC<QuestionarioInfoCardProps> = ({ questionario }) => {

  const formatText = (text: string | undefined) => {
    if (!text) return 'Sem descrição';
    return text.split('\n').map((item, i) => {
      return <React.Fragment key={i}>
        {item}
        <br />
      </React.Fragment>;
    });
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
          <Typography variant="h6">{questionario.titulo}</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Card>
          <CardContent>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              Versão: {questionario.versao || 'N/A'}
            </Typography>
            <Typography variant="body2">
              {formatText(questionario.descricao)}
            </Typography>

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
      </AccordionDetails>
    </Accordion>
  );
};

export default QuestionarioInfoCard;