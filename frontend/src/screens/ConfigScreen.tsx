import {
    Tabs,
    Box,
    Tab,

    Snackbar,
    Container,
    Table,
    TableHead,
    TableRow,
    TableCell,
    IconButton,
    TableContainer,
    Tooltip,
    Paper,
    TableBody,
    Pagination,
    Alert,
    Fab,
} from "@mui/material";

import { AddAdminModalProps } from "../modals/AddAdminModal";
import { useEffect, useState } from "react";
import AdminLayout from "../layouts/AdminLayout";
import StylizedTitle from "../components/StylizedTitle";
import { auth } from "../utils/auth";
import SearchBar from "../components/SearchBar";
import { Add, Delete, Password } from "@mui/icons-material";
import ChangePasswordModal from "../modals/ChangePasswordModal";
import { User } from "../types/user";
import DeleteModal from "../modals/DeleteDialog";
import AddAdminModal from "../modals/AddAdminModal";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

interface snackBarProps {
    open: boolean;
    message: string;
    severity: "success" | "error";
}
function CustomTabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;


    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
        </div>
    );
}
function a11yProps(index: number) {
    return {
        id: `simple-tab-${index}`,
        "aria-controls": `simple-tabpanel-${index}`,
    };
}

export default function ConfigScreen() {
    const [tab, setTab] = useState(0);

    const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
        setTab(newValue);
    };

    return (
        <AdminLayout>

            <Box sx={{ marginTop: { xs: 2, sm: 2, md: 0 }, paddingX: { xs: 1, sm: 2 } }}>
                <StylizedTitle title="Configurações" />
                <Box sx={{ width: "100%", display: "flex", justifyContent: "center", flexDirection: "column" }}>
                    <Box
                        sx={{
                            mt: 2,
                            display: "flex",
                            justifyContent: "center",
                            width: "100%",
                        }}
                    >
                        <Tabs
                            value={tab}
                            onChange={handleChange}
                            variant="scrollable"
                            scrollButtons="auto"
                            allowScrollButtonsMobile
                        >
                            <Tab label="Trocar Senha" {...a11yProps(0)} />
                            <Tab label="Adcionar Admin" {...a11yProps(1)} />
                            <Tab label="Arquivar Laudos" {...a11yProps(2)} />
                        </Tabs>

                    </Box>
                    <CustomTabPanel value={tab} index={0}>
                        <TabTrocarSenha />
                    </CustomTabPanel>

                    <CustomTabPanel value={tab} index={1}>
                        <TabAdmins />
                    </CustomTabPanel>

                    <CustomTabPanel value={tab} index={2}></CustomTabPanel>
                </Box>
            </Box>
        </AdminLayout>

    );
}

interface UserPass {
    id: string;
    nome: string;
    role: string;
}
interface PasswordModalProps {
    open: boolean;
    onClose: () => void;
    userId: string | null;
    userName?: string;
}
function TabTrocarSenha() {
    const [users, setUsers] = useState<UserPass[]>([]);
    const [passwordModalProps, setPasswordModalProps] = useState<PasswordModalProps>({
        open: false,
        onClose: () => { },
        userId: '',
        userName: ''
    })
    const [snackBarProps, setSnackBarProps] = useState<snackBarProps>({
        open: false,
        message: "",
        severity: "success",
    })
    const fetchSearchUser = async (critery: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/user/find_user_by_name/${critery}`;
        try {

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            const data = await response.json();


            if (data.length === 0) {
                setSnackBarProps({ ...snackBarProps, open: true, message: "Usuário não encontrado", severity: "error" });
            } else {
                setSnackBarProps({ ...snackBarProps, open: false });
            }
            setUsers(data);
        }
        catch (error) {
            setSnackBarProps({ ...snackBarProps, open: true, message: "Erro ao buscar usuário", severity: "error" });
        }
    };

    return (
        <Container>
            <SearchBar onSearch={fetchSearchUser} />
            <TableContainer component={Paper} sx={{ mt: 2, overflowX: 'auto' }}>
                <Table sx={{ minWidth: { xs: 'auto', sm: 650 } }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Id</TableCell>
                            <TableCell>Nome</TableCell>
                            <TableCell>Role</TableCell>
                            <TableCell align="center">Ações</TableCell>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {users.map((user) => (
                            <TableRow key={user.id}>
                                <TableCell component="th" scope="row">{user.id}</TableCell>
                                <TableCell>{user.nome}</TableCell>
                                <TableCell>{user.role}</TableCell>
                                <TableCell align="center">
                                    <Tooltip title="Trocar Senha">
                                        <IconButton onClick={() => setPasswordModalProps({
                                            open: true,
                                            onClose: () => setPasswordModalProps({ ...passwordModalProps, open: false }),
                                            userId: user.id,
                                            userName: user.nome
                                        })}>
                                            <Password />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <ChangePasswordModal {...passwordModalProps} />
        </Container>
    );
}

function TabAdmins() {
    const [admins, setAdmins] = useState<User[]>([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [showPagination, setShowPagination] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [adminIdToDelete, setAdminIdToDelete] = useState('');
    const [snackBarProps, setSnackBarProps] = useState<snackBarProps>({
        open: false,
        message: "",
        severity: "success",
    })
    const [adminModalProps, setAdminModalProps] = useState<AddAdminModalProps>(
        {
            open: false,
            onClose: () => { },
            onAdminAdded: () => { }
        }
    )
    const fetchAllAdmins = async (page: number) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/user/all_admins/${page}/10`;
        try{

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setAdmins(data);
            setTotalPages(data.totalPages);
            if (data.totalPages > 1) {
                setShowPagination(true);
            }
            
        }

        catch(error){
            setSnackBarProps({ ...snackBarProps, open: true, message: "Erro ao buscar admins", severity: "error" });
        }
    }

    const fetchDeleteAdmin = async (id: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        const url = `${baseUrl}/user/delete_admin/${id}`;

        try{


            const response = await fetch(url, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            const data = await response.json();
           
            if (response.status === 400){
                setSnackBarProps({ ...snackBarProps, open: true, message: data.error, severity: "error" });
            }
            else{
                setSnackBarProps({ ...snackBarProps, open: true, message: "Admin deletado com sucesso", severity: "success" });
                fetchAllAdmins(page);
            }
            
        }

        catch(error){
            setSnackBarProps({ ...snackBarProps, open: true, message: "Erro ao deletar admin " + error, severity: "error" });
            
        }
        
        
    }

    useEffect(() => {
        fetchAllAdmins(page);
    }, []);


    return (
        <Container>
            <TableContainer component={Paper} sx={{ mt: 2, overflowX: 'auto' }}>
                <Tooltip title="Adicionar Admin">
                <Fab
                    onClick={() => setAdminModalProps({
                        open: true,
                        onClose: () => setAdminModalProps({ ...adminModalProps, open: false }),
                        onAdminAdded: () => fetchAllAdmins(page)
                    })}

                    sx={{ position: "fixed", right: 64, bottom: 64 }}

                    color="primary"
                    aria-label="add"
                >
                    <Add/>
                   
                </Fab>
                </Tooltip>
                <Table sx={{ minWidth: { xs: 'auto', sm: 650 } }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Id</TableCell>
                            <TableCell>email</TableCell>
                            <TableCell align="center">Ações</TableCell>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {admins.map((admin) => (
                            <TableRow key={admin.id}>
                                <TableCell component="th" scope="row">{admin.id}</TableCell>
                                <TableCell>{admin.email}</TableCell>
                                <TableCell align="center">
                                    <Tooltip title="Excluir">
                                        <IconButton onClick={() => {setShowDeleteModal(true); setAdminIdToDelete(admin.id)}}>
                                            <Delete />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>

                </Table>
            </TableContainer>
            {showPagination && <Pagination count={totalPages} page={page} onChange={(_e, page) => {setPage(page); fetchAllAdmins(page)}} />}
            <DeleteModal open={showDeleteModal} onClose={() => setShowDeleteModal(false)} onConfirm={() => {fetchDeleteAdmin(adminIdToDelete); setShowDeleteModal(false)}} />    
             <AddAdminModal
                {...adminModalProps}
            />
            <Snackbar open={snackBarProps.open} autoHideDuration={6000} onClose={() => setSnackBarProps({ ...snackBarProps, open: false })} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
                <Alert severity={snackBarProps.severity} onClose={() => setSnackBarProps({ ...snackBarProps, open: false })}  sx={{ width: '100%' }}>
                    {snackBarProps.message}
                </Alert>
            </Snackbar>
        </Container>
    );




}