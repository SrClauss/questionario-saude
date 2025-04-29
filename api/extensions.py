from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
import ulid

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def init_db():
    """
    Inicializa o banco de dados e cria um usuário admin se não existir
    """
    from models import User, Colaborador

    # Cria todas as tabelas
    db.create_all()

    # Verifica se já existe um usuário admin
    admin = User.query.filter_by(email='admin@admin.com').first()
    if not admin:
        # Cria o usuário admin
        admin = User(
            id=str(ulid.ULID()),
            email='admin@admin.com',
            password_hash=generate_password_hash('admin'),
            role='admin',
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(admin)

        # Cria o perfil de colaborador para o admin
        colaborador = Colaborador(
            id=str(ulid.ULID()),
            user_id=admin.id,
            nome='Administrador',
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(colaborador)

        try:
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário admin: {e}")
