import { createTheme, ThemeProvider as MUIThemeProvider } from '@mui/material/styles'
import { ReactNode } from 'react'

// Definição das cores e configurações do tema
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#fc9e22',
      light: '#fdb951',
      dark: '#b16e18',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#00658b',
      light: '#337fa0',
      dark: '#004761',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#ffeb3b',
      light: '#ffef5c',
      dark: '#b2a429',
      contrastText: '#000000',
    },
    background: {
      default: '#ffffff',
      paper: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      'Nunito',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 24px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.2)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
      },
    },
  },
})

interface ThemeProviderProps {
  children: ReactNode
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <MUIThemeProvider theme={theme}>
      {children}
    </MUIThemeProvider>
  )
}