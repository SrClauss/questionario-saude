import { useState } from "react";
import { IconButton, TextField } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

interface SearchBarProps {
    onSearch: (query: string) => void;
}

export default function SearchBar({ onSearch }: SearchBarProps) {
    const [searchQuery, setSearchQuery] = useState<string>("");

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === "Enter") {
            onSearch(searchQuery);
        }
    };

    return (
        <TextField
            variant="outlined"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            slotProps={
                {
                    input:{

                        endAdornment: (
                            <IconButton onClick={() => onSearch(searchQuery)}>
                                <SearchIcon />
                            </IconButton>
                        ),

                    }
                }
            }
            sx={{ width: "100%", marginTop: "16px" }}
        />
    );
}