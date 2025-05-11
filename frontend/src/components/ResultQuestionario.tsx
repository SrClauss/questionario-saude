import React from "react";
import { Card, CardContent, Typography, Button, Box } from "@mui/material";
import { Questionario } from "../types/questionario";

interface ResultQuestionarioProps {
  questionario: Questionario;
  onSelect: (questionario: Questionario) => void;
  left?: boolean;
}

const ResultQuestionario: React.FC<ResultQuestionarioProps> = ({ questionario, onSelect, left = true }) => {
  return (
    <Card sx={{ my: 1, width: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", flexDirection: "column" }}>
          <Typography variant="h6" gutterBottom>
            {questionario.titulo}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {questionario.descricao}
          </Typography>
          <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 1 }}>
            <Button 
              variant="contained" 
              size="small" 
              onClick={() => onSelect(questionario)}
            >
              {left ? "Selecionar" : "Remover"}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultQuestionario;