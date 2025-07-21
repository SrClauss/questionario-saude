# Este arquivo é o ponto de entrada para o servidor Gunicorn.
# Ele importa a factory 'create_app' do seu arquivo principal e cria a instância da aplicação.
from app import create_app

app = create_app()