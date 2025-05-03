import React, { useState, useEffect, use } from "react";
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
    FormHelperText,
    Alert,
} from "@mui/material";
import { Alternativa, Pergunta } from "../../types/questionario";
import RenderAlternativas from "../../components/AlternativaForm";
interface PerguntaData {
  texto: string;
  tipo_resposta: string;
}

interface PerguntaModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (pergunta: PerguntaData) => void;
  initialData?: Pergunta;
}

const PerguntaModal: React.FC<PerguntaModalProps> = ({ open, onClose, onSave, initialData }) => {
  const [texto, setTexto] = useState(initialData?.texto || "");
  const [tipoResposta, setTipoResposta] = useState(initialData?.tipo_resposta || "texto");
  const [errors, setErrors] = useState<{ texto?: string, tipo_resposta?: string }>({});
  const [showValidationAlert, setShowValidationAlert] = useState(false);

  useEffect(() => {
    if (initialData) {
      setTexto(initialData.texto || "");
      setTipoResposta(initialData.tipo_resposta || "texto");
      // Limpa erros quando o modal é reaberto com dados iniciais
      setErrors({});
      setShowValidationAlert(false);
    } else {
      // Limpa campos quando o modal é aberto para uma nova pergunta
      setTexto("");
      setTipoResposta("texto");
      setErrors({});
      setShowValidationAlert(false);
    }
  }, [initialData, open]);

  const validateForm = (): boolean => {
    const newErrors: { texto?: string, tipo_resposta?: string } = {};
    let isValid = true;

    // Validação do texto da pergunta
    if (!texto.trim()) {
      newErrors.texto = "O texto da pergunta é obrigatório";
      isValid = false;
    } else if (texto.trim().length < 5) {
      newErrors.texto = "O texto da pergunta deve ter pelo menos 5 caracteres";
      isValid = false;
    } else if (texto.trim().length > 500) {
      newErrors.texto = "O texto da pergunta deve ter no máximo 500 caracteres";
      isValid = false;
    }

    // Validação do tipo de resposta
    if (!tipoResposta) {
      newErrors.tipo_resposta = "O tipo de resposta é obrigatório";
      isValid = false;
    }

    setErrors(newErrors);
    setShowValidationAlert(!isValid);
    return isValid;
  };

  const handleSave = () => {
    if (validateForm()) {
      onSave({ texto, tipo_resposta: tipoResposta });
      setTexto("");
      setTipoResposta("texto");
      setErrors({});
      setShowValidationAlert(false);
      onClose();
    }
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
          maxHeight: "90vh", // Define altura máxima para o modal
          overflowY: "auto", // Adiciona scroll vertical quando necessário
        }}
      >
        <Typography variant="h6" sx={{ mb: 2 }}>
          {initialData ? "Editar Pergunta" : "Nova Pergunta"}
        </Typography>

        {showValidationAlert && (
          <Alert severity="error" sx={{ mb: 2 }}>
            Por favor, corrija os erros no formulário para continuar.
          </Alert>
        )}

        <TextField
          label="Texto da Pergunta"
          fullWidth
          value={texto}
          onChange={(e) => {
            setTexto(e.target.value);
            if (errors.texto) {
              setErrors({...errors, texto: undefined});
            }
          }}
          margin="normal"
          error={!!errors.texto}
          helperText={errors.texto}
          required
        />

        <FormControl fullWidth margin="normal" error={!!errors.tipo_resposta} required>
          <InputLabel id="tipo-resposta-label">Tipo de Resposta</InputLabel>
          <Select
            labelId="tipo-resposta-label"
            id="tipo-resposta"
            value={tipoResposta}
            label="Tipo de Resposta"
            onChange={(e) => {
              setTipoResposta(e.target.value);
              if (errors.tipo_resposta) {
                setErrors({...errors, tipo_resposta: undefined});
              }
            }}
          >
            <MenuItem value="escala_likert">Escala Likert 5</MenuItem>
            <MenuItem value="escala_likert_7">Escala Likert 7</MenuItem>
            <MenuItem value="texto">Texto</MenuItem>
            <MenuItem value="booleano">Sim/Não</MenuItem>
            <MenuItem value="personalizado">Personalizado</MenuItem>
            <MenuItem value="numero">Número</MenuItem>

          </Select>
          {errors.tipo_resposta && <FormHelperText>{errors.tipo_resposta}</FormHelperText>}
        </FormControl>

        <RenderAlternativas
          tipo_resposta={tipoResposta}
          pergunta_id={initialData ? initialData.id : ""}
          onSetAlternativas={(alternativas: Alternativa[]) => {
            console.log("Alternativas:", alternativas);
          }}
          alternativas={initialData ? initialData.alternativas : []}

        />

        <Box sx={{ display: "flex", justifyContent: "space-around", gap: 1, mt: 3 }}>
          <Button variant="outlined" fullWidth onClick={onClose}>
            Cancelar
          </Button>
          <Button variant="contained" fullWidth onClick={handleSave}>
            Salvar
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};




export default PerguntaModal;