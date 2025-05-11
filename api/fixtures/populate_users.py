from faker import Faker
from models import User, Paciente
from extensions import db
from datetime import datetime, timezone
import ulid

fake = Faker('pt_BR')

def gerar_email(nome_completo):
    partes = nome_completo.lower().split()
    if len(partes) < 3:
        partes += [fake.last_name() for _ in range(3 - len(partes))]
    return f"{partes[0]}_{partes[1]}_{partes[2]}@faker.com"

def popular_pacientes(qtd=50):
    for _ in range(qtd):
        nome = fake.name()
        email = gerar_email(nome)
        cpf = fake.unique.cpf().replace('.', '').replace('-', '')
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=90)
        telefone = fake.phone_number()
        enderecos = [{
            "id": str(ulid.ULID()),
            "logradouro": fake.street_name(),
            "numero": fake.building_number(),
            "complemento": "AP01",
            "bairro": fake.bairro(),
            "cidade": fake.city(),
            "estado": fake.estado_sigla(),
            "cep": fake.postcode().replace('-', '')
        }]
        # Cria o usuário
        user = User(
            email=email,
            role='paciente',
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        user.set_password('faker')
        db.session.add(user)
        db.session.flush()  # Garante user.id

        # Cria o paciente
        paciente = Paciente(
            nome=nome,
            data_nascimento=data_nascimento,
            telefone=telefone,
            cpf=cpf,
            enderecos=enderecos,
            user_id=user.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(paciente)
    db.session.commit()
    print(f"{qtd} pacientes e usuários criados com sucesso.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        popular_pacientes()