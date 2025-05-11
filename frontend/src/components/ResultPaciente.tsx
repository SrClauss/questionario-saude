import { Box,  IconButton, Typography } from "@mui/material"
import { Paciente } from "../types/user"
import { Delete, Send } from "@mui/icons-material"
interface ResultPacienteProps {
    paciente: Paciente,
    onSelect: (paciente: Paciente) => void
    left?: boolean


}
export default function ResultPaciente({ paciente, onSelect, left=true }: ResultPacienteProps) {
    const handleSelect = () => {
        onSelect(paciente)
    }

   
    return (
       <Box
       sx={{
              display: 'flex',
              justifyContent: 'space-between',
              border: '1px solid #ccc',
              marginY: 1,
              alignItems: 'center',
              paddingX: 2,
              borderRadius: 1,

              
       }}
       
       >
        <Typography>{paciente.nome}</Typography>
        <IconButton
            onClick={handleSelect}
            
        >
            {left ? (
                <Send color="info" />
            ) : (
                <Delete color="error" />
            )}

        </IconButton>
   




       </Box>
    )
}   