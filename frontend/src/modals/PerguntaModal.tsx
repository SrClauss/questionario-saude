import React, { useState } from "react";
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Switch,
    FormControlLabel
} from "@mui/material";

interface PerguntaData {
    texto: string;
    tipo_resposta: string;
    is_obrigatoria: boolean;
}

interface PerguntaModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (pergunta: PerguntaData) => void;
}

const PerguntaModal: React.FC<PerguntaModalProps> = ({ open, onClose, onSave }) => {
    const [texto, setTexto] = useState("");
    const [tipoResposta, setTipoResposta] = useState("multipla_escolha");
    const [isObrigatoria, setIsObrigatoria] = useState(true);

    const handleSave = () => {
        if (!texto.trim()) return;
        onSave({
            texto,
            tipo_resposta: tipoResposta,
            is_obrigatoria: isObrigatoria
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
                    Inserir Perguntas
                </Typography>

                <TextField
                    label="Texto da Pergunta"
                    fullWidth
                    value={texto}
                    onChange={(e) => setTexto(e.target.value)}
                    margin="normal"
                />

                <FormControl fullWidth margin="normal">
                    <InputLabel id="tipo-resposta-label">Tipo de Resposta</InputLabel>
                    <Select
                        labelId="tipo-resposta-label"
                        id="tipo-resposta"
                        value={tipoResposta}
                        label="Tipo de Resposta"
                        onChange={(e) => setTipoResposta(e.target.value as string)}
                    >
                        <MenuItem value={"texto"}>Texto</MenuItem>
                        <MenuItem value={"numero"}>Número</MenuItem>
                        <MenuItem value={"escolha_unica"}>Escolha Única</MenuItem>
                        <MenuItem value={"multipla_escolha"}>Múltipla Escolha</MenuItem>
                    </Select>
                </FormControl>

                <FormControlLabel
                    control={<Switch checked={isObrigatoria} onChange={(e) => setIsObrigatoria(e.target.checked)} />}
                    label="Obrigatória"
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

export default PerguntaModal;