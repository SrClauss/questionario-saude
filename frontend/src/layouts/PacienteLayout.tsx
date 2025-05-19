import React, { useState } from "react";
import {
    Box,
    styled,
    IconButton,
    Typography,
    Divider,
    useMediaQuery,
    useTheme,
    Drawer
} from "@mui/material";
import logo from "../assets/img/log-laranja-minified.png";
import Home from "@mui/icons-material/Home";
import Logout from "@mui/icons-material/Logout";
import MenuIcon from "@mui/icons-material/Menu";
import ArrowBack from "@mui/icons-material/ArrowBack";
import PsychologyAltIcon from "@mui/icons-material/PsychologyAlt";
import PeopleAlt from "@mui/icons-material/PeopleAlt";
import { useNavigate } from "react-router-dom";

const Root = styled(Box)(() => ({
    display: "flex",
    flexDirection: "row",
    height: "100vh",
    background: "#f0f2f5",
    padding: "12px 12px 64px 0",
    gap: "24px",
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
    padding: "24px",
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
    padding: "24px",
    
    backgroundColor: "white",
    borderRadius: "16px 0 0 16px",
    boxShadow: "0 8px 8px 0 rgba(0,0,0,0.5)",
    height: "100%",
    overflow: "auto",
    "@media (max-width: 600px)": {
        borderRadius: 0,
        boxShadow: "none",
        marginTop: "32px",
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

interface PacienteLayoutProps {
    children: React.ReactNode;
}

export default function PacienteLayout({ children }: PacienteLayoutProps) {
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
        localStorage.removeItem("@App:token");
        localStorage.removeItem("@App:profile");
        localStorage.removeItem("@App:user");
        navigate("/login");
      };
    const mobileMenuContent = (
        <Box sx={{ padding: "16px", backgroundColor: theme.palette.primary.main, color: "white", justifyContent: "center", marginTop:"64px"}}>
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
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/paciente-baterias-list")}>
                        <PsychologyAltIcon />
                        
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Baterias Paciente
                        </Typography>
                    </IconButton>
                    <IconButton sx={{ justifyContent: 'start' }} color="inherit" onClick={navigateTo("/staff")}>
                        <PeopleAlt />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                            Staff
                        </Typography>
                    </IconButton>
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
                        <ButtonContent onClick={navigateTo("/paciente-baterias-list")}>
                            <PsychologyAltIcon />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Baterias
                            </Typography>
                        </ButtonContent>
                        <Divider sx={{ marginTop: 1.5 }} flexItem />
                        <ButtonContent onClick={navigateTo("/staff")}>
                            <PeopleAlt />
                            <Typography variant="body2" sx={{ ml: 1 }}>
                                Staff
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
                    <Content>{children}</Content>
                </>
            )}
        </Root>
    );
}