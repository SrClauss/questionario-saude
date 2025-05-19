import { Box, LinearProgress, Typography } from "@mui/material";

interface ProgressBarProps {
    total: number;
    current: number;
}

export default function ProgressBar({ total, current }: ProgressBarProps) {
    const percent = total > 0 ? Math.round((current / total) * 100) : 0;

    return (
        <Box sx={{ width: "100%", mb: 2 }}>
            <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box sx={{ width: "100%", mr: 1 }}>
                    <LinearProgress variant="determinate" value={percent} />
                </Box>
                <Box sx={{ minWidth: 35 }}>
                    <Typography variant="body2" color="text.secondary">{`${current}/${total}`}</Typography>
                </Box>
            </Box>
        </Box>
    );
}