// src/components/AlternativaRadioItem.tsx
import { Box, Radio, Typography } from "@mui/material";
import { Alternativa } from "../types/questionario";

interface AlternativaRadioItemProps {
  alternativa: Alternativa;
  selected: boolean;
  onChange: (alternativaId: string) => void;
}

export default function AlternativaRadioItem({ 
  alternativa, 
  selected, 
  onChange 
}: AlternativaRadioItemProps) {
  return (
    <Box 
      key={alternativa.id} 
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
      <Radio 
        value={alternativa.id} 
        checked={selected}
        onChange={() => alternativa.id && onChange(alternativa.id)} 
      />
      <Typography variant="body1">{alternativa.texto}</Typography>
    </Box>
  );
}