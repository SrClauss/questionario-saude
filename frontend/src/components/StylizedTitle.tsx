import { Box, Typography, Divider } from '@mui/material'
import { TypographyProps } from '@mui/material/Typography'; // Importa o tipo das props do Typography

interface StylizedTitleProps {
    title: string;
    size?: TypographyProps['variant']; // Usa o tipo importado diretamente
}

export default function StylizedTitle({ title, size="h4" }: StylizedTitleProps) {

    return(
        <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            marginBottom: 2,
            width: '100%',
            paddingTop: { xs: 2, sm: 0 }  // Adiciona espaço no topo para dispositivos móveis
        }}>
            <Typography 
                variant={size}
                sx={{ 
                    fontWeight: 500,
                    color: 'secondary.main',
                   
                }}
            >
                {title}
            </Typography>
            <Divider sx={{ flexGrow: 1, marginLeft: 2, backgroundColor: 'secondary.main'}} />
        </Box>
    ) 
}