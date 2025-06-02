import React, { createContext, useEffect, useState} from 'react';
import { UnidadeSaude } from '../types/unidade_saude';


interface UnidadeSaudeContextProps{
    unidadesSaude: UnidadeSaude[];
    setUnidadesSaude: React.Dispatch<React.SetStateAction<UnidadeSaude[]>>;
}

export const UnidadeSaudeContext = createContext<UnidadeSaudeContextProps>({
    unidadesSaude: [],
    setUnidadesSaude: () => {},
});

const fetchUnidadeSaudes = async () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem('@App:token');
    const url = `${baseUrl}/unidades_saude`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    const data = await response.json();

    return data;
}

export const UnidadeSaudeProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
    const [unidadesSaude, setUnidadesSaude] = useState<UnidadeSaude[]>([]);
    useEffect(() => {
        fetchUnidadeSaudes().then(data => {
            setUnidadesSaude(data);
        });
    }, []);
    return (
        <UnidadeSaudeContext.Provider value={{ unidadesSaude, setUnidadesSaude }}>
            {children}
        </UnidadeSaudeContext.Provider>
    );
};