import React, { useState, useEffect } from "react";
import { Modal, Box, Typography, TextField, Button, Divider, List, ListItem, ListItemText, IconButton, InputAdornment, Tooltip } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

interface Fonte {
  autores: string; // Mudado para string
  titulo: string;
  ano: string;
  editora: string;
}

interface FontesLiteraturaModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (fontes: Fonte[]) => void;
}

const formatarAutoresABNT = (autores: string[]): string => {
  const autoresFormatados = autores
    .map(autor => {
      const partes = autor.trim().split(" ");
      if (partes.length === 1) {
        return autor.toUpperCase(); // Se só tem um nome, usa tudo em maiúsculo
      }
      const sobrenome = partes.pop()!.toUpperCase();
      const nome = partes.join(" ");
      return `${sobrenome}, ${nome}`;
    })
    .sort(); // Ordena alfabeticamente

  if (autoresFormatados.length > 4) {
    return `${autoresFormatados.slice(0, 4).join('; ')} et al.`;
  }

  return autoresFormatados.join('; ');
};

export default function FontesLiteraturaModal({ open, onClose, onSave }: FontesLiteraturaModalProps) {
  const [autores, setAutores] = useState<string[]>([]);
  const [autorTemp, setAutorTemp] = useState("");
  const [fonte, setFonte] = useState<Omit<Fonte, "autores">>({
    titulo: "",
    ano: "",
    editora: ""
  });
  const [fontes, setFontes] = useState<Fonte[]>([]);

  useEffect(() => {
    if (open) {
      setAutores([]);
      setAutorTemp("");
      setFonte({ titulo: "", ano: "", editora: "" });
      setFontes([]);
    }
  }, [open]);

  const handleAddAutor = () => {
    if (autorTemp.trim()) {
      setAutores([...autores, autorTemp.trim()]);
      setAutorTemp("");
    }
  };

  const handleRemoveAutor = (autorToRemove: string) => {
    setAutores(autores.filter(autor => autor !== autorToRemove));
  };

  const handleSaveFonte = () => {
    if (fonte.titulo && fonte.ano && fonte.editora && autores.length > 0) {
      const autoresFormatados = formatarAutoresABNT(autores); // Formata os autores
      setFontes([...fontes, { ...fonte, autores: autoresFormatados }]); // Salva como string
      setFonte({ titulo: "", ano: "", editora: "" });
      setAutores([]);
    }
  };

  const handleSave = () => {
    onSave(fontes);
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          backgroundColor: "white",
          width: { xs: "90vw", sm: "60%", md: "40%" }, // Largura total em telas pequenas
          height: { xs: "90vh", sm: "auto" }, // Altura total em telas pequenas
          margin: "auto",
          marginTop: { xs: "0vh", sm: "10%" }, // Ajusta a margem superior
          padding: 3,
          borderRadius: {xs: 0, sm: 2},
          overflowY: "auto",
          maxHeight: { xs: "100vh", sm: "80vh" }, // Limita a altura máxima
        }}
      >
        <Typography variant="h6" sx={{ mb: 2 }}>
          Fontes de Literatura (ABNT)
        </Typography>

        <Typography variant="subtitle1">Autores</Typography>
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <TextField
            fullWidth
            label="Nome do Autor"
            value={autorTemp}
            onChange={(e) => setAutorTemp(e.target.value)}
            slotProps={

              {
                input:{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Tooltip title="Adicionar Autor">
                        <IconButton onClick={handleAddAutor}>
                          <AddIcon />
                        </IconButton>
                      </Tooltip>
                    </InputAdornment>
                  ),

                }
              }
            }

          />
        </Box>

        <List sx={{ width: '100%', bgcolor: 'background.paper', mb: 2 }}>
          {autores.map((autor) => (
            <ListItem key={autor} secondaryAction={
              <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveAutor(autor)}>
                <DeleteIcon />
              </IconButton>
            }>
              <ListItemText primary={autor} />
            </ListItem>
          ))}
        </List>

        <TextField
          fullWidth
          label="Título"
          value={fonte.titulo}
          onChange={(e) => setFonte({ ...fonte, titulo: e.target.value })}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Ano"
          value={fonte.ano}
          onChange={(e) => setFonte({ ...fonte, ano: e.target.value })}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Editora"
          value={fonte.editora}
          onChange={(e) => setFonte({ ...fonte, editora: e.target.value })}
          margin="normal"
        />

        <Button variant="outlined" onClick={handleSaveFonte} sx={{ mt: 2 }}>
          Adicionar Fonte
        </Button>

        <Divider sx={{ my: 2 }} />

        {fontes.length > 0 && (
          <Box sx={{ maxHeight: 150, overflowY: "auto", mb: 2 }}>
            {fontes.map((fonte, index) => (
              <Box key={index} sx={{ p: 1, border: "1px solid #ccc", borderRadius: 1, mb: 1 }}>
                <Typography variant="body2">
                  {fonte.autores} . {fonte.titulo} ({fonte.ano}), {fonte.editora}
                </Typography>
              </Box>
            ))}
          </Box>
        )}

        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1 }}>
          <Button variant="outlined" onClick={onClose}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={handleSave}>
            Salvar Fontes
          </Button>
        </Box>
      </Box>
    </Modal>
  );
}