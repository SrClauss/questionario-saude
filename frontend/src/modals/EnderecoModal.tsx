import { Endereco } from '../types/endereco';
import { TextField, Button, Box, Modal, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { ulid } from 'ulid';
import ColumnResponsive from '../components/ColumnResponsive';

const style = {
    position: 'absolute' as const,
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: { xs: '100%', sm: 400 },
    bgcolor: 'background.paper',
    boxShadow: 24,



};
interface EnderecoModalProps {

    open: boolean;
    onClose: () => void;
    onSubmit: (data: Endereco) => void;
    endereco?: Endereco | null;
}



export default function EnderecoModal({ open, onClose, onSubmit, endereco }: EnderecoModalProps) {
    const [cep, setCep] = React.useState(endereco?.cep || '');
    const [logradouro, setLogradouro] = React.useState(endereco?.logradouro || '');
    const [numero, setNumero] = React.useState(endereco?.numero || '');
    const [bairro, setBairro] = React.useState(endereco?.bairro || '');
    const [cidade, setCidade] = React.useState(endereco?.cidade || '');
    const [estado, setEstado] = React.useState(endereco?.estado || '');
    const [complemento, setComplemento] = React.useState(endereco?.complemento || '');
    const [id, setId] = React.useState(endereco?.id || ulid());
 
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
    }

    const handleSubmit = () => {
        const newEndereco = new Endereco(id, logradouro, numero, bairro, cidade, estado, cep, complemento);

        console.log(newEndereco)
        onSubmit(newEndereco);
        onClose();
    }
    return (
        <Modal
            open={open}
            onClose={onClose}
        >
            <Box sx={{
                backgroundColor: 'white',
                width: { xs: '90%', sm: '90%', md: '50%', lg: '30%' },
                position: { xs: 'absolute', md: 'absolute' },
                top: { xs: 'auto', md: '50%' },
                left: { xs: 'auto', md: '50%' },
                transform: { 
                    xs: 'translateY(10%)',
                    md: 'translate(-50%, -50%)' // Centralização completa em md e acima
                },
                height: 'auto',
                margin: { xs: 'auto', md: '0' }, // Remove margin auto em telas grandes
                padding: '24px',
                maxHeight: { xs: '95%', md: '70%' },
                overflowY: 'auto',
                // Arredondamento para melhor aparência
                borderRadius: 2,
            }}>

                <Box sx={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2}}>

                <Typography id="modal-modal-title" variant="h6" component="h2">
                    {endereco ? 'Editar Endereço' : 'Adicionar Endereço'}
                </Typography>
                <Button onClick={onClose} variant="contained" color="error">X</Button>
                </Box>
                <ColumnResponsive>
                
                    <TextField
                        label="CEP"
                        size='small'
                        value={cep}
                        onChange={(e) => setCep(e.target.value)}
                        onBlur={handleBlurCep}
                        fullWidth
                        margin="normal"
                      
                    />
                    <TextField
                        label="Logradouro"
                        size='small'
                        value={logradouro}
                        onChange={(e) => setLogradouro(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                </ColumnResponsive>

                <ColumnResponsive>
                
                
                <TextField
                    label="Número"
                    value={numero}
                    size='small'
                    onChange={(e) => setNumero(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Complemento"
                    size='small'
                    value={complemento}
                    onChange={(e) => setComplemento(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Bairro"
                    size='small'
                    value={bairro}
                    onChange={(e) => setBairro(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                </ColumnResponsive>
                <ColumnResponsive>
                
                    <TextField
                        label="Cidade"
                        size='small'
                        value={cidade}
                        onChange={(e) => setCidade(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Estado"
                        size='small'
                        value={estado}
                        onChange={(e) => setEstado(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                </ColumnResponsive>
                <Button variant="contained" color="primary" fullWidth onClick={handleSubmit}>
                    {endereco ? 'Salvar' : 'Adicionar'}
                </Button>
                <Button variant="outlined" color="error" fullWidth onClick={onClose} sx={{ marginTop: 2 }}>
                   Cancelar
                </Button>
            </Box>
        </Modal>
    );




}