import React, { useState } from 'react';
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Paper,
  Alert,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { FonteBibliografica } from '../../types/questionario';
import { formatarFonteABNT } from '../../utils/abntFormatter';

interface FontesLiteraturaModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (fontes: FonteBibliografica[]) => void;
  initialFontes?: FonteBibliografica[];
}

const FontesLiteraturaModal: React.FC<FontesLiteraturaModalProps> = ({ open, onClose, onSave, initialFontes }) => {
  const [fontes, setFontes] = useState<FonteBibliografica[]>(initialFontes || []);
  const [novaFonte, setNovaFonte] = useState<FonteBibliografica>({
    titulo: '',
    autores: '',
    ano: '',
    editora: '',
    local: ''
  });
  const [errors, setErrors] = useState<{
    titulo?: string;
    autores?: string;
    ano?: string;
  }>({});
  const [showValidationAlert, setShowValidationAlert] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setNovaFonte(prev => ({ ...prev, [name]: value }));
    
    // Limpa o erro quando o usuário começa a corrigir o campo
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
      setShowValidationAlert(false);
    }
  };

  const validateNewSource = (): boolean => {
    const newErrors: { titulo?: string; autores?: string; ano?: string } = {};
    let isValid = true;

    // Validação do título
    if (!novaFonte.titulo.trim()) {
      newErrors.titulo = "O título é obrigatório";
      isValid = false;
    } else if (novaFonte.titulo.trim().length < 3) {
      newErrors.titulo = "O título deve ter pelo menos 3 caracteres";
      isValid = false;
    }

    // Validação dos autores
    if (!novaFonte.autores.trim()) {
      newErrors.autores = "Os autores são obrigatórios";
      isValid = false;
    }

    // Validação do ano
    if (!novaFonte.ano.trim()) {
      newErrors.ano = "O ano é obrigatório";
      isValid = false;
    } else if (!/^\d{4}$/.test(novaFonte.ano)) {
      newErrors.ano = "O ano deve ter 4 dígitos (ex: 2023)";
      isValid = false;
    }

    setErrors(newErrors);
    setShowValidationAlert(!isValid);
    return isValid;
  };

  const handleAddFonte = () => {
    if (validateNewSource()) {
      setFontes([...fontes, novaFonte]);
      setNovaFonte({ titulo: '', autores: '', ano: '', editora: '', local: '' });
      setErrors({});
      setShowValidationAlert(false);
    }
  };

  const handleDeleteFonte = (index: number) => {
    const novasFontes = [...fontes];
    novasFontes.splice(index, 1);
    setFontes(novasFontes);
  };

  const handleSave = () => {
    onSave(fontes);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Paper sx={{ width: '80%', maxWidth: 600, p: 3, maxHeight: '90vh', overflow: 'auto' }}>
        <Typography variant="h6" mb={2}>Referências Bibliográficas</Typography>

        {showValidationAlert && (
          <Alert severity="error" sx={{ mb: 2 }}>
            Por favor, preencha corretamente todos os campos obrigatórios.
          </Alert>
        )}

        <TextField
          label="Título"
          name="titulo"
          value={novaFonte.titulo}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          error={!!errors.titulo}
          helperText={errors.titulo}
          required
        />
        <TextField
          label="Autores (separados por vírgula)"
          name="autores"
          value={novaFonte.autores}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          error={!!errors.autores}
          helperText={errors.autores}
          required
        />
        <TextField
          label="Ano"
          name="ano"
          value={novaFonte.ano}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          error={!!errors.ano}
          helperText={errors.ano}
          required
        />
        <TextField
          label="Editora"
          name="editora"
          value={novaFonte.editora}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Local"
          name="local"
          value={novaFonte.local}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <Button 
          variant="contained" 
          onClick={handleAddFonte} 
          sx={{ mt: 2 }}
          disabled={!novaFonte.titulo.trim() || !novaFonte.autores.trim() || !novaFonte.ano.trim()}
        >
          Adicionar Fonte
        </Button>

        {fontes.length > 0 ? (
          <List sx={{ mt: 2, bgcolor: '#f5f5f5', borderRadius: 1, p: 1 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
              Fontes adicionadas ({fontes.length}):
            </Typography>
            {fontes.map((fonte, index) => (
              <ListItem
                key={index}
                secondaryAction={
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteFonte(index)}>
                    <DeleteIcon color="error" />
                  </IconButton>
                }
                sx={{ bgcolor: 'white', mb: 1, borderRadius: 1 }}
              >
                <ListItemText primary={formatarFonteABNT(fonte)} />
              </ListItem>
            ))}
          </List>
        ) : (
          <Box sx={{ mt: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1, textAlign: 'center' }}>
            <Typography color="text.secondary">
              Nenhuma fonte bibliográfica adicionada ainda.
            </Typography>
          </Box>
        )}

        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #e0e0e0', pt: 2 }}>
          <Button variant="outlined" onClick={onClose}>Cancelar</Button>
          <Button 
            variant="contained" 
            onClick={handleSave} 
            disabled={fontes.length === 0}
            color="primary"
          >
            Salvar Referências
          </Button>
        </Box>
      </Paper>
    </Modal>
  );
};

export default FontesLiteraturaModal;