@echo off
SETLOCAL

REM Define o diretório raiz do seu projeto
SET "PROJECT_ROOT=%~dp0"
CD /D "%PROJECT_ROOT%"

echo.
echo ====================================
echo  Iniciando Caddy Server
echo ====================================
REM Inicia o Caddy server em uma nova janela.
REM O comando START permite que o script continue executando.
START "Caddy Server" "%PROJECT_ROOT%caddy.exe" run

echo.
echo ====================================
echo  Iniciando API (Python/venv)
echo ====================================
REM Entra na pasta da API
CD /D "%PROJECT_ROOT%api"

REM Ativa o ambiente virtual E inicia o servidor Python em uma nova janela.
REM A ordem é: ativar venv, e SÓ SE ativar deu certo (&&), executar python app.py.
START "API Server" cmd /k "venv\Scripts\activate && python app.py"
REM O '/k' mantém a janela aberta após a execução do comando, útil para ver logs.

echo.
echo ====================================
echo  Iniciando Frontend (npm run dev)
echo ====================================
REM Entra na pasta do Frontend
CD /D "%PROJECT_ROOT%frontend"

REM Inicia o frontend em uma nova janela.
START "Frontend Dev Server" cmd /k "npm run dev"
REM O '/k' mantém a janela aberta após a execução do comando, útil para ver logs.

echo.
echo ====================================
echo  Todos os serviços foram iniciados.
echo  Verifique as novas janelas de console.
echo ====================================
echo.
pause
ENDLOCAL
