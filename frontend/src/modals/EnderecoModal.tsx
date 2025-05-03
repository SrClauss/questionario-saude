import React, { useState, useEffect } from 'react';
import { Endereco } from '../types/endereco';
import { TextField, Button, Box, Modal, Typography, FormHelperText } from '@mui/material';
import { ulid } from 'ulid';
import ColumnResponsive from '../components/ColumnResponsive';

const style = {
  position: 'absolute' as const,
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: { xs: '90%', sm: '90%', md: '50%', lg: '30%' },
  bgcolor: 'background.paper',
  boxShadow: 24,
  borderRadius: 2,
  padding: '24px',
  maxHeight: { xs: '95%', md: '70%' },
  overflowY: 'auto',
};

interface EnderecoModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: Endereco) => void;
  endereco?: Endereco | null;
}

export default function EnderecoModal({ open, onClose, onSubmit, endereco }: EnderecoModalProps) {
  const [cep, setCep] = useState(endereco?.cep || '');
  const [logradouro, setLogradouro] = useState(endereco?.logradouro || '');
  const [numero, setNumero] = useState(endereco?.numero || '');
  const [bairro, setBairro] = useState(endereco?.bairro || '');
  const [cidade, setCidade] = useState(endereco?.cidade || '');
  const [estado, setEstado] = useState(endereco?.estado || '');
  const [complemento, setComplemento] = useState(endereco?.complemento || '');
  const [id, setId] = useState(endereco?.id || ulid());
  const [errors, setErrors] = useState<{
    cep?: string;
    logradouro?: string;
    numero?: string;
    bairro?: string;
    cidade?: string;
    estado?: string;
  }>({});

  useEffect(() => {
    // Atualiza os campos caso o endereço seja editado
    if (endereco) {
      setCep(endereco.cep || '');
      setLogradouro(endereco.logradouro || '');
      setNumero(endereco.numero || '');
      setBairro(endereco.bairro || '');
      setCidade(endereco.cidade || '');
      setEstado(endereco.estado || '');
      setComplemento(endereco.complemento || '');
      setId(endereco.id);
      setErrors({});
    } else {
      // Limpa campos para novo endereço
      setCep('');
      setLogradouro('');
      setNumero('');
      setBairro('');
      setCidade('');
      setEstado('');
      setComplemento('');
      setId(ulid());
      setErrors({});
    }
  }, [endereco, open]);

  const handleBlurCep = (e: React.FocusEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, '');
    setCep(value);
    if (value.length === 8) {
      fetch(`https://viacep.com.br/ws/${value}/json/`)
        .then((response) => response.json())
        .then((data) => {
          setLogradouro(data.logradouro || '');
          setBairro(data.bairro || '');
          setCidade(data.localidade || '');
          setEstado(data.uf || '');
        })
        .catch((error) => console.error('Error fetching address:', error));
    }
  };

  const validateFields = (): boolean => {
    const newErrors: {
      cep?: string;
      logradouro?: string;
      numero?: string;
      bairro?: string;
      cidade?: string;
      estado?: string;
    } = {};
    let valid = true;

    if (!cep.trim()) {
      newErrors.cep = 'CEP é obrigatório';
      valid = false;
    }
    if (!logradouro.trim()) {
      newErrors.logradouro = 'Logradouro é obrigatório';
      valid = false;
    }
    if (!numero.trim()) {
      newErrors.numero = 'Número é obrigatório';
      valid = false;
    }
    if (!bairro.trim()) {
      newErrors.bairro = 'Bairro é obrigatório';
      valid = false;
    }
    if (!cidade.trim()) {
      newErrors.cidade = 'Cidade é obrigatória';
      valid = false;
    }
    if (!estado.trim()) {
      newErrors.estado = 'Estado é obrigatório';
      valid = false;
    }

    setErrors(newErrors);
    return valid;
  };

  const handleSubmit = () => {
    if (!validateFields()) return;
    const newEndereco = new Endereco(
      id,
      logradouro,
      numero,
      bairro,
      cidade,
      estado,
      cep,
      complemento
    );
    console.log(newEndereco);
    onSubmit(newEndereco);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            {endereco ? 'Editar Endereço' : 'Adicionar Endereço'}
          </Typography>
          <Button onClick={onClose} variant="contained" color="error">X</Button>
        </Box>
        <ColumnResponsive>
          <TextField
            label="CEP"
            size="small"
            value={cep}
            onChange={(e) => setCep(e.target.value)}
            onBlur={handleBlurCep}
            fullWidth
            margin="normal"
            error={!!errors.cep}
            helperText={errors.cep}
          />
          <TextField
            label="Logradouro"
            size="small"
            value={logradouro}
            onChange={(e) => setLogradouro(e.target.value)}
            fullWidth
            margin="normal"
            error={!!errors.logradouro}
            helperText={errors.logradouro}
          />
        </ColumnResponsive>
        <ColumnResponsive>
          <TextField
            label="Número"
            size="small"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            fullWidth
            margin="normal"
            error={!!errors.numero}
            helperText={errors.numero}
          />
          <TextField
            label="Complemento"
            size="small"
            value={complemento}
            onChange={(e) => setComplemento(e.target.value)}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Bairro"
            size="small"
            value={bairro}
            onChange={(e) => setBairro(e.target.value)}
            fullWidth
            margin="normal"
            error={!!errors.bairro}
            helperText={errors.bairro}
          />
        </ColumnResponsive>
        <ColumnResponsive>
          <TextField
            label="Cidade"
            size="small"
            value={cidade}
            onChange={(e) => setCidade(e.target.value)}
            fullWidth
            margin="normal"
            error={!!errors.cidade}
            helperText={errors.cidade}
          />
          <TextField
            label="Estado"
            size="small"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            fullWidth
            margin="normal"
            error={!!errors.estado}
            helperText={errors.estado}
          />
        </ColumnResponsive>
        <Button variant="contained" color="primary" fullWidth onClick={handleSubmit} sx={{ mt: 2 }}>
          {endereco ? 'Salvar' : 'Adicionar'}
        </Button>
        <Button variant="outlined" color="error" fullWidth onClick={onClose} sx={{ mt: 2 }}>
          Cancelar
        </Button>
      </Box>
    </Modal>
  );
}