import React, { useEffect, useReducer, useState } from 'react';
import EnderecoModal from './EnderecoModal';
import { Colaborador } from '../types/user';
import { TextField, Button, Box, Modal, Typography, CircularProgress } from '@mui/material';
import { Endereco } from '../types/endereco';
import { ulid } from 'ulid';
import { AdressCard } from '../components/AdressCard';
import ColumnResponsive from '../components/ColumnResponsive';
import { auth } from '../utils/auth';
import { useTheme, Theme } from '@mui/material/styles';

interface ColaboradorModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (feedback: { type: string; message: string }) => void;
  colaborador?: Colaborador | null;
  mode: 'create' | 'edit';
}

interface ColaboradorState {
  nome: string;
  email: string;
  cpf: string;
  funcao: string;
  telefone: string;
  enderecos: Endereco[];
}

const initialState: ColaboradorState = {
  nome: '',
  email: '',
  cpf: '',
  funcao: '',
  telefone: '',
  enderecos: [],
};

const reducer = (state: ColaboradorState, action: any) => {
  switch (action.type) {
    case 'SET_NOME':
      return { ...state, nome: action.payload };
    case 'SET_EMAIL':
      return { ...state, email: action.payload };
    case 'SET_CPF':
      return { ...state, cpf: action.payload };
    case 'SET_FUNCAO':
      return { ...state, funcao: action.payload };
    case 'SET_TELEFONE':
      return { ...state, telefone: action.payload };
    case 'SET_ENDERECOS':
      return { ...state, enderecos: action.payload };
    case 'ADD_ENDERECO':
      const enderecoExiste = state.enderecos.some(
        (endereco) => endereco.id === action.payload.id
      );
      if (enderecoExiste) {
        return state;
      }
      return { ...state, enderecos: [...state.enderecos, action.payload] };
    case 'REMOVE_ENDERECO':
      return { ...state, enderecos: state.enderecos.filter((_, index) => index !== action.payload) };
    default:
      return state;
  }
};

const ColaboradorModal: React.FC<ColaboradorModalProps> = ({
  open,
  onClose,
  colaborador,
  mode = 'create',
  onSubmit,
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [formErrors, setFormErrors] = useState<{ nome?: string; email?: string; cpf?: string }>({});
  const [addresModalShow, setAddresModalShow] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const theme: Theme = useTheme();

  useEffect(() => {
    if (colaborador) {
      dispatch({ type: 'SET_NOME', payload: colaborador.nome });
      dispatch({ type: 'SET_CPF', payload: colaborador.cpf });
      dispatch({ type: 'SET_FUNCAO', payload: colaborador.funcao || '' });
      dispatch({ type: 'SET_TELEFONE', payload: colaborador.telefone || '' });
      dispatch({ type: 'SET_ENDERECOS', payload: colaborador.enderecos || [] });

      fetch(`${import.meta.env.VITE_BACKEND_URL}/user/users/${colaborador.user_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${auth.getToken()}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((data) => {
              dispatch({ type: 'SET_EMAIL', payload: data.email });
            });
          } else {
            throw new Error('Erro ao buscar os dados do colaborador');
          }
        })
        .catch((error) => {
          onSubmit({
            type: 'error',
            message: `Erro ao buscar os dados do colaborador: ${error}`,
          });
        });
    }
  }, [colaborador]);

  const validateForm = (): boolean => {
    const errors: { nome?: string; email?: string; cpf?: string } = {};
    let valid = true;

    if (!state.nome.trim()) {
      errors.nome = 'Nome é obrigatório';
      valid = false;
    }
    if (!state.email.trim()) {
      errors.email = 'Email é obrigatório';
      valid = false;
    } else if (!/^\S+@\S+\.\S+$/.test(state.email)) {
      errors.email = 'Email inválido';
      valid = false;
    }
    if (!state.cpf.trim()) {
      errors.cpf = 'CPF é obrigatório';
      valid = false;
    }
    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    setIsLoading(true);
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const url =
        mode === 'create'
          ? `${baseUrl}/colaboradores/register`
          : `${baseUrl}/colaboradores/${colaborador?.id}`;
      const response = await fetch(url, {
        method: mode === 'create' ? 'POST' : 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${auth.getToken()}`,
        },
        body: JSON.stringify({
          ...state,
          id: colaborador?.id || ulid(),
        }),
      });
      const data = await response.json();
      if (response.ok) {
        onSubmit({
          type: 'success',
          message:
            mode === 'create'
              ? 'Colaborador criado com sucesso!'
              : 'Colaborador atualizado com sucesso!',
        });
        onClose();
      } else {
        onSubmit({
          type: 'error',
          message: data.message || 'Falha ao salvar o colaborador',
        });
      }
    } catch (error) {
      onSubmit({
        type: 'error',
        message: `Erro ao salvar o colaborador: ${error}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        id="modal-box"
        sx={{
          backgroundColor: 'white',
          width: { sm: '90%', md: '50%', lg: '30%' },
          margin: 'auto',
          transform: { md: 'translateY(10%)', lg: 'translateY(10%)' },
          padding: '24px',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Typography variant="h6">
            {(mode === 'create' ? 'Criar' : 'Editar') + ' Colaborador'}
          </Typography>
          <Box
            sx={{
              cursor: 'pointer',
              color: theme.palette.common.white,
              display: { xs: 'block', md: 'none' },
              backgroundColor: theme.palette.error.main,
              paddingX: '10px',
              paddingY: '6px',
              borderRadius: '10%',
              transition: 'background-color 0.3s ease',
              '&:hover': {
                backgroundColor: theme.palette.error.light,
              },
            }}
            onClick={onClose}
          >
            X
          </Box>
        </Box>

        <ColumnResponsive>
          <TextField
            size="small"
            label="Nome"
            value={state.nome}
            onChange={(e) => {
              dispatch({ type: 'SET_NOME', payload: e.target.value });
              setFormErrors({ ...formErrors, nome: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.nome}
            helperText={formErrors.nome}
          />
        </ColumnResponsive>
        <ColumnResponsive>
          <TextField
            label="Email"
            size="small"
            value={state.email}
            onChange={(e) => {
              dispatch({ type: 'SET_EMAIL', payload: e.target.value });
              setFormErrors({ ...formErrors, email: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.email}
            helperText={formErrors.email}
            InputLabelProps={{
              shrink: state.email !== '',
            }}
          />
          <TextField
            label="Telefone"
            size="small"
            value={state.telefone}
            onChange={(e) => dispatch({ type: 'SET_TELEFONE', payload: e.target.value })}
            fullWidth
            margin="normal"
          />
        </ColumnResponsive>
        <ColumnResponsive>
          <TextField
            label="Função"
            size="small"
            value={state.funcao}
            onChange={(e) => dispatch({ type: 'SET_FUNCAO', payload: e.target.value })}
            fullWidth
            margin="normal"
          />
          <TextField
            label="CPF"
            size="small"
            value={state.cpf}
            onChange={(e) => {
              dispatch({ type: 'SET_CPF', payload: e.target.value });
              setFormErrors({ ...formErrors, cpf: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.cpf}
            helperText={formErrors.cpf}
          />
        </ColumnResponsive>
        <Box
          sx={{
            border: '1px solid #ccc',
            minHeight: '150px',
            borderRadius: '10px',
            padding: '10px',
            marginY: '16px',
            overflowY: 'auto',
          }}
        >
          {state.enderecos.map((endereco: Endereco) => (
            <AdressCard
              key={endereco.id}
              endereco={endereco}
              onDelete={(id: string) => {
                dispatch({
                  type: 'REMOVE_ENDERECO',
                  payload: state.enderecos.findIndex((e: Endereco) => e.id === id),
                });
              }}
            />
          ))}
        </Box>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            marginY: '16px',
          }}
        >
          <Button variant="contained" onClick={() => setAddresModalShow(true)} fullWidth>
            Adicionar Endereço
          </Button>
          <Button variant="contained" onClick={handleSubmit} disabled={isLoading} fullWidth>
            {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Salvar'}
          </Button>
        </Box>
        <EnderecoModal
          open={addresModalShow}
          onClose={() => setAddresModalShow(false)}
          onSubmit={(endereco) => {
            dispatch({ type: 'ADD_ENDERECO', payload: { ...endereco, id: ulid() } });
          }}
        />
      </Box>
    </Modal>
  );
};

export default ColaboradorModal;