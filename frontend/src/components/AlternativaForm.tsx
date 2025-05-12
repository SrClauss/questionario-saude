import React, { useState, useEffect } from "react";
import { Box, TextField, Typography, Button, Divider, IconButton } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import CheckIcon from "@mui/icons-material/Check";
import { Alternativa } from "../types/questionario";

interface EscalasAlternativas {
    pergunta_id: string;
    onSetAlternativas: (alternativas: Alternativa[]) => void;
    alternativas: Alternativa[];
}

interface AlternativaProps {
    texto: string;
    valor: number;
    onSetValor: (valor: number) => void;
    onSetTexto: (texto: string) => void;
}

const AlternativaCard: React.FC<AlternativaProps> = ({ texto, valor, onSetValor, onSetTexto }) => {
    const [isEditing, setIsEditing] = useState(false);


    return (
        <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
            {isEditing ? (
                <>
                    <TextField
                        value={texto}
                        onChange={(e) => onSetTexto(e.target.value)}
                        size="small"
                        sx={{ minWidth: 300 }}
                    />
                    <IconButton
                        color="primary"
                        onClick={() => {
                            onSetTexto(texto);
                            setIsEditing(false);
                        }}
                    >
                        <CheckIcon />
                    </IconButton>
                </>
            ) : (
                <>
                
                    <IconButton sx={{width:"fit-content"}} color="primary" onClick={() => setIsEditing(true)}>
                        <EditIcon />
                    </IconButton>
                    <Typography variant="body2" sx={{ minWidth: 150 }}>
                        {texto}
                    </Typography>
                </>
            )}
            </Box>
            <TextField
                label="Valor"
                type="number"
                value={valor}
                onChange={(e) => onSetValor(Number(e.target.value))}
                size="small"
                sx={{ width: 80 }}
            />  
        </Box>
    );
};

const header = (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
            Alternativas
        </Typography>
        <Box sx={{ flexGrow: 1 }}>
            <Divider sx={{ mb: 2 }} />
        </Box>
    </Box>
);
const EscalaLikert3: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [discordo, setDiscordo] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id,
            texto: "Discordo",
            valor: 0,
            ordem: 1,
        }
    );
    const [neutro, setNeutro] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id,
            texto: "Neutro",
            valor: 1,
            ordem: 2,
        }
    );
    const [concordo, setConcordo] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id,
            texto: "Concordo",
            valor: 2,
            ordem: 3,
        }
    );

    useEffect(() => {
        onSetAlternativas([discordo, neutro, concordo]);
    }, [discordo, neutro, concordo]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={discordo.texto}
                valor={discordo.valor}
                onSetValor={(valor) => setDiscordo({ ...discordo, valor })}
                onSetTexto={(novoTexto) => setDiscordo({ ...discordo, texto: novoTexto })}
            />
            <AlternativaCard
                texto={neutro.texto}
                valor={neutro.valor}
                onSetValor={(valor) => setNeutro({ ...neutro, valor })}
                onSetTexto={(novoTexto) => setNeutro({ ...neutro, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordo.texto}
                valor={concordo.valor}
                onSetValor={(valor) => setConcordo({ ...concordo, valor })}
                onSetTexto={(novoTexto) => setConcordo({ ...concordo, texto: novoTexto })}
            />
        </Box>
    );
}
const EscalaLikert4: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [nuncaOuRaramente, setNuncaOuRaramente] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id,
            texto: "Nunca ou raramente",
            valor: 0,
            ordem: 1,
        }
    );
    const [ocasionalmente, setOcasionalmente] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id,
            texto: "Ocasionalmente",
            valor: 1,
            ordem: 2,
        }
    );
    const [frequentemente, setFrequentemente] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id,
            texto: "Frequentemente",
            valor: 2,
            ordem: 3,
        }
    );
    const [muitoFrequente, setMuitoFrequente] = useState<Alternativa>(
        alternativas[3] || {
            pergunta_id,
            texto: "Muito frequentemente ou sempre",
            valor: 3,
            ordem: 4,
        }
    );

    useEffect(() => {
        onSetAlternativas([nuncaOuRaramente, ocasionalmente, frequentemente, muitoFrequente]);
    }, [nuncaOuRaramente, ocasionalmente, frequentemente, muitoFrequente, onSetAlternativas]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={nuncaOuRaramente.texto}
                valor={nuncaOuRaramente.valor}
                onSetValor={(valor) => setNuncaOuRaramente({ ...nuncaOuRaramente, valor })}
                onSetTexto={(novoTexto) => setNuncaOuRaramente({ ...nuncaOuRaramente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={ocasionalmente.texto}
                valor={ocasionalmente.valor}
                onSetValor={(valor) => setOcasionalmente({ ...ocasionalmente, valor })}
                onSetTexto={(novoTexto) => setOcasionalmente({ ...ocasionalmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={frequentemente.texto}
                valor={frequentemente.valor}
                onSetValor={(valor) => setFrequentemente({ ...frequentemente, valor })}
                onSetTexto={(novoTexto) => setFrequentemente({ ...frequentemente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={muitoFrequente.texto}
                valor={muitoFrequente.valor}
                onSetValor={(valor) => setMuitoFrequente({ ...muitoFrequente, valor })}
                onSetTexto={(novoTexto) => setMuitoFrequente({ ...muitoFrequente, texto: novoTexto })}
            />
        </Box>
    );
};

const EscalaLikert5: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [discordoTotalmente, setDiscordoTotalmente] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id,
            texto: "Discordo Totalmente",
            valor: 1,
            ordem: 1,
        }
    );
    const [discordoParcialmente, setDiscordoParcialmente] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id,
            texto: "Discordo Parcialmente",
            valor: 2,
            ordem: 2,
        }
    );
    const [neutro, setNeutro] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id,
            texto: "Neutro",
            valor: 3,
            ordem: 3,
        }
    );
    const [concordoParcialmente, setConcordoParcialmente] = useState<Alternativa>(
        alternativas[3] || {
            pergunta_id,
            texto: "Concordo Parcialmente",
            valor: 4,
            ordem: 4,
        }
    );
    const [concordoTotalmente, setConcordoTotalmente] = useState<Alternativa>(
        alternativas[4] || {
            pergunta_id,
            texto: "Concordo Totalmente",
            valor: 5,
            ordem: 5,
        }
    );

    useEffect(() => {
        onSetAlternativas([discordoTotalmente, discordoParcialmente, neutro, concordoParcialmente, concordoTotalmente]);
    }, [discordoTotalmente, discordoParcialmente, neutro, concordoParcialmente, concordoTotalmente, onSetAlternativas]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={discordoTotalmente.texto}
                valor={discordoTotalmente.valor}
                onSetValor={(valor) => setDiscordoTotalmente({ ...discordoTotalmente, valor })}
                onSetTexto={(novoTexto) => setDiscordoTotalmente({ ...discordoTotalmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={discordoParcialmente.texto}
                valor={discordoParcialmente.valor}
                onSetValor={(valor) => setDiscordoParcialmente({ ...discordoParcialmente, valor })}
                onSetTexto={(novoTexto) => setDiscordoParcialmente({ ...discordoParcialmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={neutro.texto}
                valor={neutro.valor}
                onSetValor={(valor) => setNeutro({ ...neutro, valor })}
                onSetTexto={(novoTexto) => setNeutro({ ...neutro, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordoParcialmente.texto}
                valor={concordoParcialmente.valor}
                onSetValor={(valor) => setConcordoParcialmente({ ...concordoParcialmente, valor })}
                onSetTexto={(novoTexto) => setConcordoParcialmente({ ...concordoParcialmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordoTotalmente.texto}
                valor={concordoTotalmente.valor}
                onSetValor={(valor) => setConcordoTotalmente({ ...concordoTotalmente, valor })}
                onSetTexto={(novoTexto) => setConcordoTotalmente({ ...concordoTotalmente, texto: novoTexto })}
            />
        </Box>
    );
};

const EscalaLikert7: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [discordoTotalmente, setDiscordoTotalmente] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id,
            texto: "Discordo Totalmente",
            valor: 1,
            ordem: 1,
        }
    );
    const [discordo, setDiscordo] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id,
            texto: "Discordo",
            valor: 2,
            ordem: 2,
        }
    );
    const [discordoParcialmente, setDiscordoParcialmente] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id,
            texto: "Discordo Parcialmente",
            valor: 3,
            ordem: 3,
        }
    );
    const [neutro, setNeutro] = useState<Alternativa>(
        alternativas[3] || {
            pergunta_id,
            texto: "Neutro",
            valor: 4,
            ordem: 4,
        }
    );
    const [concordoParcialmente, setConcordoParcialmente] = useState<Alternativa>(
        alternativas[4] || {
            pergunta_id,
            texto: "Concordo Parcialmente",
            valor: 5,
            ordem: 5,
        }
    );
    const [concordo, setConcordo] = useState<Alternativa>(
        alternativas[5] || {
            pergunta_id,
            texto: "Concordo",
            valor: 6,
            ordem: 6,
        }
    );
    const [concordoTotalmente, setConcordoTotalmente] = useState<Alternativa>(
        alternativas[6] || {
            pergunta_id,
            texto: "Concordo Totalmente",
            valor: 7,
            ordem: 7,
        }
    );

    useEffect(() => {
        onSetAlternativas([
            discordoTotalmente,
            discordo,
            discordoParcialmente,
            neutro,
            concordoParcialmente,
            concordo,
            concordoTotalmente,
        ]);
    }, [
        discordoTotalmente,
        discordo,
        discordoParcialmente,
        neutro,
        concordoParcialmente,
        concordo,
        concordoTotalmente,
        onSetAlternativas,
    ]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={discordoTotalmente.texto}
                valor={discordoTotalmente.valor}
                onSetValor={(valor) => setDiscordoTotalmente({ ...discordoTotalmente, valor })}
                onSetTexto={(novoTexto) => setDiscordoTotalmente({ ...discordoTotalmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={discordo.texto}
                valor={discordo.valor}
                onSetValor={(valor) => setDiscordo({ ...discordo, valor })}
                onSetTexto={(novoTexto) => setDiscordo({ ...discordo, texto: novoTexto })}
            />
            <AlternativaCard
                texto={discordoParcialmente.texto}
                valor={discordoParcialmente.valor}
                onSetValor={(valor) => setDiscordoParcialmente({ ...discordoParcialmente, valor })}
                onSetTexto={(novoTexto) => setDiscordoParcialmente({ ...discordoParcialmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={neutro.texto}
                valor={neutro.valor}
                onSetValor={(valor) => setNeutro({ ...neutro, valor })}
                onSetTexto={(novoTexto) => setNeutro({ ...neutro, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordoParcialmente.texto}
                valor={concordoParcialmente.valor}
                onSetValor={(valor) => setConcordoParcialmente({ ...concordoParcialmente, valor })}
                onSetTexto={(novoTexto) => setConcordoParcialmente({ ...concordoParcialmente, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordo.texto}
                valor={concordo.valor}
                onSetValor={(valor) => setConcordo({ ...concordo, valor })}
                onSetTexto={(novoTexto) => setConcordo({ ...concordo, texto: novoTexto })}
            />
            <AlternativaCard
                texto={concordoTotalmente.texto}
                valor={concordoTotalmente.valor}
                onSetValor={(valor) => setConcordoTotalmente({ ...concordoTotalmente, valor })}
                onSetTexto={(novoTexto) => setConcordoTotalmente({ ...concordoTotalmente, texto: novoTexto })}
            />
        </Box>
    );
};

const EscalaBooleana: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [sim, setSim] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id,
            texto: "Sim",
            valor: 1,
            ordem: 1,
        }
    );
    const [nao, setNao] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id,
            texto: "Não",
            valor: 0,
            ordem: 2,
        }
    );

    useEffect(() => {
        onSetAlternativas([sim, nao]);
    }, [sim, nao, onSetAlternativas]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={sim.texto}
                valor={sim.valor}
                onSetValor={(valor) => setSim({ ...sim, valor })}
                onSetTexto={(novoTexto) => setSim({ ...sim, texto: novoTexto })}
            />
            <AlternativaCard
                texto={nao.texto}
                valor={nao.valor}
                onSetValor={(valor) => setNao({ ...nao, valor })}
                onSetTexto={(novoTexto) => setNao({ ...nao, texto: novoTexto })}
            />
        </Box>
    );
};

const EscalaPersonalizada: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [altList, setAltList] = useState<Alternativa[]>(
        alternativas.length > 0
            ? alternativas
            : [
                {
                    pergunta_id,
                    texto: "",
                    valor: 0,
                    ordem: 1,
                },
            ]
    );

    useEffect(() => {
        onSetAlternativas(altList);
    }, [altList, onSetAlternativas]);

    const handleSetTexto = (index: number, newTexto: string) => {
        const newList = altList.map((alt, idx) =>
            idx === index ? { ...alt, texto: newTexto } : alt
        );
        setAltList(newList);
    };

    const handleSetValor = (index: number, newValor: number) => {
        const newList = altList.map((alt, idx) =>
            idx === index ? { ...alt, valor: newValor } : alt
        );
        setAltList(newList);
    };

    const handleAddAlternative = () => {
        const newAlt: Alternativa = {
            pergunta_id,
            texto: "",
            valor: altList.length + 1,
            ordem: altList.length + 1,
        };
        setAltList([...altList, newAlt]);
    };

    const handleRemoveAlternative = (index: number) => {
        if (altList.length <= 1) return;
        const newList = altList
            .filter((_, idx) => idx !== index)
            .map((alt, idx) => ({
                ...alt,
                ordem: idx + 1,
            }));
        setAltList(newList);
    };

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                    Alternativas
                </Typography>
                <Box sx={{ flexGrow: 1 }}>
                    <Divider sx={{ mb: 2 }} />
                </Box>
            </Box>
            {altList.map((alt, idx) => (
                <Box key={idx} sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
                    <TextField
                        label={`Texto da Alternativa ${idx + 1}`}
                        value={alt.texto}
                        onChange={(e) => handleSetTexto(idx, e.target.value)}
                        size="small"
                        fullWidth
                    />
                    <TextField
                        label="Valor"
                        type="number"
                        value={alt.valor}
                        onChange={(e) => handleSetValor(idx, Number(e.target.value))}
                        size="small"
                        sx={{ width: 80 }}
                    />
                    <Button variant="outlined" color="error" onClick={() => handleRemoveAlternative(idx)}>
                        Remover
                    </Button>
                </Box>
            ))}
            <Button variant="contained" onClick={handleAddAlternative}>
                Adicionar Alternativa
            </Button>
        </Box>
    );
};

interface RenderAlternativasProps {
    tipo_resposta: string;
    pergunta_id: string;
    onSetAlternativas: (alternativas: Alternativa[]) => void;
    alternativas: Alternativa[];
}

const RenderAlternativas: React.FC<RenderAlternativasProps> = ({
    tipo_resposta,
    pergunta_id,
    onSetAlternativas,
    alternativas,
}) => {
    switch (tipo_resposta) {

        case "escala_likert_3":
            return <EscalaLikert3 pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
        case "escala_likert_4":
            return <EscalaLikert4 pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
        case "escala_likert_5":
            return <EscalaLikert5 pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
        case "escala_likert_7":
            return <EscalaLikert7 pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
        case "texto":
            return (
                <Box sx={{ mt: 2, p: 1, backgroundColor: "#f5f5f5", borderRadius: 1 }}>
                    <Typography variant="body2" color="textSecondary">
                        Perguntas do tipo "Texto" não necessitam de alternativas.
                    </Typography>
                </Box>
            );
        case "booleano":
            return <EscalaBooleana pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
        case "numero":
            return (
                <Box sx={{ mt: 2, p: 1, backgroundColor: "#f5f5f5", borderRadius: 1 }}>
                    <Typography variant="body2" color="textSecondary">
                        Perguntas do tipo "Número" não necessitam de alternativas.
                    </Typography>
                </Box>
            );
        default:
            return <EscalaPersonalizada pergunta_id={pergunta_id} onSetAlternativas={onSetAlternativas} alternativas={alternativas} />;
    }
};

export default RenderAlternativas;