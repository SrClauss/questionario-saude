import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Divider,
  Button,
  Modal,
  IconButton,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import { AddCircle } from '@mui/icons-material';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Pergunta } from '../../types/questionario';

interface SessaoData {
  titulo: string;
  descricao?: string;
  perguntas?: Pergunta[]; // Adicionando o tipo Pergunta
}

interface SessaoModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (sessao: SessaoData) => void;
  initialData?: SessaoData;
}

const SessaoModal: React.FC<SessaoModalProps> = ({ open, onClose, onSave, initialData }) => {
  const [titulo, setTitulo] = React.useState(initialData?.titulo || "");
  const [descricao, setDescricao] = React.useState(initialData?.descricao || "");
  
  React.useEffect(() => {
    // Atualiza o estado quando initialData muda
    if (initialData) {
      setTitulo(initialData.titulo || "");
      setDescricao(initialData.descricao || "");
     }
  }, [initialData]);

  const handleSave = () => {
    if (!titulo.trim()) return; // Título é obrigatório
    onSave({ titulo, descricao });
    setTitulo("");
    setDescricao("");
    onClose(); // Fechar o modal após salvar
  };

  const handleChangeDescricao = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    console.log("Valor do evento:", e.target.value);
    console.log("Quantidade de Quebras  de Linha:", e.target.value.split("\n").length);
    setDescricao(e.target.value);
  };



  return (
    <Modal open={open} onClose={onClose}>
      <Box>

        <Box
          sx={{
            backgroundColor: "white",
            width: { xs: "90%", sm: "60%", md: "40%" },
            margin: "auto",
            marginTop: "10%",
            padding: 3,
            borderRadius: 2,
          }}
        >
          <Typography variant="h6" sx={{ mb: 2 }}>
            Editar Sessão
          </Typography>

          <TextField
            label="Título"
            fullWidth
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            margin="normal"
          />
          <TextField
            label="Descrição"
            fullWidth
            multiline
            rows={3}
            value={descricao}
            onChange={handleChangeDescricao}
            margin="normal"
          />

          <Divider sx={{ my: 2 }} />

          <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1 }}>
            <Button variant="outlined" onClick={onClose}>
              Cancelar
            </Button>
            <Button variant="contained" onClick={handleSave}>
              Salvar
            </Button>
          </Box>

        </Box>
          
      </Box>
    </Modal>
  );
};

export default SessaoModal;