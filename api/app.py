from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from extensions import db, login_manager, mail
from sqlalchemy import inspect
from flask import jsonify, request
from flask_cors import CORS
import logging



# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def create_app():
    # Mude a configuração do static_url_path para vazio
    app = Flask(__name__, static_folder="static/", static_url_path="")
    
    app.url_map.strict_slashes = False  # Permite rotas com e sem barra no final
    
    CORS(app)  # Permite CORS para todas as rotas que começam com /backend
    # Configurações do aplicativo
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
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
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}  # Extensões permitidas
    app.config['PERFIL_DE_SAUDE'] = os.getenv('PERFIL_DE_SAUDE')

    # Cria o diretório de upload se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # Inicializa o Flask-Mail com o app

    
    
    #inicializa o flask migrate
    migrate = Migrate(app, db)
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
    from routes.medico import medico_bp
    from routes.avaliacao import avaliacao_bp
    from routes.unidade_saude import unidade_saude_bp
    from routes.laudo import laudo_bp
    from routes.exames import exame_bp
    
    app.register_blueprint(user_bp, url_prefix='/backend/user', name='user_bp')
    app.register_blueprint(profissional_saude_bp, url_prefix='/backend/profissionais_saude', name='profissional_saude_bp')
    app.register_blueprint(paciente_bp, url_prefix='/backend/pacientes', name='paciente_bp')
    app.register_blueprint(colaborador_bp, url_prefix='/backend/colaboradores', name='colaborador_bp')
    app.register_blueprint(questionario_bp, url_prefix='/backend/questionario', name='questionario_bp')
    app.register_blueprint(sessoes_bp, url_prefix='/backend/sessoes', name='sessoes_bp')
    app.register_blueprint(perguntas_bp, url_prefix='/backend/perguntas', name='perguntas_bp')
    app.register_blueprint(alternativas_bp, url_prefix='/backend/alternativas', name='alternativas_bp')
    app.register_blueprint(bateria_testes_bp, url_prefix='/backend/baterias_testes', name='bateria_testes_bp')
    app.register_blueprint(populate_bp, url_prefix='/backend/populate', name='populate_bp')
    app.register_blueprint(medico_bp, url_prefix='/backend/medicos', name='medico_bp')
    app.register_blueprint(avaliacao_bp, url_prefix='/backend/avaliacoes', name='avaliacao_bp')
    app.register_blueprint(unidade_saude_bp, url_prefix='/backend/unidades_saude', name='unidade_saude_bp')
    app.register_blueprint(laudo_bp, url_prefix='/backend/laudos', name='laudo_bp')
    app.register_blueprint(exame_bp, url_prefix='/backend/exames', name='exame_bp')
    
 
    @app.route('/backend/hello', methods=['GET'])
    def hello():
        """
        Rota simples para teste.
        """
        return jsonify({'message': 'Hello, world!'}), 200
        
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
