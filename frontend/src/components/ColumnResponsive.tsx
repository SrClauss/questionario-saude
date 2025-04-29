import React from 'react';
import Box from '@mui/material/Box';

export default function ColumnResponsive({ children }: { children: React.ReactNode }) {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: { xs: 'column', sm: 'row' },
                justifyContent: 'space-between',
                alignItems: 'center',
                width: '100%',
                gap:{ xs: 0, sm: 1 },
                maxWidth: '100%',
              
            }}
        >
            {children}
        </Box>
    );
}