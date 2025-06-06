import { Box, Card, useTheme, Divider, Typography } from "@mui/material";
import { BateriaTestes } from "../types/baterias"
import { Questionario } from "../types/questionario";
import PieChartResultados from "./PieChartResultados";
import InfoBox from "./InfoBox";
import { BallotRounded, FactCheck } from "@mui/icons-material";
import { ConditionalIconButton } from "./ConditionalIconButton";
import { auth } from "../utils/auth";



interface BateriaCardProps {
    bateria: BateriaTestes;
    questionario: Questionario;
    qtd_perguntas: number;
    nome_profissional: string;
    onAction: () => void;
}
const BateriaCard: React.FC<BateriaCardProps> = ({ bateria, questionario, qtd_perguntas, nome_profissional, onAction }) => {
    const theme = useTheme();
    const role = auth.getUserData()?.role;
    return (
        <Card
            sx={{
                margin: 2,
                backgroundColor: (theme) => theme.palette.background.paper,
                boxShadow: 3,
                borderRadius: 2,
                padding: 2
            }}
        >
            <Box>
                <Box id="title-action" sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <Box width={"100%"}>
                        <Typography variant="body2" component="h2" >
                            {questionario.titulo}
                        </Typography>
                    </Box>
               

                    <Divider orientation="vertical" flexItem sx={{ marginX: 1 }} />
                    {role === "admin" || role === "profissional_saude" || role === "paciente" ? (
                        <ConditionalIconButton
                            role={role}
                            onAction={onAction}
                        />
                    ) : null}
                </Box>

                <Divider id="divider" sx={{ marginY: 2 }} flexItem />

                <Box id="graficos" sx={{ display: 'flex', justifyContent: 'space-between' }} >
                <Box sx={{ display:'flex', alignItems:'center', justifyContent: 'center', width: "50%" }}>
                        <PieChartResultados
                            respostas={bateria.respostas?Object.keys(bateria.respostas):[]}
                            qtd_perguntas={qtd_perguntas}
                            mode="tiny"

                        />
                    </Box >

                    <Divider orientation="vertical" flexItem sx={{ marginX: 1 }} />
                    <Box sx={{ width: "50%" }}>

                        <Box sx={{ marginTop: 2, display: "flex",justifyContent: "center", flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                            <InfoBox
                                backgroundColor={theme.palette.info.main}
                                value={qtd_perguntas}
                                caption="Perguntas"
                                icon={<BallotRounded sx={{ fontSize: "2em" }} htmlColor="white" />}
                            />
                            <InfoBox
                                backgroundColor={theme.palette.success.main}
                                value={bateria.respostas?Object.keys(bateria.respostas).length:0}
                                caption="Respostas"
                                icon={<FactCheck sx={{ fontSize: "2em" }} htmlColor="white" />}
                            />


                        </Box>



                    </Box>
                </Box>

                <Divider sx={{ marginY: 2 }} />
                <Box sx={{ display: "flex", justifyContent: "space-between" }}>
                    <Box sx={{ display: "flex", justifyContent: "left", gap: 0.5 }}>
                        <Typography variant="caption" fontWeight={'bold'} color="textDisabled" component="strong" >
                            Data:
                        </Typography>
                        <Typography variant="caption" color="textDisabled" component="span" >

                            {new Date(bateria.created_at).toLocaleDateString("pt-BR", {
                                year: "numeric",
                                month: "2-digit",
                                day: "2-digit",
                            })}
                        </Typography>

                    </Box>
                    <Box sx={{ display: "flex", flexDirection: "row", marginLeft: 2, justifyContent: "left", gap: 0.5 }}>

                        <Typography variant="caption" component="span" color="textDisabled" >
                            <strong>Prescritor: </strong>{nome_profissional ? nome_profissional : "Não informado"}
                        </Typography>
                    </Box>
                </Box>


            </Box>
        </Card>
    )
}




export default BateriaCard;