from flask import Blueprint, request, jsonify
from models import BateriaTestes, ProfissionalSaude, Paciente, Questionario
from extensions import db
from datetime import datetime
from utils.auth import token_required
from sqlalchemy import exc

bateria_testes_bp = Blueprint('baterias_testes', 'baterias_testes')

# Rota para listar todas as baterias de testes
@bateria_testes_bp.route('', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_testes():
    """
    Lista todas as baterias de testes.
    """
    baterias = BateriaTestes.query.all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para criar uma nova bateria de testes
@bateria_testes_bp.route('', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_bateria_teste():
    """
    Cria uma nova bateria de testes.
    """
    data = request.get_json()
    try:
        # Converte data_aplicacao para datetime.date
        data_aplicacao = datetime.strptime(data['data_aplicacao'], '%Y-%m-%d').date()

        bateria = BateriaTestes(
            profissional_saude_id=data['profissional_saude_id'],
            paciente_id=data['paciente_id'],
            colaborador_id=data.get('colaborador_id'),
            questionario_id=data['questionario_id'],
            data_aplicacao=data_aplicacao,
            respostas=data.get('respostas'),
            observacoes=data.get('observacoes'),
            is_completo=data.get('is_completo', False)
        )
        db.session.add(bateria)
        db.session.commit()
        return jsonify(bateria.to_json()), 201
    except Exception as e:
        print(f"Erro ao criar bateria de testes: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para obter uma bateria de testes pelo ID
@bateria_testes_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_bateria_teste(id):
    """
    Retorna uma bateria de testes pelo ID.
    """
    bateria = BateriaTestes.query.get(id)
    if not bateria:
        return jsonify({'error': 'Bateria de testes não encontrada'}), 404
    return jsonify(bateria.to_json()), 200

# Rota para atualizar uma bateria de testes
@bateria_testes_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_bateria_teste(id):
    """
    Atualiza uma bateria de testes.
    """
    data = request.get_json()
    try:
        bateria = BateriaTestes.query.get(id)
        if not bateria:
            return jsonify({'error': 'Bateria de testes não encontrada'}), 404

        # Converte data_aplicacao para datetime.date
        data_aplicacao = datetime.strptime(data['data_aplicacao'], '%Y-%m-%d').date()

        bateria.profissional_saude_id = data['profissional_saude_id']
        bateria.paciente_id = data['paciente_id']
        bateria.colaborador_id = data.get('colaborador_id')
        bateria.questionario_id = data['questionario_id']
        bateria.data_aplicacao = data_aplicacao
        bateria.respostas = data.get('respostas')
        bateria.observacoes = data.get('observacoes')
        bateria.is_completo = data.get('is_completo', bateria.is_completo)

        db.session.commit()
        return jsonify(bateria.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para excluir uma bateria de testes
@bateria_testes_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_bateria_teste(id):
    """
    Exclui uma bateria de testes.
    """
    try:
        bateria = BateriaTestes.query.get(id)
        if not bateria:
            return jsonify({'error': 'Bateria de testes não encontrada'}), 404

        db.session.delete(bateria)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para listar baterias de testes por paciente
@bateria_testes_bp.route('/paciente/<paciente_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente'])
def get_baterias_by_paciente(paciente_id):
    """
    Lista todas as baterias de testes de um paciente específico.
    """
    baterias = BateriaTestes.query.filter_by(paciente_id=paciente_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para listar baterias de testes por profissional de saúde
@bateria_testes_bp.route('/profissional/<profissional_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_profissional(profissional_id):
    """
    Lista todas as baterias de testes de um profissional de saúde específico.
    """
    baterias = BateriaTestes.query.filter_by(profissional_saude_id=profissional_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para listar baterias de testes por colaborador
@token_required(roles=['admin', 'profissional_saude'])
@bateria_testes_bp.route('/colaborador/<colaborador_id>', methods=['GET'])
def get_baterias_by_colaborador(colaborador_id):
    """
    Lista todas as baterias de testes de um colaborador específico.
    """
    baterias = BateriaTestes.query.filter_by(colaborador_id=colaborador_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para listar baterias de testes por questionário
@bateria_testes_bp.route('/questionario/<questionario_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_questionario(questionario_id):
    """
    Lista todas as baterias de testes de um questionário específico.
    """
    baterias = BateriaTestes.query.filter_by(questionario_id=questionario_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para salvar várias baterias de testes em lote
@bateria_testes_bp.route('/batch_save', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def batch_save_baterias_testes():
    """
    Salva várias baterias de testes em lote (bulk operation).
    payload:
    {
        profissional_saude_id: ulid,
        baterias: [
            {
                paciente_id: ulid,
                colaborador_id: ulid,
                questionario_id: ulid,
                data_aplicacao: 'YYYY-MM-DD',
                respostas: {},
                observacoes: '',
                is_completo: true
            },
            ...
        ]
    }
    """
    data = request.get_json()
    baterias = []
    
    # Validar profissional_saude_id no payload principal
    profissional_saude_id = data.get('profissional_saude_id')
    if not profissional_saude_id:
        return jsonify({'error': 'profissional_saude_id é obrigatório'}), 400
    
    try:
        # Iterar sobre a lista de baterias, não sobre o objeto principal
        for item in data.get('baterias', []):
            
            # Converte data_aplicacao para datetime.date
            data_aplicacao = datetime.strptime(item['data_aplicacao'], '%Y-%m-%d').date()

            bateria = BateriaTestes(
                profissional_saude_id=profissional_saude_id,
                paciente_id=item['paciente_id'],
                colaborador_id=item.get('colaborador_id'),
                questionario_id=item['questionario_id'],
                data_aplicacao=data_aplicacao,
                respostas=item.get('respostas'),
                observacoes=item.get('observacoes'),
                is_completo=item.get('is_completo', False)
            )
            
            baterias.append(bateria)

        db.session.bulk_save_objects(baterias)
        db.session.commit()
        return jsonify({'message': 'Baterias de testes salvas com sucesso'}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Erro de valor: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



@bateria_testes_bp.route('/ensure_perfil_de_saude', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente'])
def ensure_perfil_de_saude():
    """
    Garante que o usuário tenha um perfil de saúde associado.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id é obrigatório'}), 400
    
    paciente = Paciente.query.filter_by(user_id=user_id).first()
    
    perfil_saude = Questionario.query.filter_by(title='Perfil de Saúde').first()
    if not perfil_saude:
        return jsonify({'error': 'Perfil de Saúde não encontrado'}), 404