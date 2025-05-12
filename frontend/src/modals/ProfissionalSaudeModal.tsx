import React, { useEffect, useReducer } from 'react';
import EnderecoModal from './EnderecoModal';
import { ProfissionalSaude } from "../types/user";
import { TextField, Button, Box, Modal, Typography, CircularProgress } from '@mui/material';
import { Endereco } from '../types/endereco';
import { ulid } from 'ulid';
import { AdressCard } from '../components/AdressCard';
import ColumnResponsive from '../components/ColumnResponsive';
import { auth } from '../utils/auth';
import { useTheme, Theme } from '@mui/material/styles';
import TopicInputField from '../components/TopicInputField'; // Importe o TopicInputField

interface ProfissionalSaudeModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (feedback: { type: string; message: string }) => void;
  profissionalSaude?: ProfissionalSaude | null;
  mode: 'create' | 'edit';
}

interface ProfissionalSaudeState {
  nome: string;
  email: string;
  registro_profissional: string;
  cpf: string;
  tipo_registro: string;
  estado_registro: string;
  
  telefone: string;
  enderecos: Endereco[];
  perfil: string[]; // Adicione o campo perfil
}

const initialState: ProfissionalSaudeState = {
  nome: '',
  email: '',
  registro_profissional: '',
  cpf: '',
  tipo_registro: '',
  estado_registro: '',
  telefone: '',
  enderecos: [],
  perfil: [], // Inicialize o campo perfil
};

const reducer = (state: ProfissionalSaudeState, action: any) => {
  switch (action.type) {
    case 'SET_NOME':
      return { ...state, nome: action.payload };
    case 'SET_EMAIL':
      return { ...state, email: action.payload };
    case 'SET_REGISTRO_PROFISSIONAL':
      return { ...state, registro_profissional: action.payload };
    case 'SET_CPF':
      return { ...state, cpf: action.payload };
    case 'SET_TIPO_REGISTRO':
      return { ...state, tipo_registro: action.payload };
    case 'SET_ESTADO_REGISTRO':
      return { ...state, estado_registro: action.payload };
    case 'SET_TELEFONE':
      return { ...state, telefone: action.payload };
    case 'SET_ENDERECOS':
      return { ...state, enderecos: action.payload };
    case 'ADD_ENDERECO': {
      const enderecoExiste = state.enderecos.some((endereco) => endereco.id === action.payload.id);
      if (enderecoExiste) {
        return state;
      }
      return { ...state, enderecos: [...state.enderecos, action.payload] };
    }
    case 'REMOVE_ENDERECO':
      return { ...state, enderecos: state.enderecos.filter((_, index) => index !== action.payload) };
    case 'SET_PERFIL': // Adicione o caso para o campo perfil
      return { ...state, perfil: action.payload };
    default:
      return state;
  }
};

const ProfissionalSaudeModal: React.FC<ProfissionalSaudeModalProps> = ({
  open,
  onClose,
  profissionalSaude,
  mode = 'create',
  onSubmit,
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [addresModalShow, setAddresModalShow] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [formErrors, setFormErrors] = React.useState<{
    nome?: string;
    email?: string;
    registro_profissional?: string;
    cpf?: string;
    tipo_registro?: string;
    estado_registro?: string;
  }>({});
  const theme: Theme = useTheme();

  useEffect(() => {
    if (profissionalSaude) {
      dispatch({ type: 'SET_NOME', payload: profissionalSaude.nome });
      dispatch({ type: 'SET_REGISTRO_PROFISSIONAL', payload: profissionalSaude.registro_profissional });
      dispatch({ type: 'SET_CPF', payload: profissionalSaude.cpf });
      dispatch({ type: 'SET_TIPO_REGISTRO', payload: profissionalSaude.tipo_registro });
      dispatch({ type: 'SET_ESTADO_REGISTRO', payload: profissionalSaude.estado_registro });
      dispatch({ type: 'SET_TELEFONE', payload: profissionalSaude.telefone || '' });
      dispatch({ type: 'SET_ENDERECOS', payload: profissionalSaude.enderecos || [] });
      dispatch({ type: 'SET_PERFIL', payload: profissionalSaude.perfil || [] }); // Carregue o perfil

      fetch(`${import.meta.env.VITE_BACKEND_URL}/user/users/${profissionalSaude.user_id}`, {
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
            throw new Error('Erro ao buscar os dados do profissional de saúde');
          }
        })
        .catch((error) => {
          onSubmit({
            type: 'error',
            message: `Erro ao buscar os dados do profissional de saúde: ${error}`,
          });
        });
    }
  }, [profissionalSaude]);

  const validateForm = (): boolean => {
    const errors: {
      nome?: string;
      email?: string;
      registro_profissional?: string;
      cpf?: string;
      tipo_registro?: string;
      estado_registro?: string;
    } = {};
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

    if (!state.registro_profissional.trim()) {
      errors.registro_profissional = 'Registro profissional é obrigatório';
      valid = false;
    }

    if (!state.cpf.trim()) {
      errors.cpf = 'CPF é obrigatório';
      valid = false;
    }

    if (!state.tipo_registro.trim()) {
      errors.tipo_registro = 'Tipo de registro é obrigatório';
      valid = false;
    }

    if (!state.estado_registro.trim()) {
      errors.estado_registro = 'Estado do registro é obrigatório';
      valid = false;
    }

    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    console.log('state', state);
    setIsLoading(true);

    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL;
      const url =
        mode === 'create'
          ? `${baseUrl}/profissionais_saude/register`
          : `${baseUrl}/profissionais_saude/${profissionalSaude?.id}`;
      const response = await fetch(url, {
        method: mode === 'create' ? 'POST' : 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${auth.getToken()}`,
        },
        body: JSON.stringify({
          ...state,
          id: profissionalSaude?.id || ulid(),
          perfil: JSON.stringify(state.perfil) // Converta o array para string JSON
        }),
      });

      const data = await response.json();

      if (response.ok) {
        onSubmit({
          type: 'success',
          message:
            mode === 'create'
              ? `Profissional de saúde criado com sucesso! Um e-mail de confirmação foi enviado para ${state.email}.`
              : `Profissional de saúde atualizado com sucesso!`,
        });
        onClose();
      } else {
        onSubmit({
          type: 'error',
          message: data.message || 'Falha ao salvar o profissional de saúde',
        });
      }
    } catch (error) {
      onSubmit({
        type: 'error',
        message: `Erro ao salvar o profissional de saúde: ${error}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePerfilChange = (newPerfil: string[]) => {
    dispatch({ type: 'SET_PERFIL', payload: newPerfil });
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
          maxHeight: '80vh', // Adicione uma altura máxima
          overflowY: 'auto', // Adicione overflow para habilitar a rolagem
        }}
      >
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Typography variant="h6">
            {(mode === 'create' ? 'Criar' : 'Editar') + ' Profissional de Saúde'}
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
            label="Registro Profissional"
            size="small"
            value={state.registro_profissional}
            onChange={(e) => {
              dispatch({ type: 'SET_REGISTRO_PROFISSIONAL', payload: e.target.value });
              setFormErrors({ ...formErrors, registro_profissional: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.registro_profissional}
            helperText={formErrors.registro_profissional}
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
        <ColumnResponsive>
          <TextField
            label="Tipo de Registro"
            size="small"
            value={state.tipo_registro}
            onChange={(e) => {
              dispatch({ type: 'SET_TIPO_REGISTRO', payload: e.target.value });
              setFormErrors({ ...formErrors, tipo_registro: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.tipo_registro}
            helperText={formErrors.tipo_registro}
          />
          <TextField
            label="Estado do Registro"
            size="small"
            value={state.estado_registro}
            onChange={(e) => {
              dispatch({ type: 'SET_ESTADO_REGISTRO', payload: e.target.value });
              setFormErrors({ ...formErrors, estado_registro: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.estado_registro}
            helperText={formErrors.estado_registro}
          />
        </ColumnResponsive>

        {/* Adicione o TopicInputField */}
        <ColumnResponsive>
          <TopicInputField
            initialTopics={state.perfil}
            onChange={handlePerfilChange}
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
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={isLoading}
            fullWidth
          >
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

export default ProfissionalSaudeModal;