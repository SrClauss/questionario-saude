# Use uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da API
COPY . .

# Expõe a porta que o Flask/Gunicorn vai usar e inicia o servidor
EXPOSE 5000
# O formato é "nome_do_arquivo_wsgi:nome_da_variavel_app".
# Assumindo que seu arquivo é wsgi.py e a variável é 'app'.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]