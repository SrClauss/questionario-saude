import React, { useState } from "react";
import {
    Box,
    styled,
    IconButton,
    Typography,
    Divider,
    Badge,
    useMediaQuery,
    useTheme,
    Drawer
} from "@mui/material";
import logo from "../assets/img/log-laranja-minified.png";
import PeopleAlt from "@mui/icons-material/PeopleAlt";
import PsycologyAltIcon from "@mui/icons-material/PsychologyAlt";
import DashboardRounded from "@mui/icons-material/DashboardRounded";
import EmailIcon from "@mui/icons-material/Email";
import Home from "@mui/icons-material/Home";
import SettingsIcon from "@mui/icons-material/Settings";
import Logout from "@mui/icons-material/Logout";
import MenuIcon from "@mui/icons-material/Menu";
import ArrowBack from "@mui/icons-material/ArrowBack";
import BallotRounded from "@mui/icons-material/BallotRounded";
import { Engineering } from "@mui/icons-material";
import DoctorIconComponent from "../components/DoctorIconComponent";
import { useNavigate } from "react-router-dom";
import { auth } from "../utils/auth";

const Root = styled(Box)(() => ({
    display: "flex",
    flexDirection: "row",
    minHeight: "100vh",
    "@media (max-width: 600px)": {
        flexDirection: "column",
    },
}));

const Sidebar = styled(Box)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    width: "150px",
    padding: "16px",
    display: "flex",
    flexDirection: "column",
    "@media (max-width: 600px)": {
        display: "none",
    },
}));

const MobileHeader = styled(Box)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    padding: "8px 16px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
}));

const Content = styled(Box)(({ theme }) => ({
    flexGrow: 1,
    padding: "16px",
    backgroundColor: "white",
    marginTop: "50px",
    "@media (min-width: 600px)": {
        marginTop: 0,
    },
}));

const ButtonContent = styled(Box)(({ theme }) => ({
    display: "flex",
    justifyContent: "left",
    alignItems: "center",
    marginTop: "15px",
    color: "white",
    "&:hover": {
        color: theme.palette.primary.dark,
        borderRadius: "8px",
        cursor: "pointer",
    },
}));

export default function AdminLayout({ children }: { children: React.ReactNode }) {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
    const navigate = useNavigate();

    const navigateTo = (path: string) => () => {
        navigate(path);
        setIsMobileMenuOpen(false);
    };

    const toggleMobileMenu = (open: boolean) => () => {
        setIsMobileMenuOpen(open);
    };

    const handleLogout = () => {
        // Remova os tokens e demais dados de autorização
        localStorage.removeItem("@App:token");
        localStorage.removeItem("@App:user");
        localStorage.removeItem("@App:profile");
        navigate("/login");
    };

    const mobileMenuContent = (
        <Box sx={{ padding: "16px", backgroundColor: theme.palette.primary.main, color: "white" }}>
            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
                <img src={logo} alt="Logo" style={{ width: "40px", height: "auto", marginRight: "8px" }} />
                <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={toggleMobileMenu(false)}>
                    <ArrowBack />
                </IconButton>
            </Box>
            <Divider />
            <Box sx={{ display: "flex", flexDirection: "column", gap: "16px", marginTop: "16px" }}>
                {/* Divisão em duas colunas com Divider vertical */}
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    {/* Coluna 1 */}
                    <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: "16px" }}>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/")}>
                            <Home />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Home
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/paciente")}>
                            <PeopleAlt />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Pacientes
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/profissional")}>
                            <DoctorIconComponent />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Profissionais
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/colaborador")}>
                            <Engineering />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Colaboradores
                            </Typography>
                        </IconButton>
                    </Box>

                    {/* Divider vertical */}
                    <Divider orientation="vertical" flexItem sx={{ mx: 2, backgroundColor: "white" }} />

                    {/* Coluna 2 */}
                    <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: "16px" }}>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/dashboard")}>
                            <DashboardRounded />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Dashboard
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/questionario")}>
                            <BallotRounded />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Questionário
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/testes")}>
                            <PsycologyAltIcon />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Testes
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/notificacoes")}>
                            <Badge badgeContent={1} color="error">
                                <EmailIcon />
                            </Badge>
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Notificações
                            </Typography>
                        </IconButton>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={navigateTo("/configuracoes")}>
                            <SettingsIcon />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Configurações
                            </Typography>
                        </IconButton>
                    </Box>
                </Box>
                <Divider />
                {/* Botão de Sair */}
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: "auto" }}>
                    <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={handleLogout}>
                        <Logout />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Sair
                        </Typography>
                    </IconButton>
                </Box>
            </Box>
        </Box>
    );

    return (
        <Root>
            {isMobile ? (
                <>
                    <MobileHeader>
                        <Box sx={{ display: "flex", alignItems: "center" }}>
                            <img src={logo} alt="Logo" style={{ width: "40px", height: "auto", marginRight: "8px" }} />
                        </Box>
                        <IconButton sx={{justifyContent: 'start'}} color="inherit" onClick={toggleMobileMenu(true)}>
                            <MenuIcon />
                        </IconButton>
                    </MobileHeader>
                    <Drawer
                        anchor="top"
                        open={isMobileMenuOpen}
                        onClose={toggleMobileMenu(false)}
                        PaperProps={{
                            sx: { backgroundColor: theme.palette.primary.main, color: "white" },
                        }}
                    >
                        {mobileMenuContent}
                    </Drawer>
                </>
            ) : (
                <Sidebar>
                    {/* Sidebar no Desktop */}
                    <Box sx={{ display: "flex", justifyContent: "center", marginBottom: 5 }}>
                        <img src={logo} alt="Logo" style={{ width: "100px", height: "auto", margin: "10px" }} />
                    </Box>
                    <ButtonContent onClick={navigateTo("/")}>
                        <Home />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Home
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/dashboard")}>
                        <DashboardRounded />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Dashboard
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/paciente")}>
                        <PeopleAlt />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Pacientes
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/profissional")}>
                        <DoctorIconComponent />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Profissionais
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/colaborador")}>
                        <Engineering />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Colaborador
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/questionario")}>
                        <BallotRounded />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Questionário
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/testes")}>
                        <PsycologyAltIcon />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Testes
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/notificacoes")}>
                        <Badge badgeContent={1} color="error">
                            <EmailIcon />
                        </Badge>
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Notificações
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={navigateTo("/configuracoes")}>
                        <SettingsIcon />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Configurações
                        </Typography>
                    </ButtonContent>
                    <Divider sx={{ marginTop: 1.5 }} flexItem />
                    <ButtonContent onClick={handleLogout} sx={{ marginTop: "auto", marginBottom: 4 }}>
                        <Logout />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Sair
                        </Typography>
                    </ButtonContent>
                </Sidebar>
            )}
            <Content>{children}</Content>
        </Root>
    );
}