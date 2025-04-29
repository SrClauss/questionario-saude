import React, { useState, useEffect } from "react";
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    InputAdornment
} from "@mui/material";

interface BooleanaData {
    opcaoPositiva: string;
    valorPositivo: number;
    opcaoNegativa: string;
    valorNegativo: number;
}

interface BooleanaModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (data: BooleanaData) => void;
    initialData?: BooleanaData;
}

const BooleanaModal: React.FC<BooleanaModalProps> = ({ 
    open, 
    onClose, 
    onSave, 
    initialData 
}) => {
    const [opcaoPositiva, setOpcaoPositiva] = useState(initialData?.opcaoPositiva || "Sim");
    const [valorPositivo, setValorPositivo] = useState(initialData?.valorPositivo || 1);
    const [opcaoNegativa, setOpcaoNegativa] = useState(initialData?.opcaoNegativa || "Não");
    const [valorNegativo, setValorNegativo] = useState(initialData?.valorNegativo || 0);

    useEffect(() => {
        if (initialData) {
            setOpcaoPositiva(initialData.opcaoPositiva);
            setValorPositivo(initialData.valorPositivo);
            setOpcaoNegativa(initialData.opcaoNegativa);
            setValorNegativo(initialData.valorNegativo);
        } else {
            setOpcaoPositiva("Sim");
            setValorPositivo(1);
            setOpcaoNegativa("Não");
            setValorNegativo(0);
        }
    }, [initialData, open]);

    const handleSave = () => {
        if (!opcaoPositiva.trim() || !opcaoNegativa.trim()) return;
        
        onSave({
            opcaoPositiva,
            valorPositivo,
            opcaoNegativa,
            valorNegativo
        });
        
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
                    Editar Opções de Escolha Única
                </Typography>

                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Opção Positiva
                </Typography>
                <TextField
                    label="Texto"
                    fullWidth
                    value={opcaoPositiva}
                    onChange={(e) => setOpcaoPositiva(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Valor"
                    type="number"
                    fullWidth
                    value={valorPositivo}
                    onChange={(e) => setValorPositivo(Number(e.target.value))}
                    InputProps={{
                        startAdornment: <InputAdornment position="start">#</InputAdornment>,
                    }}
                    sx={{ mb: 3 }}
                />

                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Opção Negativa
                </Typography>
                <TextField
                    label="Texto"
                    fullWidth
                    value={opcaoNegativa}
                    onChange={(e) => setOpcaoNegativa(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Valor"
                    type="number"
                    fullWidth
                    value={valorNegativo}
                    onChange={(e) => setValorNegativo(Number(e.target.value))}
                    InputProps={{
                        startAdornment: <InputAdornment position="start">#</InputAdornment>,
                    }}
                    sx={{ mb: 3 }}
                />

                <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 3 }}>
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

export default BooleanaModal;