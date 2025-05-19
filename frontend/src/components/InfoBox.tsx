import { Box, Typography } from "@mui/material";
import { ReactNode } from "react";
interface InfoBoxProps {
    backgroundColor: string;
    value: number;
    caption: string;
    icon: ReactNode;
}

const InfoBox: React.FC<InfoBoxProps> = ({ backgroundColor, value, caption, icon }) => {

    return (
        <Box
            sx={{
                backgroundColor: backgroundColor,
                display: "flex",
                borderRadius: 2,
                padding: 1,
                maxWidth: 180,
                width: 180,
                height: 100,
            }}
        >
            <Box
                sx={{ padding: 1, textAlign: "left", flexGrow: 1, color: "white" }}
            >
                <Typography variant="h3" sx={{ marginLeft: 1 }}>
                    {value}
                </Typography>
                <Typography variant="body1">
                    {caption}
                </Typography>
            </Box>
            {icon}
        </Box>
    );
};

export default InfoBox;