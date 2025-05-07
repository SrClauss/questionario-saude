import React, { useState, useEffect } from 'react';
import { Modal, Box, Typography, Button, TextField, MenuItem } from '@mui/material';
import RenderAlternativas from '../../components/AlternativaForm';
import { Alternativa } from '../../types/questionario';

export interface AlternativasLotePayload {
  tipo_resposta: string;
  alternativas: { texto: string; valor: number; ordem: number }[];
}

interface AlternativasLoteModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (payload: AlternativasLotePayload) => void;
  sessaoId: string;
}

const AlternativasLoteModal: React.FC<AlternativasLoteModalProps> = ({ open, onClose, onSave, sessaoId }) => {
  // Estado para controlar as alternativas – inicialmente vazio
  const [alternativas, setAlternativas] = useState<Alternativa[]>([]);
  const [tipoResposta, setTipoResposta] = useState("personalizado");
  // Quando o modal abrir, inicia com lista vazia
  useEffect(() => {
    if (open) {
      setAlternativas([]);
    }
  }, [open]);

  const handleSubmit = () => {
    // Formata o payload removendo quaisquer campos além de texto, valor e ordem
    const payload: AlternativasLotePayload = {
      tipo_resposta: tipoResposta,
      alternativas: alternativas.map(alt => ({
        texto: alt.texto,
        valor: alt.valor,
        ordem: alt.ordem,
      }))
    };
    onSave(payload);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{
        backgroundColor: 'white',
        width: { xs: '90%', sm: '60%', md: '40%' },
        margin: 'auto',
        marginTop: '10%',
        padding: 3,
        borderRadius: 2,
        maxHeight: '90vh',
        overflowY: 'auto',
      }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Alterar Alternativas em Lote
        </Typography>
        <TextField
            label="Tipo de Resposta"
            fullWidth
            select

            value={tipoResposta}
            onChange={(e) => {
                setTipoResposta(e.target.value);
            }}
            margin="normal"
            >
                <MenuItem value="personalizado">Personalizado</MenuItem>
                <MenuItem value="texto">Texto</MenuItem>
                <MenuItem value="booleano">Booleano</MenuItem>
                <MenuItem value="numero">Número</MenuItem>
                <MenuItem value="escala_likert">Escala Likert 5</MenuItem>
                <MenuItem value="escala_likert_7">Escala Likert 7</MenuItem>
            </TextField>

        <RenderAlternativas 
          tipo_resposta={tipoResposta} 
          pergunta_id="" 
          alternativas={alternativas}
          onSetAlternativas={setAlternativas}
        />
        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 2, mt: 2 }}>
          <Button variant="outlined" onClick={onClose}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit}>Salvar</Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default AlternativasLoteModal;