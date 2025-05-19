import React from 'react';
import { Box, Typography, CircularProgress, Avatar, Tooltip, Snackbar, Alert } from '@mui/material';
import PieChartResultados from './PieChartResultados';
import { BateriaTestesState } from '../screens/PacienteHomeScreen';
import { auth } from '../utils/auth';

interface AvatarProgressoProps {
  perfilDeSaudeBateria: BateriaTestesState | undefined;
  loadingImage: boolean;
  userImage: string | null;
  pacienteNome: string | undefined;
  onReload: () => void;
}

const ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'];

const AvatarProgresso: React.FC<AvatarProgressoProps> = ({
  perfilDeSaudeBateria,
  loadingImage,
  userImage,
  pacienteNome,
  onReload,
}) => {
  const [snackbar, setSnackbar] = React.useState<{ open: boolean, message: string, severity: "success" | "error" | "info" }>({ open: false, message: "", severity: "info" });

  const handleSendImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const user = auth.getUser();

    if (user && e.target.files && e.target.files[0]) {
      const file = e.target.files[0];

      // Verificação do tamanho do arquivo (1MB)
      if (file.size > 1024 * 1024) {
        setSnackbar({ open: true, message: "A imagem não pode ser maior que 1MB.", severity: "error" });
        return;
      }

      // Verificação da extensão do arquivo
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (!ext || !ALLOWED_EXTENSIONS.includes(ext)) {
        setSnackbar({ open: true, message: "Formato de imagem não suportado. Aceitos: png, jpg, jpeg, gif, bmp, webp.", severity: "error" });
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/user/${user.id}/upload`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${user.token}`,
            },
            body: formData,
          });

        if (response.ok) {
          setSnackbar({ open: true, message: 'Imagem enviada com sucesso!', severity: "success" });
          onReload();
        } else {
          setSnackbar({ open: true, message: `Erro ao enviar imagem: ${response.statusText}`, severity: "error" });
        }
      }
      catch (error) {
        setSnackbar({ open: true, message: `Erro ao enviar imagem: ${error}`, severity: "error" });
      }
    }
  };

  const inputRef = React.useRef<HTMLInputElement | null>(null);

  return (
    <Box sx={{ position: 'relative', width: '300px', height: '300px' }}>
      {perfilDeSaudeBateria ? (
        <PieChartResultados
          respostas={perfilDeSaudeBateria.bateria.respostas || {}}
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
        <Tooltip title="Clique para mudar a foto de perfil">
          <Avatar
            onClick={() => inputRef.current?.click()}
            src={userImage}
            sx={{
              cursor: 'pointer',
              position: 'absolute',
              top: '33.5%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: 110,
              height: 110,
              zIndex: 2,
            }}
          />
        </Tooltip>
      ) : (
        <Tooltip title="Clique para inserir uma foto de perfil">
          <Avatar
            onClick={() => inputRef.current?.click()}
            sx={{
              position: 'absolute',
              top: '33.4%',
              left: '50%',
              cursor: 'pointer',
              transform: 'translate(-50%, -50%)',
              width: 110,
              height: 110,
              zIndex: 2,
            }}>
            {pacienteNome ? pacienteNome[0] : 'U'}
          </Avatar>
        </Tooltip>
      )}
      <input
        type="file"
        accept="image/*"
        ref={inputRef}
        style={{ display: 'none' }}
        id="avatar-upload"
        onChange={handleSendImage}
      />

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AvatarProgresso;