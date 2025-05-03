import React, { useState, useEffect } from "react";
import { Box, TextField, Typography, Button, Divider } from "@mui/material";
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
}

const AlternativaCard: React.FC<AlternativaProps> = ({ texto, valor, onSetValor }) => {
    return (
        <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-around" }}>
            <Typography variant="body2" sx={{ minWidth: 150 }}>
                {texto}
            </Typography>
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
        <Typography variant="h6" sx={{ mb: 2 }}>Alternativas</Typography>
        <Box sx={{ flexGrow: 1 }}>
            <Divider sx={{ mb: 2 }} />
        </Box>
    </Box>
);

const EscalaLikert5: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [discordoTotalmente, setDiscordoTotalmente] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id: pergunta_id,
            texto: "Discordo Totalmente",
            valor: 1,
            ordem: 1,
        }
    );
    const [discordoParcialmente, setDiscordoParcialmente] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id: pergunta_id,
            texto: "Discordo Parcialmente",
            valor: 2,
            ordem: 2,
        }
    );
    const [neutro, setNeutro] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id: pergunta_id,
            texto: "Neutro",
            valor: 3,
            ordem: 3,
        }
    );
    const [concordoParcialmente, setConcordoParcialmente] = useState<Alternativa>(
        alternativas[3] || {
            pergunta_id: pergunta_id,
            texto: "Concordo Parcialmente",
            valor: 4,
            ordem: 4,
        }
    );
    const [concordoTotalmente, setConcordoTotalmente] = useState<Alternativa>(
        alternativas[4] || {
            pergunta_id: pergunta_id,
            texto: "Concordo Totalmente",
            valor: 5,
            ordem: 5,
        }
    );

    useEffect(() => {
        onSetAlternativas([
            discordoTotalmente,
            discordoParcialmente,
            neutro,
            concordoParcialmente,
            concordoTotalmente,
        ]);
    }, [discordoTotalmente, discordoParcialmente, neutro, concordoParcialmente, concordoTotalmente, onSetAlternativas]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={discordoTotalmente.texto}
                valor={discordoTotalmente.valor}
                onSetValor={(valor) => setDiscordoTotalmente({ ...discordoTotalmente, valor })}
            />
            <AlternativaCard
                texto={discordoParcialmente.texto}
                valor={discordoParcialmente.valor}
                onSetValor={(valor) => setDiscordoParcialmente({ ...discordoParcialmente, valor })}
            />
            <AlternativaCard
                texto={neutro.texto}
                valor={neutro.valor}
                onSetValor={(valor) => setNeutro({ ...neutro, valor })}
            />
            <AlternativaCard
                texto={concordoParcialmente.texto}
                valor={concordoParcialmente.valor}
                onSetValor={(valor) => setConcordoParcialmente({ ...concordoParcialmente, valor })}
            />
            <AlternativaCard
                texto={concordoTotalmente.texto}
                valor={concordoTotalmente.valor}
                onSetValor={(valor) => setConcordoTotalmente({ ...concordoTotalmente, valor })}
            />
        </Box>
    );
};

const EscalaLikert7: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [discordoTotalmente, setDiscordoTotalmente] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id: pergunta_id,
            texto: "Discordo Totalmente",
            valor: 1,
            ordem: 1,
        }
    );
    const [discordo, setDiscordo] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id: pergunta_id,
            texto: "Discordo",
            valor: 2,
            ordem: 2,
        }
    );
    const [discordoParcialmente, setDiscordoParcialmente] = useState<Alternativa>(
        alternativas[2] || {
            pergunta_id: pergunta_id,
            texto: "Discordo Parcialmente",
            valor: 3,
            ordem: 3,
        }
    );
    const [neutro, setNeutro] = useState<Alternativa>(
        alternativas[3] || {
            pergunta_id: pergunta_id,
            texto: "Neutro",
            valor: 4,
            ordem: 4,
        }
    );
    const [concordoParcialmente, setConcordoParcialmente] = useState<Alternativa>(
        alternativas[4] || {
            pergunta_id: pergunta_id,
            texto: "Concordo Parcialmente",
            valor: 5,
            ordem: 5,
        }
    );
    const [concordo, setConcordo] = useState<Alternativa>(
        alternativas[5] || {
            pergunta_id: pergunta_id,
            texto: "Concordo",
            valor: 6,
            ordem: 6,
        }
    );
    const [concordoTotalmente, setConcordoTotalmente] = useState<Alternativa>(
        alternativas[6] || {
            pergunta_id: pergunta_id,
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
        onSetAlternativas
    ]);

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            {header}
            <AlternativaCard
                texto={discordoTotalmente.texto}
                valor={discordoTotalmente.valor}
                onSetValor={(valor) => setDiscordoTotalmente({ ...discordoTotalmente, valor })}
            />
            <AlternativaCard
                texto={discordo.texto}
                valor={discordo.valor}
                onSetValor={(valor) => setDiscordo({ ...discordo, valor })}
            />
            <AlternativaCard
                texto={discordoParcialmente.texto}
                valor={discordoParcialmente.valor}
                onSetValor={(valor) => setDiscordoParcialmente({ ...discordoParcialmente, valor })}
            />
            <AlternativaCard
                texto={neutro.texto}
                valor={neutro.valor}
                onSetValor={(valor) => setNeutro({ ...neutro, valor })}
            />
            <AlternativaCard
                texto={concordoParcialmente.texto}
                valor={concordoParcialmente.valor}
                onSetValor={(valor) => setConcordoParcialmente({ ...concordoParcialmente, valor })}
            />
            <AlternativaCard
                texto={concordo.texto}
                valor={concordo.valor}
                onSetValor={(valor) => setConcordo({ ...concordo, valor })}
            />
            <AlternativaCard
                texto={concordoTotalmente.texto}
                valor={concordoTotalmente.valor}
                onSetValor={(valor) => setConcordoTotalmente({ ...concordoTotalmente, valor })}
            />
        </Box>
    );
};

const EscalaBooleana: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {

    const [sim, setSim] = useState<Alternativa>(
        alternativas[0] || {
            pergunta_id: pergunta_id,
            texto: "Sim",
            valor: 1,
            ordem: 1,
        }
    );
    const [nao, setNao] = useState<Alternativa>(
        alternativas[1] || {
            pergunta_id: pergunta_id,
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
            />
            <AlternativaCard
                texto={nao.texto}
                valor={nao.valor}
                onSetValor={(valor) => setNao({ ...nao, valor })}
            />
        </Box>
    );
}

const EscalaPersonalizada: React.FC<EscalasAlternativas> = ({ pergunta_id, onSetAlternativas, alternativas }) => {
    const [altList, setAltList] = useState<Alternativa[]>(
        alternativas.length > 0
            ? alternativas
            : [
                {
                    pergunta_id: pergunta_id,
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
        const newList = altList.filter((_, idx) => idx !== index).map((alt, idx) => ({
            ...alt,
            ordem: idx + 1,
        }));
        setAltList(newList);
    };

    return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>Alternativas</Typography>
                <Box sx={{ flexGrow: 1 }}>
                    <Divider sx={{ mb: 2 }} />
                </Box>
            </Box>
            {altList.map((alt, idx) => (
                <Box
                    key={idx}
                    sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}
                >
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
                    <Button
                        variant="outlined"
                        color="error"
                        onClick={() => handleRemoveAlternative(idx)}
                    >
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
        case "escala_likert":
            return (
                <EscalaLikert5
                    pergunta_id={pergunta_id}
                    onSetAlternativas={onSetAlternativas}
                    alternativas={alternativas}
                />
            );
        case "escala_likert_7":
            return (
                <EscalaLikert7
                    pergunta_id={pergunta_id}
                    onSetAlternativas={onSetAlternativas}
                    alternativas={alternativas}
                />
            );
        case "texto":

        return (
            <Box sx={{ mt: 2, p: 1, backgroundColor: "#f5f5f5", borderRadius: 1 }}>
              <Typography variant="body2" color="textSecondary">
                Perguntas do tipo "Texto" não necessitam de alternativas.
              </Typography>
            </Box>
          );
        case "booleano":
            return (
                <EscalaBooleana
                    pergunta_id={pergunta_id}
                    onSetAlternativas={onSetAlternativas}
                    alternativas={alternativas}
                />
            );
        
        case "numero":
            return (
                <Box sx={{ mt: 2, p: 1, backgroundColor: "#f5f5f5", borderRadius: 1 }}>
                    <Typography variant="body2" color="textSecondary">
                        Perguntas do tipo "Número" não necessitam de alternativas.
                    </Typography>
                </Box>
            );
        default:
            return (
                <EscalaPersonalizada
                    pergunta_id={pergunta_id}
                    onSetAlternativas={onSetAlternativas}
                    alternativas={alternativas}
                />
            );
    }
};

export default RenderAlternativas;