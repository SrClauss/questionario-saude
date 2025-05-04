import React, { useState, useEffect } from "react";
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
  metodo_pontuacao: string; // Adicionado o campo metodo_pontuacao
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
  const [metodoPontuacao, setMetodoPontuacao] = useState(initialData?.metodo_pontuacao || "soma_item"); // Novo estado
  const [errors, setErrors] = useState<{ texto?: string, tipo_resposta?: string, metodo_pontuacao?: string }>({});
  const [showValidationAlert, setShowValidationAlert] = useState(false);

  useEffect(() => {
    if (initialData) {
      setTexto(initialData.texto || "");
      setTipoResposta(initialData.tipo_resposta || "texto");
      setMetodoPontuacao(initialData.metodo_pontuacao || "soma_item"); // Inicializa com o valor existente ou padrão
      setErrors({});
      setShowValidationAlert(false);
    } else {
      setTexto("");
      setTipoResposta("texto");
      setMetodoPontuacao("soma_item"); // Valor padrão para nova pergunta
      setErrors({});
      setShowValidationAlert(false);
    }
  }, [initialData, open]);

  const validateForm = (): boolean => {
    const newErrors: { texto?: string, tipo_resposta?: string, metodo_pontuacao?: string } = {};
    let isValid = true;

    // Validação existente...
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

    if (!tipoResposta) {
      newErrors.tipo_resposta = "O tipo de resposta é obrigatório";
      isValid = false;
    }

    // Nova validação para metodo_pontuacao
    if (!metodoPontuacao) {
      newErrors.metodo_pontuacao = "O método de pontuação é obrigatório";
      isValid = false;
    }

    setErrors(newErrors);
    setShowValidationAlert(!isValid);
    return isValid;
  };

  const handleSave = () => {
    if (validateForm()) {
      onSave({ texto, tipo_resposta: tipoResposta, metodo_pontuacao: metodoPontuacao });
      setTexto("");
      setTipoResposta("texto");
      setMetodoPontuacao("soma_item");
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
          maxHeight: "90vh",
          overflowY: "auto",
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

        {/* Novo campo para método de pontuação */}
        <FormControl fullWidth margin="normal" error={!!errors.metodo_pontuacao} required>
          <InputLabel id="metodo-pontuacao-label">Método de Pontuação</InputLabel>
          <Select
            labelId="metodo-pontuacao-label"
            id="metodo-pontuacao"
            value={metodoPontuacao}
            label="Método de Pontuação"
            onChange={(e) => {
              setMetodoPontuacao(e.target.value);
              if (errors.metodo_pontuacao) {
                setErrors({...errors, metodo_pontuacao: undefined});
              }
            }}
          >
            <MenuItem value="soma_item">Soma dos Itens</MenuItem>
            <MenuItem value="qualitativo">Qualitativo</MenuItem>
            <MenuItem value="moda">Moda</MenuItem>
            <MenuItem value="media">Média</MenuItem>
            <MenuItem value="formula_anterior">Fórmula Anterior</MenuItem>
          </Select>
          {errors.metodo_pontuacao && <FormHelperText>{errors.metodo_pontuacao}</FormHelperText>}
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