import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Divider,
  Button,
  Modal,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Checkbox,
  ListItemText,
  Switch,
  FormControlLabel
} from "@mui/material";
import { Pergunta } from "../../types/questionario";

export interface SessaoData {
  titulo: string;
  descricao?: string;
  // Permite null para que o backend receba campos nulos quando desabilitados
  pergunta_condicional?: { id: string; texto: string } | null;
  respostas_condicionais?: { id: string; texto: string }[] | null;
}

interface SessaoModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (sessao: SessaoData) => void;
  initialData?: SessaoData;
  questionarioId: string;
  currentSessaoId?: string;
}

const SessaoModal: React.FC<SessaoModalProps> = ({
  open,
  onClose,
  onSave,
  initialData,
  questionarioId,
  currentSessaoId
}) => {
  const [titulo, setTitulo] = useState(initialData?.titulo || "");
  const [descricao, setDescricao] = useState(initialData?.descricao || "");
  const [allPerguntas, setAllPerguntas] = useState<Pergunta[]>([]);
  const [condPerguntaId, setCondPerguntaId] = useState(initialData?.pergunta_condicional?.id || "");
  const [condRespostasIds, setCondRespostasIds] = useState<string[]>(initialData?.respostas_condicionais?.map(r => r.id) || []);
  // Se já existir valor condicional, o switch inicia marcado
  const [showConditional, setShowConditional] = useState(!!initialData?.pergunta_condicional);

  // Busca as perguntas condicionais se o switch estiver ativo.
  useEffect(() => {
    if (!open) return;
    if (!showConditional) return;
    const effectiveQId = questionarioId || (initialData && (initialData as any).questionario_id);
    if (!effectiveQId) {
      console.error("questionarioId não foi definido.");
      return;
    }
    fetch(`${import.meta.env.VITE_BACKEND_URL}/questionario/detailed/${effectiveQId}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("@App:token")}` }
    })
      .then(res => res.json())
      .then((data) => {
        if (!data.sessoes || !Array.isArray(data.sessoes)) {
          console.error("Propriedade 'sessoes' não encontrada na resposta:", data);
          return;
        }
        const perguntas: Pergunta[] = [];
        data.sessoes.forEach((sessao: any) => {
          if (sessao.id !== currentSessaoId && sessao.perguntas && Array.isArray(sessao.perguntas)) {
            perguntas.push(...sessao.perguntas);
          }
        });
        setAllPerguntas(perguntas);
      })
      .catch(console.error);
  }, [open, questionarioId, currentSessaoId, initialData, showConditional]);

  // Reseta os estados quando initialData muda
  useEffect(() => {
    setTitulo(initialData?.titulo || "");
    setDescricao(initialData?.descricao || "");
    setCondPerguntaId(initialData?.pergunta_condicional?.id || "");
    setCondRespostasIds(initialData?.respostas_condicionais?.map(r => r.id) || []);
    setShowConditional(!!initialData?.pergunta_condicional); // Garante que o estado seja booleano
  }, [initialData]);

  const handleSave = () => {
    if (!titulo.trim()) return;

    // Define o payload com campos nulos quando não houver condição
    let payload: SessaoData = {
      titulo,
      descricao,
      pergunta_condicional: null,
      respostas_condicionais: null
    };

    if (showConditional && condPerguntaId) {
      const perguntaCond = allPerguntas.find(p => p.id === condPerguntaId);
      if (perguntaCond) {
        payload.pergunta_condicional = { id: perguntaCond.id, texto: perguntaCond.texto };
        payload.respostas_condicionais = condRespostasIds.length > 0
          ? perguntaCond.alternativas
              .filter(a => condRespostasIds.includes(a.id!))
              .map(a => ({ id: a.id!, texto: a.texto }))
          : null;
      }
    }

    onSave(payload);
    onClose();
  };

  // As alternativas exibidas são as da pergunta selecionada
  const alternativas = allPerguntas.find(p => p.id === condPerguntaId)?.alternativas || [];

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{
        backgroundColor: "white",
        width: { xs: "90%", sm: "60%", md: "40%" },
        margin: "auto",
        marginTop: "10%",
        padding: 3,
        borderRadius: 2,
      }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          {initialData ? "Editar Sessão" : "Nova Sessão"}
        </Typography>
        <TextField
          label="Título"
          fullWidth
          value={titulo}
          onChange={e => setTitulo(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Descrição"
          fullWidth
          multiline
          rows={3}
          value={descricao}
          onChange={e => setDescricao(e.target.value)}
          margin="normal"
        />
        <Divider sx={{ my: 2 }} />
        <FormControlLabel
          control={
            <Switch
              checked={showConditional}
              onChange={(e) => {
                setShowConditional(e.target.checked);
                if (!e.target.checked) {
                  // Limpa os valores caso desabilite
                  setCondPerguntaId("");
                  setCondRespostasIds([]);
                }
              }}
              color="primary"
            />
          }
          label="Habilitar condições (Pergunta e Respostas Condicionais)"
        />
        {showConditional && (
          <>
            <Divider sx={{ my: 2 }} />
            <FormControl fullWidth margin="normal">
              <InputLabel id="cond-pergunta-label">Pergunta Condicional</InputLabel>
              <Select
                labelId="cond-pergunta-label"
                value={condPerguntaId}
                label="Pergunta Condicional"
                onChange={(e: SelectChangeEvent) => {
                  setCondPerguntaId(e.target.value);
                  setCondRespostasIds([]); // limpa valores anteriores
                }}
              >
                <MenuItem value=""><em>Nenhuma</em></MenuItem>
                {allPerguntas.map(p => (
                  <MenuItem key={p.id} value={p.id}>
                    {p.texto}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal" disabled={!condPerguntaId}>
              <InputLabel id="cond-respostas-label">Respostas Condicionais</InputLabel>
              <Select
                labelId="cond-respostas-label"
                multiple
                value={condRespostasIds}
                onChange={(e: SelectChangeEvent<string[]>) =>
                  setCondRespostasIds(e.target.value as string[])
                }
                renderValue={(selected) =>
                  alternativas
                    .filter(a => selected.includes(a.id!))
                    .map(a => a.texto)
                    .join(", ")
                }
                label="Respostas Condicionais"
              >
                {alternativas.map(a => (
                  <MenuItem key={a.id} value={a.id!}>
                    <Checkbox checked={condRespostasIds.includes(a.id!)} />
                    <ListItemText primary={a.texto} />
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </>
        )}
        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 2 }}>
          <Button variant="outlined" onClick={onClose}>Cancelar</Button>
          <Button variant="contained" onClick={handleSave}>Salvar</Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default SessaoModal;