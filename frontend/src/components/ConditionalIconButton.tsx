import { BallotRounded, DeleteForever } from "@mui/icons-material";
import { Box, IconButton, Tooltip } from "@mui/material";
import React from "react";

interface ConditionalIconButtonProps {
  role: "admin" | "profissional_saude" | "paciente";
  onAction: () => void;
}


export const ConditionalIconButton: React.FC<ConditionalIconButtonProps> = ({
    role,
    onAction,
    }) => {
    return (
        <Box>
        {(role === "profissional_saude"  || role === "admin") &&(
            <Tooltip title="Deletar">
            <IconButton color="error" onClick={onAction}>
                <DeleteForever sx={{fontSize: "1.5em"}} />
            </IconButton>
            </Tooltip>
        )}
        {role === "paciente" && (
            <Tooltip title="Ver Respostas">
            <IconButton color="primary" onClick={onAction}>
                <BallotRounded sx={{fontSize: "1.5em"}} />
            </IconButton>
            </Tooltip>
        )}
        </Box>
    );
    }
 