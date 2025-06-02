from faker import Faker
from models import User, Medico
from extensions import db
from datetime import datetime, timezone
import ulid

fake = Faker('pt_BR')

def gerar_email(nome_completo):
    partes = nome_completo.lower().split()
    if len(partes) < 3:
        partes += [fake.last_name() for _ in range(3 - len(partes))]
    return f"{partes[0]}_{partes[1]}_{partes[2]}@faker.com"

def popular_medicos(qtd=20):
    for _ in range(qtd):
        nome = fake.name()
        email = gerar_email(nome)
        crm = fake.unique.numerify(text='######')
        especialidade = fake.random_element(elements=('Pediatria', 'Neurologia Infantil', 'Psiquiatria Infantil', 'Genética Médica'))

        # Cria o usuário
        user = User(
            email=email,
            role='medico',
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        user.set_password('faker')
        db.session.add(user)
        db.session.flush()  # Garante user.id

        # Cria o médico
        medico = Medico(
            nome=nome,
            user_id=user.id,
            crm=crm,
            especialidade=especialidade,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(medico)
    db.session.commit()
    print(f"{qtd} médicos e usuários criados com sucesso.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        popular_medicos()
        
    
