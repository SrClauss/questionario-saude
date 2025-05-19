import { Box, Checkbox, Typography } from "@mui/material";
import { Alternativa } from "../types/questionario";

interface AlternativaCheckItemProps {
  alternativa: Alternativa;
  respostas: string[]; // Array de IDs de alternativas selecionadas
  onChange: (alternativaId: string, checked: boolean) => void;
}

export default function AlternativaCheckItem({ 
  alternativa, 
  respostas, 
  onChange 
}: AlternativaCheckItemProps) {
  // Verifica se a alternativa atual está no array de respostas
  const isChecked = alternativa.id ? respostas.includes(alternativa.id) : false;
  
  return (
    <Box 
      sx={{
        display: "flex",
        alignItems: "center",
        marginBottom: 1,
        padding: 1,
        borderRadius: 1,
        '&:hover': {
          backgroundColor: 'rgba(0, 0, 0, 0.04)'
        }
      }}
    >
      <Checkbox 
        checked={isChecked}
        onChange={(e) => alternativa.id && onChange(alternativa.id, e.target.checked)} 
      />
      <Typography variant="body1">{alternativa.texto}</Typography>
    </Box>
  );
}