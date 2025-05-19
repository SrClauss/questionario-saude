
interface ApiFetchOptions extends RequestInit {}

export const apiFetch = async (url: string, options: ApiFetchOptions = {}): Promise<Response> => {
    const response: Response = await fetch(url, options);

    if (response.status === 401) {
        // Limpar autenticação
        localStorage.removeItem('@App:token');
        // Redirecionar para login
        window.location.href = '/login';
        throw new Error('Sessão expirada');
    }

    return response;
}