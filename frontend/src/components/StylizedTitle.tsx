import { Box, Typography, Divider, useTheme } from '@mui/material'

interface StylizedTitleProps {
    title: string
}

export default function StylizedTitle({ title }: StylizedTitleProps) {
    const theme = useTheme()
    return(
        <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            marginBottom: 2,
            width: '100%',
            paddingTop: { xs: 2, sm: 0 }  // Adiciona espaço no topo para dispositivos móveis
        }}>
            <Typography 
                variant="h4"  
                sx={{ 
                    fontWeight: 500,
                    fontSize: { xs: '1.5rem', sm: '2rem', md: '2.125rem' },  // Texto menor em dispositivos móveis
                    flexShrink: 0  // Impede que o texto encolha demais
                }}
            >
                {title}
            </Typography>
            <Divider sx={{ flexGrow: 1, marginLeft: 2}} />
        </Box>
    ) 
}