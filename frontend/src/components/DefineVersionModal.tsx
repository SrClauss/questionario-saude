import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
} from '@mui/material';

interface DefineVersionModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (version: string) => void;
  title: string;
  description: string;
}

const DefineVersionModal: React.FC<DefineVersionModalProps> = ({ open, onClose, onConfirm, title, description }) => {
  const [version, setVersion] = useState('');

  const handleConfirm = () => {
    if (version.trim()) {
      onConfirm(version.trim());
      setVersion('');
    }
  };

  const handleClose = () => {
    setVersion('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{description}</DialogContentText>
        <TextField
          autoFocus
          margin="dense"
          label="Nova Versão"
          fullWidth
          value={version}
          onChange={(e) => setVersion(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancelar</Button>
        <Button onClick={handleConfirm} disabled={!version.trim()} color="primary">
          Confirmar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DefineVersionModal;