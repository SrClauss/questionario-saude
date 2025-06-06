import SearchBar from "../components/SearchBar";
import { useState, useEffect, useContext } from "react";
import {
    Box,
    MenuItem,
    Typography,
    Button,
    Snackbar,
    Alert,
    useTheme,
    TextField,
    Menu,
} from "@mui/material";
import { BateriaTestes } from "../types/baterias";
import { Paciente } from "../types/user";
import { Questionario } from "../types/questionario";
import VariableLayout from "../layouts/VariableLayout";
import { auth } from "../utils/auth";
import StylizedTitle from "../components/StylizedTitle";


export default function TestesScreen() {
    const theme = useTheme();
    const [snackbarProps, setSnackbarProps] = useState({
        open: false,
        type: "success",
        message: "",
    });
    const [bateriasTestes, setBateriasTestes] = useState<BateriaTestes[]>([]);
    const [tipoCriterio, setTipoCriterio] = useState("questionario");
    const [criterioDatas, setCriterioDatas] = useState({
        inicial: '',
        final: ''
    });



    const fetchBateriasByDatas = async (dataInicial: string, dataFinal: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();

        const response = await fetch(`${baseUrl}/baterias_testes/datas/${dataInicial}/${dataFinal}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
        if (response.ok) {
            const data = await response.json();
            setBateriasTestes(data);
        } else {
            const error = await response.json();
            setSnackbarProps({
                open: true,
                type: "error",
                message: error.message,
            });
        }
    }
    const fetchBateriasByNomePaciente = async (nomePaciente: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();
        console.log("tralalero tralala")

        const response = await fetch(`${baseUrl}/baterias_testes/nome_paciente/${nomePaciente}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
        if (response.ok) {
            const data = await response.json();
            setBateriasTestes(data);
        } else {
            const error = await response.json();
            setSnackbarProps({
                open: true,
                type: "error",
                message: error.message,
            });
        }
    }
    const fetchBateriasByTituloDescricaoQuestionario = async (criterio: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = auth.getToken();

        const response = await fetch(`${baseUrl}/baterias_testes/titulo_descricao_questionario/${criterio}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
        if (response.ok) {
            const data = await response.json();
            setBateriasTestes(data);
        } else {
            const error = await response.json();
            setSnackbarProps({
                open: true,
                type: "error",
                message: error.message,
            });
        }
    }
    const handleSearch = (searchTerm: string) => {


        switch (tipoCriterio) {
            case "paciente":
                fetchBateriasByNomePaciente(searchTerm);
                break;
            case "questionario":
                fetchBateriasByTituloDescricaoQuestionario(searchTerm);
                break;
            case "data":
                fetchBateriasByDatas(criterioDatas.inicial, criterioDatas.final);
                break;
            default:
                break;
        }

    }

      
    return (
        <VariableLayout>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',  marginTop: { xs: 6, md: 0 } }} >

            <StylizedTitle
                    title="Pesquisa de Baterias de Testes"/>
                </Box>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', md: 'row' }}}>
                {
                    tipoCriterio === "data" ? (

                        <>

                            <TextField
                                label="Data"
                                variant="outlined"
                                type="date"
                                value={criterioDatas.inicial}
                                onChange={(e) => setCriterioDatas({ ...criterioDatas, inicial: e.target.value })}
                                sx={{
                                    width: "100%",
                                    backgroundColor: theme.palette.background.paper,
                                    borderRadius: "4px",
                                }}
                                slotProps={{
                                    inputLabel: {

                                        shrink: true,
                                    },
                                }}
                            />
                            <TextField
                                label="Data"
                                variant="outlined"
                                type="date"
                                value={criterioDatas.final}
                                onChange={(e) => setCriterioDatas({ ...criterioDatas, final: e.target.value })}
                                sx={{
                                    width: "100%",
                                    backgroundColor: theme.palette.background.paper,
                                    borderRadius: "4px",
                                }}
                                slotProps={{
                                    inputLabel: {

                                        shrink: true,
                                    },
                                }}
                            ></TextField>
                        </>
                    ) : (

                        <SearchBar

                            onSearch={handleSearch}


                        />
                    )


                }
                <TextField
                    label="Criterio"
                    variant="outlined"
                    value={tipoCriterio}
                    onChange={(e) => setTipoCriterio(e.target.value)}
                    select
                    sx={{
                        width: { xs: "100%", md: "20%" },
                        backgroundColor: theme.palette.background.paper,
                        borderRadius: "4px",
                    }}

                >
                    <MenuItem value="questionario">
                        Questionario
                    </MenuItem>
                    <MenuItem value="paciente">
                        Paciente
                    </MenuItem>
                    <MenuItem value="data">
                        Data
                    </MenuItem>

                </TextField>
            </Box>


            

            <Snackbar
                open={snackbarProps.open}
                autoHideDuration={6000}
                onClose={() => setSnackbarProps({ ...snackbarProps, open: false })}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert
                    onClose={() => setSnackbarProps({ ...snackbarProps, open: false })}
                    severity={snackbarProps.type as "success" | "error" | "info" | "warning"}
                    sx={{ width: "100%" }}
                >
                    {snackbarProps.message}
                </Alert>
            </Snackbar>
        </VariableLayout>
    )

}
