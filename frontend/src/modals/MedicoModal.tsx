import React, { useEffect, useReducer } from "react";
import { Medico } from "../types/user";
import {
  TextField,
  Button,
  Box,
  Modal,
  Typography,
  CircularProgress,
} from "@mui/material";
import { Endereco } from "../types/endereco";

import ColumnResponsive from "../components/ColumnResponsive";
import { auth } from "../utils/auth";
import { useTheme, Theme } from "@mui/material/styles";

interface MedicoModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (feedback: { type: string; message: string }) => void;
  medico?: Medico | null;
  mode: "create" | "edit";
}
interface MedicoState {
  nome: string;
  email: string;
  crm: string;
  enderecos: Endereco[];
  especialidade: string; // Adicione o campo especialidades
}
const initialState: MedicoState = {
  nome: "",
  email: "",
  crm: "",
  enderecos: [],
  especialidade: "", // Inicialize o campo especialidades
};

const reducer = (state: MedicoState, action: any) => {
  switch (action.type) {
    case "SET_NOME":
      return { ...state, nome: action.payload };
    case "SET_EMAIL":
      return { ...state, email: action.payload };
    case "SET_CRM":
      return { ...state, crm: action.payload };
    case "SET_ESPECIALIDADE": // Adicione o caso para o campo especialidades
      return { ...state, especialidade: action.payload };
    default:
      return state;
  }
};

const MedicoModal: React.FC<MedicoModalProps> = ({
  open,
  onClose,
  medico,
  mode = "create",
  onSubmit,
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const [isLoading, setIsLoading] = React.useState(false);
  const [formErrors, setFormErrors] = React.useState<{
    nome?: string;
    email?: string;
    crm?: string;
    cpf?: string;
    especialidade?: string;
  }>({});
  const theme: Theme = useTheme();
  useEffect(() => {
    if (medico) {
      dispatch({ type: "SET_NOME", payload: medico.nome });
      dispatch({ type: "SET_CRM", payload: medico.crm });
      dispatch({
        type: "SET_ESPECIALIDADE",
        payload: medico.especialidade || "",
      }); // Carregue a especialidade

      fetch(`${import.meta.env.VITE_BACKEND_URL}/user/${medico.user_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.getToken()}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((data) => {
              dispatch({ type: "SET_EMAIL", payload: data.email });
            });
          } else {
            throw new Error("Erro ao buscar os dados do médico");
          }
        })
        .catch((error) => {
          onSubmit({
            type: "error",
            message: `Erro ao buscar os dados do médico: ${error}`,
          });
        });
    }
  }, [medico]);

  const validateForm = (): boolean => {
    const errors: {
      nome?: string;
      email?: string;
      crm?: string;
      cpf?: string;
    } = {};
    let valid = true;

    if (!state.nome.trim()) {
      errors.nome = "Nome é obrigatório";
      valid = false;
    }

    if (!state.email.trim()) {
      errors.email = "Email é obrigatório";
      valid = false;
    } else if (!/^\S+@\S+\.\S+$/.test(state.email)) {
      errors.email = "Email inválido";
      valid = false;
    }

    if (!state.crm.trim()) {
      errors.crm = "CRM é obrigatório";
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
        mode === "create"
          ? `${baseUrl}/medicos/register`
          : `${baseUrl}/medicos/${medico?.id}`;
      const response = await fetch(url, {
        method: mode === "create" ? "POST" : "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.getToken()}`,
        },
        body: JSON.stringify({
          ...state,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        onSubmit({
          type: "success",
          message:
            mode === "create"
              ? `Médico criado com sucesso! Um e-mail de confirmação foi enviado para ${state.email}.`
              : `Médico atualizado com sucesso!`,
        });
        onClose();
      } else {
        onSubmit({
          type: "error",
          message: data.message || "Falha ao salvar o médico",
        });
      }
    } catch (error) {
      onSubmit({
        type: "error",
        message: `Erro ao salvar o médico: ${error}`,
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
          backgroundColor: "white",
          width: { sm: "90%", md: "70%", lg: "50%" },
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          padding: 4,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <Typography variant="h6">
            {(mode === "create" ? "Criar" : "Editar") + " Médico"}
          </Typography>
          <Box
            sx={{
              cursor: "pointer",
              color: theme.palette.common.white,
              display: { xs: "block", md: "none" },
              backgroundColor: theme.palette.error.main,
              paddingX: "10px",
              paddingY: "6px",
              borderRadius: "10%",
              transition: "background-color 0.3s ease",
              "&:hover": {
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
              dispatch({ type: "SET_NOME", payload: e.target.value });
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
              dispatch({ type: "SET_EMAIL", payload: e.target.value });
              setFormErrors({ ...formErrors, email: undefined });
            }}
            fullWidth
            margin="normal"
            error={!!formErrors.email}
            helperText={formErrors.email}
            InputLabelProps={{
              shrink: state.email !== "",
            }}
          />

          <TextField
            label="CRM"
            size="small"
            value={state.crm}
            onChange={(e) =>
              dispatch({ type: "SET_CRM", payload: e.target.value })
            }
            fullWidth
            margin="normal"
            error={!!formErrors.crm}
            helperText={formErrors.crm}
          />
        </ColumnResponsive>

        <ColumnResponsive>
          <TextField
            label="Especialidade"
            size="small"
            value={state.especialidade}
            onChange={(e) =>
              dispatch({ type: "SET_ESPECIALIDADE", payload: e.target.value })
            }
            fullWidth
            margin="normal"
            error={!!formErrors.especialidade}
            helperText={formErrors.especialidade}
          />
        </ColumnResponsive>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
            marginY: "16px",
          }}
        >
       
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={isLoading}
            fullWidth
          >
            {isLoading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              "Salvar"
            )}
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default MedicoModal;
