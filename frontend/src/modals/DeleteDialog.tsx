import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button } from '@mui/material';

interface DeleteModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    itemName?: string; // Nome do item a ser deletado (opcional)
}

const DeleteModal: React.FC<DeleteModalProps> = ({ open, onClose, onConfirm, itemName }) => {
    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="delete-dialog-title"
            aria-describedby="delete-dialog-description"
        >
            <DialogTitle id="delete-dialog-title">Confirmar Deleção</DialogTitle>
            <DialogContent>
                <DialogContentText id="delete-dialog-description">
                    {`Tem certeza que deseja deletar ${itemName ? `"${itemName}"` : 'este item'}? Esta ação não pode ser desfeita.`}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Não
                </Button>
                <Button onClick={onConfirm} color="error" autoFocus>
                    Sim
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default DeleteModal;