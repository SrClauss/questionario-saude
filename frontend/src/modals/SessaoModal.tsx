import React, { useState } from "react";
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    Divider
} from "@mui/material";

interface SessaoData {
  titulo: string;
  descricao?: string;
}

interface SessaoModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (sessao: SessaoData) => void;
}

const SessaoModal: React.FC<SessaoModalProps> = ({ open, onClose, onSave }) => {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");

  const handleSave = () => {
    if (!titulo.trim()) return; // Título é obrigatório
    onSave({ titulo, descricao });
    setTitulo("");
    setDescricao("");
  };

  const handleChangeDescricao = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    console.log("Valor do evento:", e.target.value);
    console.log("Quantidade de Quebras  de Linha:", e.target.value.split("\n").length);
    setDescricao(e.target.value);
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
          Inserir Sessão
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
    </Modal>
  );
};

export default SessaoModal;