import { Box, Card, IconButton, Tooltip, Typography } from "@mui/material";
import { Endereco } from "../types/endereco";
import DeleteIcon from '@mui/icons-material/Delete';

interface AdressCardProps {
  endereco: Endereco;
  onDelete: (index: string) => void;
  key: string;
}
export const AdressCard: React.FC<AdressCardProps> = ({ endereco, onDelete }) => {
  return (

    <Card id={`endereco-${endereco.id}`} sx={{ padding:1, marginBottom: 1, display: 'flex', justifyContent:"space-between" }}>
      <Typography variant="caption" gutterBottom>
        

        {endereco.cep} - {endereco.logradouro}, {endereco.numero}, {endereco.bairro}{endereco.complemento?", " + endereco.complemento + ", ":", "} {endereco.cidade} - {endereco.estado}

      </Typography>
      <Box>
        <Tooltip title="Deletar Endereço" arrow>
        <IconButton>
          <DeleteIcon color="error" fontSize="small" onClick={()=>onDelete(endereco.id)} />
        </IconButton>
        </Tooltip>

      </Box>
      </Card>
  
  );
};