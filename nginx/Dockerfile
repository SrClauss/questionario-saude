# Estágio 1: Build do Frontend (React/Vite)
FROM node:20-alpine AS builder

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ ./
RUN npm run build

# Estágio 2: Servidor Nginx de Produção
FROM nginx:alpine

# Copia os arquivos estáticos do frontend para o subdiretório /app
COPY --from=builder /app/dist /usr/share/nginx/html/app
# Copia os arquivos estáticos da pasta 'public' para a pasta /public
COPY ./public /usr/share/nginx/html/public
# Copia o arquivo de configuração do Nginx
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf