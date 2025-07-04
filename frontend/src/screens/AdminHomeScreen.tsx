import { useEffect, useState } from "react";
import {
    Box,
    Typography,
    Paper,
    LinearProgress,
    useTheme,
} from "@mui/material";
import AdminLayout from "../layouts/AdminLayout";
import InfoBox from "../components/InfoBox";
import {
    Person,
    AssignmentTurnedIn,
    CalendarMonth,
    PeopleAlt,
    Engineering,
    BallotRounded,
    Healing,
    FactCheckRounded,
    Warning,
    Group,
    MedicalInformationOutlined,
    PsychologyAlt,
} from "@mui/icons-material";
import StylizedTitle from "../components/StylizedTitle";

export default function AdminHomeScreen() {
    const theme = useTheme();
    const [metrics, setMetrics] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchMetrics = async () => {
            setIsLoading(true);
            const baseUrl = import.meta.env.VITE_BACKEND_URL;
            const token = localStorage.getItem("@App:token");
            const url = `${baseUrl}/user/admin_metrics`;

            if (!token) {
                console.error("Token não encontrado.");
                setIsLoading(false);
                return;
            }

            try {
                const response = await fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setMetrics(data);
                } else {
                    console.error("Erro ao buscar métricas:", response.statusText);
                    setMetrics(null);
                }
            } catch (error) {
                console.error("Erro ao buscar métricas:", error);
                setMetrics(null);
            } finally {
                setIsLoading(false);
            }
        };

        fetchMetrics();
    }, []);

    if (isLoading) {
        return (
            <AdminLayout>
                <LinearProgress />
            </AdminLayout>
        );
    }

    if (!metrics) {
        return (
            <AdminLayout>
                <Typography variant="h6" color="error" sx={{ textAlign: 'center', mt: 4 }}>
                    Não foi possível carregar as métricas.
                </Typography>
            </AdminLayout>
        );
    }

    return (
        <AdminLayout>
            <Box sx={{ p: 3 }}>
                <StylizedTitle title="Dashboard" />

                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, justifyContent: 'center' }}>
                    <InfoBox backgroundColor={theme.palette.info.main} value={metrics.numero_usuarios || 0} caption="Total de Usuários" icon={<Group htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.primary.main} value={metrics.numero_pacientes || 0} caption="Pacientes" icon={<PeopleAlt htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.secondary.main} value={metrics.numero_profissionais_saude || 0} caption="Terapeutas" icon={<Person htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.success.main} value={metrics.numero_medicos || 0} caption="Médicos" icon={<Healing htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.warning.dark} value={metrics.numero_colaboradores || 0} caption="Colaboradores" icon={<Engineering htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.error.main} value={metrics.numero_usuarios_sem_autenticacao || 0} caption="Usuários Pendentes" icon={<Warning htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.info.light} value={metrics.pacientes_ultimos_30_dias || 0} caption="Pacientes (30d)" icon={<CalendarMonth htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.primary.dark} value={metrics.questionarios_cadastrados || 0} caption="Questionários" icon={<BallotRounded htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.secondary.dark} value={metrics.avaliacoes_cadastrados || 0} caption="Avaliações" icon={<AssignmentTurnedIn htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.success.dark} value={metrics.baterias_aplicadas_total || 0} caption="Baterias (Total)" icon={<PsychologyAlt htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.warning.dark} value={metrics.baterias_ultimos_30_dias || 0} caption="Baterias (30d)" icon={<CalendarMonth htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.error.light} value={metrics.baterias_respondidas_ultimos_30_dias || 0} caption="Baterias Resp. (30d)" icon={<FactCheckRounded htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.info.dark} value={metrics.laudos_emitidos || 0} caption="Laudos (Total)" icon={<MedicalInformationOutlined htmlColor="white" sx={{ fontSize: 48 }} />} />
                    <InfoBox backgroundColor={theme.palette.grey[700]} value={metrics.laudos_emitidos_ultimos_30_dias || 0} caption="Laudos (30d)" icon={<CalendarMonth htmlColor="white" sx={{ fontSize: 48 }} />} />
                </Box>
            </Box>
        </AdminLayout>
    );
}
