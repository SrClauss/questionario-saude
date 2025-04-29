from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os
from extensions import db, login_manager, mail
from sqlalchemy import inspect
from flask import jsonify
from flask_cors import CORS
import logging

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app)  # Permite CORS para todas as rotas que começam com /backend
    # Configurações do aplicativo
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Diretório para salvar as imagens
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    # Cria o diretório de upload se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # Inicializa o Flask-Mail com o app

    # Configuração de logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = app.logger
    logger.setLevel(logging.DEBUG)

    with app.app_context():
        from extensions import init_db
        init_db()  # Inicializa o banco e cria usuário admin

    # Registrar blueprints
    from routes.user import user_bp
    from routes.profissional_saude import profissional_saude_bp
    from routes.paciente import paciente_bp
    from routes.colaborador import colaborador_bp
    from routes.questionario import questionario_bp
    from routes.sessoes import sessoes_bp
    from routes.perguntas import perguntas_bp
    from routes.alternativas import alternativas_bp
    from routes.bateria_testes import bateria_testes_bp
    from routes._populate import populate_bp
    
    
    app.register_blueprint(user_bp, url_prefix='/backend/user')
    app.register_blueprint(profissional_saude_bp, url_prefix='/backend/profissionais_saude')
    app.register_blueprint(paciente_bp, url_prefix='/backend/pacientes')
    app.register_blueprint(colaborador_bp, url_prefix='/backend/colaboradores')
    app.register_blueprint(questionario_bp, url_prefix='/backend/questionario')
    app.register_blueprint(sessoes_bp, url_prefix='/backend/sessoes')
    app.register_blueprint(perguntas_bp, url_prefix='/backend/perguntas')
    app.register_blueprint(alternativas_bp, url_prefix='/backend/alternativas')
    app.register_blueprint(bateria_testes_bp, url_prefix='/backend/baterias_testes')
    app.register_blueprint(populate_bp, url_prefix='/backend/populate')

    
    # Printar tabelas do banco de dados
    with app.app_context():
        db.create_all()
        
    return app


def list_routes(app):
    """
    Lista todas as rotas registradas no Flask.
    """
    for rule in app.url_map.iter_rules():
        print(f"Rota: {rule} -> Métodos: {', '.join(rule.methods)}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        list_routes(app)
    app.run(debug=True)
