import React, { useState, useEffect } from 'react';
import { Medico, Paciente } from '../types/user';
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  Autocomplete,
  CircularProgress,
  IconButton,
  Paper,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

// Estrutura de dados que o modal envia ao submeter
export interface LaudoFormData {
  medico_id: string;
  paciente_id: string;
  cids: string[]; // Alterado para array de strings (códigos CID)
  data: string; // ISO string date
  parecer: string;
  abordagem_terapeutica: string;
}

interface CidOption {
  cid: string; // Este é o código do CID, ex: "A00.0"
  descricao: string;
}

// Campos que o usuário preenche no formulário do modal
interface LaudoFormFields {
  cids: string[]; // Alterado para array de strings (códigos CID)
  data: string; // ISO string date
  parecer: string;
  abordagem_terapeutica: string;
}

interface LaudoCadastroModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (laudoData: LaudoFormData) => void;
  medico: Medico; // Médico logado/responsável
  paciente: Paciente; // Paciente da avaliação
  initialData?: Partial<LaudoFormFields>; // Opcional, para edição dos campos do laudo
}

const LaudoCadastroModal: React.FC<LaudoCadastroModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  medico,
  paciente,
  initialData = {},
}) => {
  const [formFields, setFormFields] = useState<LaudoFormFields>({
    cids: initialData.cids || [], // Inicializa como array vazio
    data: initialData.data || new Date().toISOString().split('T')[0], // Default to today
    parecer: initialData.parecer || '',
    abordagem_terapeutica: initialData.abordagem_terapeutica || '',
  });

  const [cidInput, setCidInput] = useState('');
  const [cidOptions, setCidOptions] = useState<readonly CidOption[]>([]);
  const [selectedCids, setSelectedCids] = useState<CidOption[]>([]); // Alterado para array
  const [loadingCid, setLoadingCid] = useState(false);

  useEffect(() => {
    // Reset form fields when initialData changes or modal opens
    setFormFields({
      cids: initialData.cids || [],
      data: initialData.data || new Date().toISOString().split('T')[0],
      parecer: initialData.parecer || '',
      abordagem_terapeutica: initialData.abordagem_terapeutica || '',
    });
    // Reset CID fields as well
    if (isOpen) {
      setSelectedCids([]); // Reseta para array vazio
      setCidInput('');
      setCidOptions([]);
    }
  }, [initialData, isOpen]);


  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormFields((prev) => ({ ...prev, [name]: value }));
  };

  const fetchCidOptions = async (searchTerm: string) => {
    if (searchTerm.length < 3) { // Não buscar com menos de 3 caracteres
      setCidOptions([]);
      setLoadingCid(false);
      return;
    }
    setLoadingCid(true);
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem('@App:token');
    try {
      const response = await fetch(`${baseUrl}/laudos/get_cid_by_description/${searchTerm}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data: CidOption[] = await response.json();
        setCidOptions(data);
      } else {
        setCidOptions([]);
      }
    } catch (error) {
      console.error("Erro ao buscar CIDs:", error);
      setCidOptions([]);
    } finally {
      setLoadingCid(false);
    }
  };

  // Debounce para a busca de CID
  useEffect(() => {
    const handler = setTimeout(() => {
      if (cidInput) {
        fetchCidOptions(cidInput);
      } else {
        setCidOptions([]);
      }
    }, 500); // 500ms de debounce

    return () => {
      clearTimeout(handler);
    };
  }, [cidInput]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Basic validation example
    if (formFields.cids.length === 0 || !formFields.data || !formFields.parecer || !formFields.abordagem_terapeutica ) {
      alert('CID, Data, Parecer e Abordagem Terapêutica são obrigatórios.');
      return;
    }
    const completeLaudoData: LaudoFormData = {
      ...formFields,
      medico_id: medico.id,
      paciente_id: paciente.id,
    };
    onSubmit(completeLaudoData);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <Modal
      open={isOpen}
      onClose={onClose}
      aria-labelledby="laudo-cadastro-modal-title"
      aria-describedby="laudo-cadastro-modal-description"
    >
      <Box sx={modalStyle}>
        <Paper elevation={3} sx={{ p: { xs: 2, md: 3 } }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography id="laudo-cadastro-modal-title" variant="h6" component="h2">
              Cadastro de Laudo
            </Typography>
            <IconButton onClick={onClose} aria-label="fechar modal">
              <CloseIcon />
            </IconButton>
          </Box>

          <Box sx={{ mb: 2, p: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
            <Typography variant="subtitle2"><strong>Médico:</strong> {medico.nome}</Typography>
            <Typography variant="subtitle2"><strong>Paciente:</strong> {paciente.nome}</Typography>
          </Box>

          <form onSubmit={handleSubmit}>
            {/* Linha para CID e Data */}
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 2 }}>
              <Box sx={{ width: { xs: '100%', sm: '50%' } }}> {/* CID Autocomplete */}
                <Autocomplete
                  id="cid-autocomplete"
                  options={cidOptions}
                  multiple // Permite múltiplas seleções
                  disableCloseOnSelect // Mantém o dropdown aberto após selecionar um item
                  getOptionLabel={(option) => `${option.cid} - ${option.descricao}`}
                  value={selectedCids} // Usa o estado de CIDs selecionados (array)
                  onChange={(_event, newValue) => {
                    setSelectedCids(newValue); // Atualiza o array de CIDs selecionados
                    // Atualiza formFields.cids com os códigos dos CIDs selecionados
                    setFormFields((prev) => ({ ...prev, cids: newValue.map(cidOption => cidOption.cid) }));
                  }}
                  inputValue={cidInput}
                  onInputChange={(_event, newInputValue) => {
                    setCidInput(newInputValue);
                  }}
                  loading={loadingCid}
                  loadingText="Carregando..."
                  noOptionsText={cidInput.length < 3 ? "Digite ao menos 3 caracteres" : "Nenhum CID encontrado"}
                  filterOptions={(x) => x} // Desabilita filtro do cliente, busca é no backend
                  isOptionEqualToValue={(option, value) => option.cid === value.cid} // Compara pelo código do CID
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="CID (Código ou Descrição)"
                      variant="outlined"
                      size="small"
                      required={selectedCids.length === 0} // Obrigatório se nenhum CID estiver selecionado
                      InputProps={{
                        ...params.InputProps,
                        endAdornment: (
                          <>
                            {loadingCid ? <CircularProgress color="inherit" size={20} /> : null}
                            {params.InputProps.endAdornment}
                          </>
                        ),
                      }}
                    />
                  )}
                />
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' } }}>
                <TextField
                  label="Data"
                  type="date"
                  id="data"
                  name="data"
                  value={formFields.data}
                  onChange={handleChange}
                  required
                  fullWidth
                  variant="outlined"
                  size="small"
                  InputLabelProps={{ // Corrigido de slotProps para InputLabelProps
                    shrink: true,
                  }}
                />
              </Box>
            </Box>

            {/* Campo Parecer */}
            <Box sx={{ mb: 2 }}>
              <TextField
                label="Parecer"
                id="parecer"
                name="parecer"
                value={formFields.parecer}
                onChange={handleChange}
                required
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                size="small"
              />
            </Box>

            {/* Campo Abordagem Terapêutica */}
            <Box>
              <TextField
                label="Abordagem Terapêutica"
                id="abordagem_terapeutica"
                name="abordagem_terapeutica"
                value={formFields.abordagem_terapeutica}
                onChange={handleChange}
                required
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                size="small"
              />
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3, gap: 1 }}>
              <Button onClick={onClose} color="secondary" variant="outlined">
                Cancelar
              </Button>
              <Button type="submit" variant="contained" color="primary">
                Salvar Laudo
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Modal>
  );
};

// Estilo para o Box do Modal (similar a outros modais do projeto)
const modalStyle = {
  position: 'absolute' as const,
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: { xs: '95%', sm: '80%', md: '600px' }, // Ajustado para um bom tamanho
  bgcolor: 'transparent', // O Paper interno terá o fundo
  boxShadow: 24,
  borderRadius: 2, // O Paper interno terá o borderRadius
  // p: 0, // O Paper interno terá o padding
  maxHeight: '90vh',
  overflowY: 'auto',
};

export default LaudoCadastroModal;