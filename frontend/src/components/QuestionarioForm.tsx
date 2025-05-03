import React, { useState } from 'react';
import { TextField, Button, Box, Typography, List, ListItem, ListItemText, IconButton } from '@mui/material';
import ColumnResponsive from './ColumnResponsive';
import FontesLiteraturaModal from '../modals/ModalsCadastroQuestionario/FontesLiteraturaModal';
import { FonteBibliografica } from '../types/questionario';
import { formatarFonteABNT } from '../utils/abntFormatter';
import DeleteIcon from '@mui/icons-material/Delete';
import { Questionario } from '../types/questionario';
interface QuestionarioFormProps {
  initialData?: {
    titulo: string;
    descricao: string;
    versao: string;
    fontes_literatura: FonteBibliografica[];
  };
  onSave: (questionario: Questionario) => Promise<void>; // onSave agora é uma função assíncrona
}

const QuestionarioForm: React.FC<QuestionarioFormProps> = ({ initialData, onSave }) => {
  const [titulo, setTitulo] = useState(initialData?.titulo || '');
  const [descricao, setDescricao] = useState(initialData?.descricao || '');
  const [versao, setVersao] = useState(initialData?.versao || '');
  const [fontesLiteratura, setFontesLiteratura] = useState<FonteBibliografica[]>(initialData?.fontes_literatura || []);
  const [isFontesModalOpen, setIsFontesModalOpen] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => { // handleSubmit agora é assíncrona
    e.preventDefault();
    const data: Questionario = {
      titulo,
      descricao,
      versao,
      fontes_literatura: fontesLiteratura,
      id: '', // Provide a default or placeholder value
      is_active: true, // Default value
      created_at: new Date().toISOString(), // Default to current timestamp
      updated_at: new Date().toISOString(), // Default to current timestamp
      sessoes: [], // Default to an empty array
    };
    // Aqui você pode adicionar a lógica para enviar os dados do formulário para o backend
    console.log('Dados do formulário:', data);
    await onSave(data); // Chama a função onSave assíncrona
  };

  const handleOpenFontesModal = () => {
    setIsFontesModalOpen(true);
  };

  const handleCloseFontesModal = () => {
    setIsFontesModalOpen(false);
  };

  const handleSaveFontes = (fontes: FonteBibliografica[]) => {
    setFontesLiteratura(fontes);
    handleCloseFontesModal();
  };

  const handleDeleteFonte = (index: number) => {
    const novasFontes = [...fontesLiteratura];
    novasFontes.splice(index, 1);
    setFontesLiteratura(novasFontes);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        {initialData ? 'Editar Questionário' : 'Cadastrar Questionário'}
      </Typography>
      <TextField
        fullWidth
        label="Título"
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
        margin="normal"
        required
      />
      <TextField
        fullWidth
        label="Descrição"
        multiline
        rows={4}
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
        margin="normal"
      />
      <TextField
        fullWidth
        label="Versão"
        value={versao}
        onChange={(e) => setVersao(e.target.value)}
        margin="normal"
      />

      <Box mt={2}>
        <Typography variant="subtitle1">Referências Bibliográficas:</Typography>
        <List dense>
          {fontesLiteratura.map((fonte, index) => (
            <ListItem
              key={index}
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteFonte(index)}>
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemText primary={formatarFonteABNT(fonte)} />
            </ListItem>
          ))}
        </List>
        <Button variant="outlined" onClick={handleOpenFontesModal}>
          Adicionar/Editar Referências Bibliográficas
        </Button>
      </Box>

      <ColumnResponsive>
        <Box></Box>
        <Button variant="contained" type="submit">
          {initialData ? 'Salvar Alterações' : 'Cadastrar'}
        </Button>
      </ColumnResponsive>

      <FontesLiteraturaModal
        open={isFontesModalOpen}
        onClose={handleCloseFontesModal}
        onSave={handleSaveFontes}
        initialFontes={fontesLiteratura}
      />
    </Box>
  );
};

export default QuestionarioForm;