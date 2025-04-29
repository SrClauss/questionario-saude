import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Divider, Container, Avatar } from '@mui/material';
import { auth } from '../utils/auth';

const PacienteHomeScreen: React.FC = () => {
  const userId = auth.getUserData()?.id; // Obtém o ID do usuário do auth

  return (
    <Container maxWidth="lg" sx={{ padding: 2, height: '90vh' }}>
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
      </Box>
    </Container>
  );
};

export default PacienteHomeScreen;