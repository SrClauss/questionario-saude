import React, { useState } from "react";
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
} from "@mui/material";

interface AlternativaData {
  texto: string;
  valor: number;
}

interface AlternativaModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (alternativa: AlternativaData) => void;
}

const AlternativaModal: React.FC<AlternativaModalProps> = ({ open, onClose, onSave }) => {
  const [texto, setTexto] = useState("");
  const [valor, setValor] = useState<number>(0);

  const handleSave = () => {
    if (!texto.trim()) return; // Texto é obrigatório
    onSave({ texto, valor });
    setTexto("");
    setValor(0);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
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
          Inserir Alternativa
        </Typography>

        <TextField
          label="Texto da Alternativa"
          fullWidth
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Valor da Alternativa"
          fullWidth
          type="number"
          value={valor}
          onChange={(e) => setValor(Number(e.target.value))}
          margin="normal"
        />

        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 2 }}>
          <Button variant="outlined" onClick={onClose}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={handleSave}>
            Salvar
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default AlternativaModal;