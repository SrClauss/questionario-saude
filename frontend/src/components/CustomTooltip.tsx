import { styled, Tooltip, tooltipClasses, TooltipProps } from '@mui/material';

const CustomTooltip = styled(({ className, ...props }: TooltipProps) => (
  <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    fontSize: '1.5rem', // Tamanho da fonte desejado
    maxWidth: '300px',  // Largura máxima
    textAlign: 'justify', // Justifica o texto
    color: theme.palette.warning.main, // Cor do texto
    padding: theme.spacing(2), // Ex: 16px se a spacing for 8px
  },
}));

export default CustomTooltip;