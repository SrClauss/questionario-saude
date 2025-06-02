import React, { useEffect, useReducer, useState } from 'react';
import EnderecoModal from './EnderecoModal';
import { TextField, Button, Box, Modal, Typography, CircularProgress } from '@mui/material';
import { Endereco } from '../types/endereco';
import ColumnResponsive from '../components/ColumnResponsive';
import { auth } from '../utils/auth';
import { useTheme, Theme } from '@mui/material/styles';

// Define the UnidadeSaude type based on your backend model
export interface UnidadeSaude {
  id: string;
  nome: string;
  cnpj: string;
  endereco: Endereco;
  telefone?: string;
  email?: string;
  created_at?: string;
  updated_at?: string;
}

interface UnidadeSaudeModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (feedback: { type: string; message: string }) => void;
  unidadeSaude?: UnidadeSaude | null;
  mode: 'create' | 'edit';
}

interface UnidadeSaudeState {
  nome: string;
  cnpj: string;
  endereco: Endereco | null;
  telefone: string;
  email: string;
}

const initialState: UnidadeSaudeState = {
  nome: '',
  cnpj: '',
  endereco: null,
  telefone: '',
  email: '',
};

type Action =
  | { type: 'SET_NOME'; payload: string }
  | { type: 'SET_CNPJ'; payload: string }
  | { type: 'SET_ENDERECO'; payload: Endereco | null }
  | { type: 'SET_TELEFONE'; payload: string }
  | { type: 'SET_EMAIL'; payload: string }
  | { type: 'RESET_STATE'; payload: UnidadeSaudeState };

const reducer = (state: UnidadeSaudeState, action: Action): UnidadeSaudeState => {
  switch (action.type) {
    case 'SET_NOME':
      return { ...state, nome: action.payload };
    case 'SET_CNPJ':
      return { ...state, cnpj: action.payload };
    case 'SET_ENDERECO':
      return { ...state, endereco: action.payload };
    case 'SET_TELEFONE':
      return { ...state, telefone: action.payload };
    case 'SET_EMAIL':
      return { ...state, email: action.payload };
    case 'RESET_STATE':
      return action.payload;
    default:
      return state;
  }
};

const UnidadeSaudeModal: React.FC<UnidadeSaudeModalProps> = ({
  open,
  onClose,
  unidadeSaude,
  mode = 'create',
  onSubmit,
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [formErrors, setFormErrors] = useState<{ nome?: string; cnpj?: string; endereco?: string; email?: string }>({});
  const [enderecoModalShow, setEnderecoModalShow] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const theme: Theme = useTheme();

  useEffect(() => {
    if (open) {
      if (mode === 'edit' && unidadeSaude) {
        dispatch({ type: 'SET_NOME', payload: unidadeSaude.nome });
        dispatch({ type: 'SET_CNPJ', payload: unidadeSaude.cnpj });
        dispatch({ type: 'SET_ENDERECO', payload: unidadeSaude.endereco });
        dispatch({ type: 'SET_TELEFONE', payload: unidadeSaude.telefone || '' });
        dispatch({ type: 'SET_EMAIL', payload: unidadeSaude.email || '' });
        setFormErrors({});
      } else {
        dispatch({ type: 'RESET_STATE', payload: { ...initialState } });
        setFormErrors({});
      }
    }
  }, [open, mode, unidadeSaude, dispatch]);

  const validateForm = (): boolean => {
    const errors: { nome?: string; cnpj?: string; endereco?: string; email?: string } = {};
    let valid = true;

    if (!state.nome.trim()) {
      errors.nome = 'Nome é obrigatório';
      valid = false;
    }
    if (!state.cnpj.trim()) {
      // Add CNPJ specific validation if needed (e.g., format, length)
      errors.cnpj = 'CNPJ é obrigatório';
      valid = false;
    }
    if (!state.endereco) {
      errors.endereco = 'Endereço é obrigatório';
      valid = false;
    }
    if (state.email.trim() && !/^\S+@\S+\.\S+$/.test(state.email)) {
        errors.email = 'Email inválido';
        valid = false;
    }

    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    setIsLoading(true);

    const payload = {
      nome: state.nome,
      cnpj: state.cnpj,
      endereco: state.endereco, // Backend expects a JSON object for endereco
      telefone: state.telefone,
      email: state.email,
    };
    console.log(payload);

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const url =
        mode === 'create'
          ? `${baseUrl}/unidades_saude/`
          : `${baseUrl}/unidades_saude/${unidadeSaude?.id}`;
      const response = await fetch(url, {
        method: mode === 'create' ? 'POST' : 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${auth.getToken()}`,
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (response.ok) {
        onSubmit({
          type: 'success',
          message:
            mode === 'create'
              ? 'Unidade de Saúde criada com sucesso!'
              : 'Unidade de Saúde atualizada com sucesso!',
        });
        onClose();
      } else {
        onSubmit({
          type: 'error',
          message: data.message || 'Falha ao salvar a Unidade de Saúde',
        });
      }
    } catch (error) {
      onSubmit({
        type: 'error',
        message: `Erro ao salvar a Unidade de Saúde: ${error instanceof Error ? error.message : String(error)}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: { xs: '90%', sm: '70%', md: '50%', lg: '40%' },
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          borderRadius: 2,
          maxHeight: '90vh',
          overflowY: 'auto',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            {(mode === 'create' ? 'Criar Nova' : 'Editar') + ' Unidade de Saúde'}
          </Typography>
          <Button
            onClick={onClose}
            sx={{
                minWidth: 'auto',
                padding: '6px',
                display: { xs: 'inline-flex', md: 'none' }, // Show on mobile, hide on md up
                color: theme.palette.common.white,
                backgroundColor: theme.palette.error.main,
                '&:hover': {
                    backgroundColor: theme.palette.error.light,
                },
            }}
            >
            X
          </Button>
        </Box>

        <TextField
          label="Nome da Unidade"
          value={state.nome}
          onChange={(e) => {
            dispatch({ type: 'SET_NOME', payload: e.target.value });
            setFormErrors({ ...formErrors, nome: undefined });
          }}
          fullWidth
          margin="normal"
          error={!!formErrors.nome}
          helperText={formErrors.nome}
          disabled={isLoading}
        />
        <TextField
          label="CNPJ"
          value={state.cnpj}
          onChange={(e) => {
            dispatch({ type: 'SET_CNPJ', payload: e.target.value });
            setFormErrors({ ...formErrors, cnpj: undefined });
          }}
          fullWidth
          margin="normal"
          error={!!formErrors.cnpj}
          helperText={formErrors.cnpj}
          disabled={isLoading}
        />
        <TextField
          label="Telefone"
          value={state.telefone}
          onChange={(e) => dispatch({ type: 'SET_TELEFONE', payload: e.target.value })}
          fullWidth
          margin="normal"
          disabled={isLoading}
        />
        <TextField
          label="Email"
          value={state.email}
          onChange={(e) => {
            dispatch({ type: 'SET_EMAIL', payload: e.target.value });
            if (formErrors.email) setFormErrors({...formErrors, email: undefined});
          }}
          fullWidth
          margin="normal"
          error={!!formErrors.email}
          helperText={formErrors.email}
          disabled={isLoading}
        />

        <Typography variant="subtitle2" gutterBottom sx={{mt: 2}}>Endereço</Typography>
        {state.endereco ? (
          <Box sx={{ border: '1px solid #ccc', p: 2, borderRadius: 1, mb: 1 }}>
            <Typography variant="body2">{`${state.endereco.logradouro}, ${state.endereco.numero}`}</Typography>
            <Typography variant="body2">{`${state.endereco.bairro}, ${state.endereco.cidade} - ${state.endereco.estado}`}</Typography>
            <Typography variant="body2">CEP: {state.endereco.cep}</Typography>
            {state.endereco.complemento && <Typography variant="body2">Complemento: {state.endereco.complemento}</Typography>}
            <Button variant="outlined" size="small" onClick={() => setEnderecoModalShow(true)} sx={{ mt: 1 }} disabled={isLoading}>
              Editar Endereço
            </Button>
          </Box>
        ) : (
          <Button variant="contained" onClick={() => setEnderecoModalShow(true)} fullWidth sx={{ mb: 1 }} disabled={isLoading}>
            Adicionar Endereço
          </Button>
        )}
        {formErrors.endereco && <Typography color="error" variant="caption" display="block">{formErrors.endereco}</Typography>}

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
          <Button onClick={onClose} color="secondary" disabled={isLoading}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Salvar'}
          </Button>
        </Box>

        <EnderecoModal
          open={enderecoModalShow}
          onClose={() => setEnderecoModalShow(false)}
          onSubmit={(enderecoData) => {
            dispatch({ type: 'SET_ENDERECO', payload: enderecoData });
            if (formErrors.endereco) setFormErrors({...formErrors, endereco: undefined});
            setEnderecoModalShow(false);
          }}
          endereco={state.endereco}
        />
      </Box>
    </Modal>
  );
};

export default UnidadeSaudeModal;