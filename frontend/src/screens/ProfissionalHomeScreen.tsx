import React, { useEffect, useRef, useState } from "react";
import { 
  Avatar, Box, Tooltip, Typography, useTheme, 
  Paper, LinearProgress
} from "@mui/material";
import AdminLayout from "../layouts/AdminLayout";
import { ProfissionalSaude } from "../types/user";
import { auth } from "../utils/auth";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, 
  ResponsiveContainer, LineChart, Line, Legend
} from 'recharts';
import { 
  Person, AssignmentTurnedIn, EventAvailable, TrendingUp,
  CalendarMonth
} from "@mui/icons-material";
import InfoBox from "../components/InfoBox";

export default function ProfissionalHomeScreen() {
  const theme = useTheme();
  const profile = auth.getProfile();
  const [dashboardData, setDashboardData] = useState<any>({});
  const [userImage, setUserImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const profissional: ProfissionalSaude | null =
    profile && "registro_profissional" in profile ? (profile as ProfissionalSaude) : null;

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchSetImage = async (userId: string, file: File): Promise<string> => {
    const token = localStorage.getItem("@App:token");
    if (!token) {
      throw new Error("Token não disponível");
    }
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const url = `${baseUrl}/user/${userId}/upload`;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Erro ao fazer upload da imagem: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Upload realizado com sucesso:", data);

    const newImageUrl = `${baseUrl}/user/${userId}/image`;
    return newImageUrl;
  };

  const fetchImage = async () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    const url = `${baseUrl}/user/${profissional?.user_id}/image`;
    if (!token) return;

    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setUserImage(imageUrl);
      } else {
        console.error("Error fetching image:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching image:", error);
    }
  };

  const fetchDashboardData = async (profissionalId: string) => {
    setIsLoading(true);
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    const url = `${baseUrl}/baterias_testes/dashboard_profissional/${profissionalId}`;
    if (!token) return;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
        console.log("Dashboard data:", data);
      } else {
        console.error("Error fetching dashboard data:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && profissional?.user_id) {
      try {
        const newImageUrl = await fetchSetImage(profissional.user_id, file);
        setUserImage(newImageUrl);
      } catch (error) {
        console.error("Erro ao atualizar imagem:", error);
      }
    }
  };

  useEffect(() => {
    fetchImage();
    if (profissional?.id) {
      fetchDashboardData(profissional.id);
    }
  }, []);

  return (
    <AdminLayout>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#f5f5f5",
          padding: 3,
          minHeight: "100vh",
        }}
      >
        {isLoading && <LinearProgress />}
        
        <Paper 
          elevation={2} 
          sx={{ 
            p: 3, 
            mb: 3, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 2,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
            <Tooltip title="Clique para alterar a imagem">
              <Avatar
                alt={profissional?.nome}
                src={userImage || undefined}
                onClick={handleAvatarClick}
                sx={{
                  width: 70,
                  height: 70,
                  cursor: "pointer",
                  borderColor: theme.palette.primary.main,
                  borderWidth: 3,
                  borderStyle: "solid",
                  mr: 2
                }}
              >
                {profissional?.nome ? profissional.nome.charAt(0) : ""}
              </Avatar>
            </Tooltip>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ m: 0 }}>
                Dashboard Profissional
              </Typography>
              <Typography variant="subtitle1" color="textSecondary">
                Olá, {profissional?.nome}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', flex: 1, justifyContent: 'flex-end' }}>
            <CalendarMonth sx={{ mr: 1 }} />
            <Typography>
              {new Date().toLocaleDateString('pt-BR', { 
                day: '2-digit', 
                month: 'long', 
                year: 'numeric' 
              })}
            </Typography>
          </Box>
        </Paper>

        {/* InfoBoxes */}
        <Box
          sx={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 2,
            mb: 4,
          }}
        >
          <InfoBox
            backgroundColor={theme.palette.primary.main}
            value={dashboardData.numero_total_baterias || 0}
            caption="Total de Baterias"
            icon={<AssignmentTurnedIn htmlColor="white" sx={{ fontSize: 48 }} />}
          />
          <InfoBox
            backgroundColor={theme.palette.error.main}
            value={dashboardData.numero_total_baterias_abertas || 0}
            caption="Baterias Abertas"
            icon={<EventAvailable htmlColor="white" sx={{ fontSize: 48 }} />}
          />
          <InfoBox
            backgroundColor={theme.palette.warning.dark}
            value={dashboardData.numero_total_baterias_por_profissional || 0}
            caption="Baterias por Profissional"
            icon={<TrendingUp htmlColor="white" sx={{ fontSize: 48 }} />}
          />
          <InfoBox
            backgroundColor={theme.palette.success.main}
            value={dashboardData.numero_total_baterias_abertas_por_profissional || 0}
            caption="Abertas por Profissional"
            icon={<Person htmlColor="white" sx={{ fontSize: 48 }} />}
          />
        </Box>

        {/* Gráfico de evolução de pacientes */}
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
            mb: 4,
          }}
        >
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Evolução de Pacientes Conectados (Últimos 6 Meses)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={dashboardData.evolucao_pacientes || []}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mes" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="qtd_pacientes"
                  stroke={theme.palette.primary.main}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Box>

        {/* Gráfico de comparação de baterias pendentes e completas */}
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
            mb: 4,
          }}
        >
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Comparação de Baterias Pendentes e Completas (Este Mês)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={[
                  {
                    name: "Baterias",
                    Completas: dashboardData.numero_baterias_ultimo_mes - dashboardData.numero_baterias_abertas_ultimo_mes || 0,
                    Pendentes: dashboardData.numero_baterias_abertas_ultimo_mes || 0,
                  },
                ]}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Bar dataKey="Completas" fill={theme.palette.success.main} />
                <Bar dataKey="Pendentes" fill={theme.palette.error.main} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Box>

        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </Box>
    </AdminLayout>
  );
}