import React, { useState, useEffect } from 'react';
import { Box, Typography,  Container, Avatar, Fab } from '@mui/material';
import { auth } from '../utils/auth';
import { useNavigate } from 'react-router-dom';
const PacienteHomeScreen: React.FC = () => {
  const userId = auth.getUserData()?.id; // Obtém o ID do usuário do auth
  const [baterias, setBaterias] = useState<any[]>([]); // Inicializa o estado para armazenar as baterias
  const [paciente, setPaciente] = useState<any>(null); // Inicializa o estado para armazenar o 
  const navigate = useNavigate(); // Hook para navegação
  useEffect(() => {
    const fetchPaciente = async () => {
      try {
          const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/pacientes/get_paciente_by_user_id/${userId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
          },
        });
        const data = await response.json();
   
        setPaciente(data);
      } catch (error) {
        console.error('Error fetching paciente:', error);
      }
    };

    fetchPaciente();
  }, [userId]);

  useEffect(() => {
    const fetchBaterias = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/baterias_testes/paciente/${paciente.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('@App:token')}`,
          },
        });
        const data = await response.json();
        setBaterias(data);
      } catch (error) {
        console.error('Error fetching baterias:', error);
      }
    };
    if (paciente) {
      fetchBaterias();
    }
  }, [paciente]);
  useEffect(() => {
    //Verifica se em baterias existe algu
  }, [baterias]);

  
  const handleLogout = () => {
    localStorage.removeItem('@App:token'); // Remove o token do localStorage
    navigate('/login'); // Redireciona para a página de login
  }

  return (
    <Container maxWidth="lg" sx={{ padding: 2, height: '90vh' }}>
    <Fab
        color="primary"
        aria-label="add"
        sx={{
          position: 'absolute',
          bottom: 16,
          right: 16,
        }}
        onClick={handleLogout}

      >

        <Avatar sx={{ width: 56, height: 56 }}>
          <Typography variant="h6">S</Typography>
        </Avatar>
      </Fab>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          backgroundColor: 'white',
          height: '100%', // Garante que o Box ocupe toda a altura do Container
          padding: 2,
          borderRadius: 2,
          boxShadow: 3,
          overflow: 'auto', // Adiciona scroll apenas se o conteúdo exceder a altura
        }}
      >
     
        <Typography variant="h4">Área do Paciente</Typography>
        <div>{JSON.stringify(paciente)}</div>
      </Box>
    </Container>
  );
};

export default PacienteHomeScreen;


/*

Rota: /static/<path:filename> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/user/users -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/user/users/<string:id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/user/users -> Métodos: POST, OPTIONS
Rota: /backend/user/users/<string:id> -> Métodos: PUT, OPTIONS
Rota: /backend/user/users/<string:id> -> Métodos: DELETE, OPTIONS
Rota: /backend/user/users/login -> Métodos: POST, OPTIONS
Rota: /backend/user/<string:user_id>/upload -> Métodos: POST, OPTIONS
Rota: /backend/user/<string:user_id>/image -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/user/users/set_password -> Métodos: PUT, OPTIONS
Rota: /backend/profissionais_saude/profissionais_saude/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/profissionais_saude/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/profissionais_saude/ -> Métodos: POST, OPTIONS
Rota: /backend/profissionais_saude/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/profissionais_saude/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/profissionais_saude/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/profissionais_saude/register -> Métodos: POST, OPTIONS
Rota: /backend/profissionais_saude/set-password-confirm-email -> Métodos: POST, OPTIONS
Rota: /backend/profissionais_saude/email/<email> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/profissionais_saude/filter_by_name/<name>/<page>/<len>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/profissionais_saude/filter_by_name/<name>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/ -> Métodos: POST, OPTIONS
Rota: /backend/pacientes/register -> Métodos: POST, OPTIONS
Rota: /backend/pacientes/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/pacientes/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/pacientes/email/<email> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/filter_by_name/<name>/<int:page>/<int:len>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/pacientes/filter_by_name/<name>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/ -> Métodos: POST, OPTIONS
Rota: /backend/colaboradores/register -> Métodos: POST, OPTIONS
Rota: /backend/colaboradores/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/colaboradores/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/colaboradores/email/<email> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/filter_by_name/<name>/<page>/<len>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/colaboradores/filter_by_name/<name>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/ -> Métodos: POST, OPTIONS
Rota: /backend/questionario/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/questionario/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/questionario/<questionario_id>/sessoes -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/detailed/<int:page>/<int:len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/detailed -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/detailed/<string:id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/find_by_title_or_description/<string:search>/<int:page>/<int:len>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/find_by_title_or_description/<string:search>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/questionario/number_of_queries/<string:id>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/ -> Métodos: POST, OPTIONS
Rota: /backend/sessoes/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/sessoes/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/sessoes/questionario/<questionario_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/detailed/<int:page>/<int:len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/detailed -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/detailed/<string:id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/sessoes/<sessao_id>/alternativas-lote -> Métodos: POST, OPTIONS
Rota: /backend/perguntas/<page>/<len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/ -> Métodos: POST, OPTIONS
Rota: /backend/perguntas/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/perguntas/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/perguntas/sessao/<sessao_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/<id>/alternativas -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/detailed/<int:page>/<int:len> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/detailed -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/detailed/<string:id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/perguntas/<id>/batch -> Métodos: POST, OPTIONS
Rota: /backend/alternativas/<int:page>/<int:per_page>/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/alternativas/ -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/alternativas/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/alternativas/ -> Métodos: POST, OPTIONS
Rota: /backend/alternativas/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/alternativas/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/alternativas/batch -> Métodos: PUT, OPTIONS
Rota: /backend/baterias_testes -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes -> Métodos: POST, OPTIONS
Rota: /backend/baterias_testes/<id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes/<id> -> Métodos: PUT, OPTIONS
Rota: /backend/baterias_testes/<id> -> Métodos: DELETE, OPTIONS
Rota: /backend/baterias_testes/paciente/<paciente_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes/profissional/<profissional_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes/colaborador/<colaborador_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes/questionario/<questionario_id> -> Métodos: GET, HEAD, OPTIONS
Rota: /backend/baterias_testes/batch_save -> Métodos: POST, OPTIONS
Rota: /backend/populate/popular-banco -> Métodos: POST, OPTIONS
 */