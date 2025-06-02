import React, { useState, useEffect } from "react";
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
import EmailIcon from "@mui/icons-material/Email";
import Home from "@mui/icons-material/Home";
import SettingsIcon from "@mui/icons-material/Settings";
import Logout from "@mui/icons-material/Logout";
import MenuIcon from "@mui/icons-material/Menu";
import ArrowBack from "@mui/icons-material/ArrowBack";
import BallotRounded from "@mui/icons-material/BallotRounded";
import DoctorIconComponent from "../components/DoctorIconComponent";
import { useNavigate } from "react-router-dom";
import { auth } from "../utils/auth";
import { DashboardRounded, Engineering, LocalHospital } from "@mui/icons-material";
import TerapeutaIconComponent from "../components/TerapeutaIconComponent";
import ProntuarioIconComponent from "../components/ProntuarioIconComponent";
const Root = styled(Box)(() => ({
    display: "flex",
    flexDirection: "row",
    height: "100vh",
    background: "#f0f2f5",
    padding: "12px 12px 64px 0",
    gap: "24px", // Espaço entre Sidebar e Content
    boxSizing: "border-box",
    "@media (max-width: 600px)": {
        flexDirection: "column",
        padding: 0,
        gap: 0,
        background: "#fff",
        height: "100vh",
    },
}));

const Sidebar = styled(Box)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    width: "170px",
    padding: "24px", // igual ao Content
    display: "flex",
    flexDirection: "column",
    borderRadius: "0 16px 16px 0",
    boxShadow: "0 8px 8px 0 rgba(0,0,0,0.5)",
    height: "100%",
    "@media (max-width: 600px)": {
        display: "none",
        height: "auto",
        padding: "16px",
    },
}));

const Content = styled(Box)(() => ({
    flexGrow: 1,
    padding: "24px", // igual ao Sidebar
    backgroundColor: "white",
    borderRadius: "16px 0 0 16px",
    boxShadow: "0 8px 8px 0 rgba(0,0,0,0.5)",
    height: "100%",
    overflow: "auto",
    // Removido marginLeft
    "@media (max-width: 600px)": {
        borderRadius: 0,
        boxShadow: "none",
        height: "auto",
        padding: "16px",
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

interface AdminLayoutProps {
    children: React.ReactNode;
    isProfissional?: boolean;
}

export default function AdminLayout({ children }: AdminLayoutProps) {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isProfissional, setIsProfissional] = useState(false);
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
        localStorage.removeItem("@App:token");
        localStorage.removeItem("@App:user");
        localStorage.removeItem("@App:profile");
        navigate("/login");
    };

    useEffect(() => {
        const userData = auth.getUserData();
        const isProfissional = userData?.role === "profissional_saude";
        setIsProfissional(isProfissional);
    }, []);

    const mobileMenuContent = (
        <Box sx={{ padding: "16px", backgroundColor: theme.palette.primary.main, color: "white" }}>
            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
                <img src={logo} alt="Logo" style={{ width: "40px", height: "auto", marginRight: "8px" }} />
                <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={toggleMobileMenu(false)}>
                    <ArrowBack />
                </IconButton>
            </Box>
            <Divider />
            <Box sx={{ display: "flex", flexDirection: "column", gap: "16px", marginTop: "16px" }}>
                <Box sx={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/")}>
                        <Home />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Home
                        </Typography>
                    </IconButton>
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/paciente")}>
                        <PeopleAlt />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Pacientes
                        </Typography>
                    </IconButton>
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/profissional")}>
                        <DoctorIconComponent />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Terapeutas
                        </Typography>
                    </IconButton>

                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/medicos")}>

                        <TerapeutaIconComponent />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Medicos
                        </Typography>
                    </IconButton>
                        

                    {!isProfissional && (
                        <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/colaborador")}>
                            <Engineering />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Colaboradores
                            </Typography>
                        </IconButton>)
}
                    {
                        /*
                        
                        
                            <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/dashboard")}>
                                <DashboardRounded />
                                <Typography variant="body2" sx={{ ml: 1 }}>
                                    Dashboard
                                </Typography>
                            </IconButton>
                            
                        
                        */
                    }
                    
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/questionario")}>
                        <BallotRounded />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Questionário
                        </Typography>
                    </IconButton>
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/baterias")}>
                        <PsycologyAltIcon />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Baterias
                        </Typography>
                    </IconButton>



                    
                    
                    {/*
                    
                    
                    
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/notificacoes")}>
                        <Badge badgeContent={1} color="error">
                            <EmailIcon />
                        </Badge>
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Notificações
                        </Typography>
                    </IconButton>
                    */

                    }

                          <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/unidade-saude")}>
                        <LocalHospital />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Unidades de Saúde
                        </Typography>
                    </IconButton>

                    {!isProfissional && (
                        <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/configuracoes")}>
                            <SettingsIcon />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Configurações
                            </Typography>
                        </IconButton>
                    )}

              

                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={handleLogout}>
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
                        <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={toggleMobileMenu(true)}>
                            <MenuIcon />
                        </IconButton>
                    </MobileHeader>
                    <Drawer
                        anchor="top"
                        open={isMobileMenuOpen}
                        onClose={toggleMobileMenu(false)}
                        slotProps={{paper: { sx: { backgroundColor: theme.palette.primary.main, color: "white" } }}}
                    >
                        {mobileMenuContent}
                    </Drawer>
                    <Content>{children}</Content>
                </>
            ) : (
                <>
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
                        

                        <ButtonContent onClick={navigateTo("/paciente")}>
                            <PeopleAlt />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Pacientes
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        <ButtonContent onClick={navigateTo("/profissional")}>
                            <TerapeutaIconComponent />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Terapeutas
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        <ButtonContent onClick={navigateTo("/medico")}>
                            <DoctorIconComponent />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Médicos
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        {!isProfissional && (
                            <>
                                <ButtonContent onClick={navigateTo("/colaborador")}>
                                    <Engineering />
                                    <Typography variant="body2" sx={{ ml: 1 }}>
                                        Colaborador
                                    </Typography>
                                </ButtonContent>
                                <Divider sx={{ marginTop: 1.5 }} flexItem />
                            </>
                        )}
                   
                        <ButtonContent onClick={navigateTo("/questionario")}>
                            <BallotRounded />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Questionário
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        <ButtonContent onClick={navigateTo("/baterias")}>
                            <ProntuarioIconComponent fillColor="inherit"/>
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Avaliações
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />

                        
                        {/*
                        <ButtonContent onClick={navigateTo("/notificacoes")}>
                            <Badge badgeContent={1} color="error">
                                <EmailIcon />
                            </Badge>
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Notificações
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        */}
                        <ButtonContent onClick={navigateTo("/unidade-saude")}>
                            <LocalHospital />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Unidades de Saúde
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        {!isProfissional && (
                            <>
                                <ButtonContent onClick={navigateTo("/configuracoes")}>
                                    <SettingsIcon />
                                    <Typography variant="body2" sx={{ ml: 1 }}>
                                        Configurações
                                    </Typography>
                                </ButtonContent>
                                <Divider sx={{ marginTop: 1.5 }} flexItem />
                            </>
                        )}
                        <ButtonContent onClick={handleLogout} sx={{ marginTop: "auto", marginBottom: 4 }}>
                            <Logout />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Sair
                            </Typography>
                        </ButtonContent>
                    </Sidebar>
                    <Content>{children}</Content>
                </>
            )}
        </Root>
    );
}