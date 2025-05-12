import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
  Typography,
} from '@mui/material';

interface ConfirmActionModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  confirmationText: string; // a frase que o usuário deve digitar para confirmar
  title: string; // Obrigatório
  description: string; // Obrigatório
}

const ConfirmActionModal: React.FC<ConfirmActionModalProps> = ({
  open,
  onClose,
  onConfirm,
  confirmationText,
  title,
  description,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleConfirm = () => {
    if (inputValue.trim() === confirmationText) {
      onConfirm();
      setInputValue('');
    }
  };

  const handleClose = () => {
    setInputValue('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>
          {description}
        </DialogContentText>
        
        <Typography variant="body2" sx={{ mt: 2, mb: 1 }}>
          Para confirmar esta ação, digite <strong>"{confirmationText}"</strong> abaixo:
        </Typography>
        
        <TextField
          autoFocus
          margin="dense"
          label="Confirmação"
          fullWidth
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancelar</Button>
        <Button onClick={handleConfirm} disabled={inputValue.trim() !== confirmationText} color="error">
          Confirmar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConfirmActionModal;