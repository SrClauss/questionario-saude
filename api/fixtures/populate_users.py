from faker import Faker
from models import User, Paciente
from extensions import db
from datetime import datetime, timezone
import ulid
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

fake = Faker('pt_BR')

def gerar_email_unico_no_lote(nome_completo, existing_emails_in_batch):
    """Gera um email único para o lote atual, adicionando um contador se necessário."""
    partes = nome_completo.lower().split()
    base_email_parts = []

    if len(partes) >= 1:
        base_email_parts.append(partes[0].replace('.', '').replace(',', ''))
    if len(partes) >= 2:
        base_email_parts.append(partes[1].replace('.', '').replace(',', ''))
    if len(partes) >= 3:
        base_email_parts.append(partes[2].replace('.', '').replace(',', ''))
    
    while len(base_email_parts) < 3:
        base_email_parts.append(fake.last_name().lower().replace(" ", "").replace('.', '').replace(',', ''))

    base_name = "_".join(base_email_parts[:3])
    
    email_candidate = f"{base_name}@faker.com"
    counter = 1
    while email_candidate in existing_emails_in_batch:
        email_candidate = f"{base_name}{counter}@faker.com"
        counter += 1
    return email_candidate

def gerar_cpf_unico_no_lote(existing_cpfs_in_batch, nome_paciente_para_log, indice_paciente_para_log, max_tentativas_geracao_cpf):
    """
    Gera um CPF único que não está no conjunto existing_cpfs_in_batch.
    Retorna o CPF único ou None se falhar após max_tentativas_geracao_cpf.
    """
    for attempt_num in range(max_tentativas_geracao_cpf):
        cpf_candidate = fake.cpf().replace('.', '').replace('-', '')
        if cpf_candidate not in existing_cpfs_in_batch:
            return cpf_candidate # CPF único encontrado
    
    # Se chegou aqui, todas as tentativas falharam
    logger.warning(
        f"Não foi possível gerar um CPF único para {nome_paciente_para_log} "
        f"(paciente índice {indice_paciente_para_log + 1}) após {max_tentativas_geracao_cpf} tentativas. "
        f"Este registro será pulado na fase de geração."
    )
    return None

def popular_pacientes(qtd=500):
    logger.info(f"Iniciando o processo de popular {qtd} pacientes.")
    
    pacientes_data_list = []
    generated_cpfs_batch = set()
    generated_emails_batch = set()

    logger.info("Fase 1: Geração de dados únicos em memória para o lote.")
    for i in range(qtd):
        nome = fake.name()
        
        # Gerar email único para o lote
        email = gerar_email_unico_no_lote(nome, generated_emails_batch)
        generated_emails_batch.add(email)

        # Gerar CPF único para o lote usando a função helper
        # O limite de tentativas é por paciente, para evitar loops infinitos na geração do lote.
        max_tentativas_cpf_por_paciente = qtd * 2 # Ajuste conforme necessário, ex: 2x a quantidade de pacientes
        cpf = gerar_cpf_unico_no_lote(generated_cpfs_batch, nome, i, max_tentativas_cpf_por_paciente)
        
        if not cpf: 
            # O log de aviso já foi feito dentro de gerar_cpf_unico_no_lote.
            continue
        generated_cpfs_batch.add(cpf) # Adiciona o CPF (que é único no lote) ao set.

        data_nascimento = fake.date_of_birth(minimum_age=0, maximum_age=90)
        telefone = fake.phone_number()
        enderecos = [{
            "id": str(ulid.ULID()),
            "logradouro": fake.street_name(),
            "numero": fake.building_number(),
            "complemento": "CASA",
            "bairro": fake.bairro(),
            "cidade": fake.city(),
            "estado": fake.estado_sigla(),
            "cep": fake.postcode().replace('-', '')
        }]

        pacientes_data_list.append({
            "user_data": {
                "email": email,
                "role": 'paciente',
                "is_active": True,
                "password": 'faker' # Senha padrão para dados de teste
            },
            "paciente_data": {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "telefone": telefone,
                "cpf": cpf,
                "enderecos": enderecos,
            }
        })

        if (i + 1) % (max(1, qtd // 20)) == 0: # Log de progresso a cada 5%
            logger.info(f"Gerados {i + 1}/{qtd} conjuntos de dados de pacientes para o lote.")

    logger.info(f"Fase 1 concluída. {len(pacientes_data_list)} conjuntos de dados de pacientes foram gerados em memória.")

    if not pacientes_data_list:
        logger.info("Nenhum dado de paciente foi gerado. Encerrando.")
        return

    users_to_insert = []
    pacientes_to_insert = []
    
    # Lista para manter a correspondência entre usuário e dados do paciente
    # [(user_obj, paciente_data_dict), ...]
    user_paciente_mapping = [] 

    logger.info("Fase 2: Preparando objetos User para inserção em lote.")
    for data_item in pacientes_data_list:
        user = User(
            email=data_item["user_data"]["email"],
            role=data_item["user_data"]["role"],
            is_active=data_item["user_data"]["is_active"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        user.set_password(data_item["user_data"]["password"])
        users_to_insert.append(user)
        user_paciente_mapping.append((user, data_item["paciente_data"]))

    try:
        logger.info(f"Adicionando {len(users_to_insert)} usuários à sessão.")
        db.session.add_all(users_to_insert)
        logger.info("Realizando flush para obter IDs dos usuários.")
        db.session.flush() # Garante que os IDs dos usuários sejam atribuídos

        logger.info("Fase 3: Preparando objetos Paciente para inserção em lote.")
        for user_obj, paciente_data in user_paciente_mapping:
            paciente = Paciente(
                user_id=user_obj.id, # ID obtido após o flush
                nome=paciente_data['nome'],
                data_nascimento=paciente_data['data_nascimento'],
                telefone=paciente_data['telefone'],
                cpf=paciente_data['cpf'],
                enderecos=paciente_data['enderecos'],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            pacientes_to_insert.append(paciente)
        
        logger.info(f"Adicionando {len(pacientes_to_insert)} pacientes à sessão.")
        db.session.add_all(pacientes_to_insert)

        logger.info("Fase 4: Realizando commit final no banco de dados.")
        db.session.commit()
        logger.info(f"Sucesso! {len(pacientes_to_insert)} pacientes e seus usuários correspondentes foram criados e commitados.")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro durante a inserção em lote no banco de dados: {e}", exc_info=True)
        logger.error("Rollback realizado. Nenhuma alteração foi salva no banco de dados nesta tentativa.")
    finally:
        db.session.close()
        logger.info("Sessão do banco de dados fechada.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        popular_pacientes()