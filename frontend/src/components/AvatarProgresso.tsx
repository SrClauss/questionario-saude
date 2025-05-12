import React from 'react';
import { Box, Typography, CircularProgress, Avatar } from '@mui/material';
import PieChartResultados from './PieChartResultados';
import { BateriaTestesState } from '../screens/PacienteHomeScreen';

interface AvatarProgressoProps {
  perfilDeSaudeBateria: BateriaTestesState | undefined;
  loadingImage: boolean;
  userImage: string | null;
  pacienteNome: string | undefined;
}

const AvatarProgresso: React.FC<AvatarProgressoProps> = ({
  perfilDeSaudeBateria,
  loadingImage,
  userImage,
  pacienteNome,
}) => {
  return (
    <Box sx={{ position: 'relative', width: '300px', height: '300px' }}>
      {perfilDeSaudeBateria ? (
        <PieChartResultados
          respostas={perfilDeSaudeBateria.bateria.respostas || []}
          qtd_perguntas={perfilDeSaudeBateria.qtd_perguntas}
        />
      ) : (
        <Typography variant="body1">
          Nenhuma bateria encontrada para o questionário "Perfil de Saúde".
        </Typography>
      )}
      {loadingImage ? (
        <CircularProgress sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 2,
        }} />
      ) : userImage ? (
        <Avatar
          src={userImage}
          sx={{
            position: 'absolute',
            top: '33.5%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 110,
            height: 110,
            zIndex: 2,
          }}
        />
      ) : (
        <Avatar sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 100,
          height: 100,
          zIndex: 2,
        }}>
          {pacienteNome ? pacienteNome[0] : 'U'}
        </Avatar>
      )}
    </Box>
  );
};

export default AvatarProgresso;