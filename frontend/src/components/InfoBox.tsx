import { Box, Typography, useTheme, useMediaQuery } from "@mui/material";
import React, { ReactNode } from "react";

interface InfoBoxProps {
    backgroundColor: string;
    value: number;
    caption: string;
    icon: ReactNode;
}
const InfoBox: React.FC<InfoBoxProps> = ({ backgroundColor, value, caption, icon }) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    return (
        <Box
            sx={{
                backgroundColor: backgroundColor,
                display: "flex",
                alignItems: 'center',
                justifyContent: 'space-between',
                borderRadius: 2,
                padding: isMobile ? 1.5 : 2, // Ajustado para dar mais espaço interno
                width: isMobile ? 150 : 180,    // Mais estreito em telas pequenas
                height: isMobile ? 90 : 100,   // Mais baixo em telas pequenas
                boxSizing: 'border-box',
            }}
        >
            <Box
                sx={{
                    textAlign: "left",
                    color: "white",
                    overflow: 'hidden', // Para texto não quebrar o layout
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center', // Centralizar texto verticalmente
                }}
            >
                <Typography variant={isMobile ? "h5" : "h3"} sx={{ fontWeight: 'bold', lineHeight: 1.1 }}>
                    {value}
                </Typography>
                <Typography variant={isMobile ? "caption" : "body2"} sx={{ lineHeight: 1.2 }}>
                    {caption}
                </Typography>
            </Box>
            {/* Clona o ícone para ajustar seu tamanho responsivamente */}
            {React.isValidElement(icon) && React.cloneElement(icon as React.ReactElement<any>, {
                sx: {
                    ...((icon as any).props.sx || {}), // Mantém sx original se existir, como htmlColor
                    fontSize: isMobile ? '2.25rem' : '3rem', // Aprox. 36px e 48px
                    color: 'white', // Garante a cor, caso htmlColor não seja aplicado por algum motivo
                    marginLeft: theme.spacing(isMobile ? 1 : 1.5) // Espaçamento à esquerda do ícone
                }
            })}
        </Box>
    );
};

export default InfoBox;