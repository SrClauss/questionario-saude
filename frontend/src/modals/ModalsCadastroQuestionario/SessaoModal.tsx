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
  ListItemText
} from "@mui/material";
import { Pergunta, PerguntaCondicional, RespostaCondicional } from "../../types/questionario";

interface SessaoData {
  titulo: string;
  descricao?: string;
  pergunta_condicional?: PerguntaCondicional;
  respostas_condicionais?: RespostaCondicional[];
}

interface SessaoModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (sessao: SessaoData) => void;
  initialData?: SessaoData;
}

const SessaoModal: React.FC<SessaoModalProps> = ({ open, onClose, onSave, initialData }) => {
  const [titulo, setTitulo] = useState(initialData?.titulo || "");
  const [descricao, setDescricao] = useState(initialData?.descricao || "");
  const [allPerguntas, setAllPerguntas] = useState<Pergunta[]>([]);
  const [condPerguntaId, setCondPerguntaId] = useState(initialData?.pergunta_condicional?.id || "");
  const [condRespostasIds, setCondRespostasIds] = useState<string[]>(initialData?.respostas_condicionais?.map(r => r.id) || []);

  // Carrega perguntas detalhadas ao abrir modal
  useEffect(() => {
    if (!open) return;
    fetch(`${import.meta.env.VITE_BACKEND_URL}/perguntas/detailed`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("@App:token")}` }
    })
      .then(res => res.json())
      .then((data: Pergunta[]) => setAllPerguntas(data))
      .catch(console.error);
  }, [open]);

  // Reset quando initialData muda
  useEffect(() => {
    setTitulo(initialData?.titulo || "");
    setDescricao(initialData?.descricao || "");
    setCondPerguntaId(initialData?.pergunta_condicional?.id || "");
    setCondRespostasIds(initialData?.respostas_condicionais?.map(r => r.id) || []);
  }, [initialData]);

  const handleSave = () => {
    if (!titulo.trim()) return;
    // monta objetos condicionais
    const perguntaCond = allPerguntas.find(p => p.id === condPerguntaId);
    const pergunta_condicional = perguntaCond
      ? { id: perguntaCond.id, texto: perguntaCond.texto }
      : undefined;
    const respostas_condicionais = perguntaCond
      ? perguntaCond.alternativas
          .filter(a => condRespostasIds.includes(a.id!))
          .map(a => ({ id: a.id!, texto: a.texto }))
      : undefined;
    onSave({ titulo, descricao, pergunta_condicional, respostas_condicionais });
    onClose();
  };

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

        {/* Select Pergunta Condicional */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="cond-pergunta-label">Pergunta Condicional</InputLabel>
          <Select
            labelId="cond-pergunta-label"
            value={condPerguntaId}
            label="Pergunta Condicional"
            onChange={(e: SelectChangeEvent) => {
              setCondPerguntaId(e.target.value);
              setCondRespostasIds([]); // limpa anteriores
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

        {/* Select Respostas Condicionais */}
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

        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 2 }}>
          <Button variant="outlined" onClick={onClose}>Cancelar</Button>
          <Button variant="contained" onClick={handleSave}>Salvar</Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default SessaoModal;