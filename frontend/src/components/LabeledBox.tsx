import React from 'react';
import { Box, Typography } from '@mui/material';

interface LabeledBoxProps {
    label: string;
    children: React.ReactNode;
}

const LabeledBox: React.FC<LabeledBoxProps> = ({ label, children }) => {
    return (
        <Box 
            sx={{
                position: 'relative',
                border: '1px solid',
                borderColor: 'grey.400',
                borderRadius: 1,
                padding: 2,
                marginTop: 3,
            }}
        >
            <Typography 
                variant="caption" 
                component="span" 
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 16,
                    transform: 'translateY(-50%)',
                    backgroundColor: 'white',
                    paddingX: 1,
                }}
            >
                {label}
            </Typography>
            <Box>
                {children}
            </Box>
        </Box>
    );
};

export default LabeledBox;