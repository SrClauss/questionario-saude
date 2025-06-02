
from flask import Blueprint, request, jsonify
from models import Avaliacao, BateriaTestes, Paciente, Questionario, UnidadeSaude, Medico
from extensions import db
from datetime import datetime
from utils.auth import token_required
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import exc

avaliacao_bp = Blueprint('avaliacoes', __name__, url_prefix='/avaliacoes')

# Rota para criar uma nova avaliação
@avaliacao_bp.route('', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_avaliacao():
    """
    Cria uma nova avaliação.
    """
    data = request.get_json()
    print(data) 
    try:
        data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()

        avaliacao = Avaliacao(
           paciente_id = data['paciente_id'],
           unidade_saude_id = data['unidade_saude_id'],
           data_inicio = data_inicio,
           
       )
        db.session.add(avaliacao)
        db.session.commit()
        return jsonify(avaliacao.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para obter uma avaliação pelo ID
@avaliacao_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_avaliacao(id):
    """
    Retorna uma avaliação pelo ID.
    """
    avaliacao = Avaliacao.query.get(id)
    if not avaliacao:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    return jsonify(avaliacao.to_json()), 200
# Rota para atualizar uma avaliação
@avaliacao_bp.route('/set_medico/<avaliacao_id>/<medico_id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def set_medico(avaliacao_id, medico_id):
    """
    Atualiza o médico de uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            
            return jsonify({'error': 'Avaliação não encontrada'}), 404
        
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico nao encontrado'}), 404
        
        avaliacao.medico_id = medico_id
        db.session.commit()
        return jsonify(avaliacao.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
        

        
        
# Rota para excluir uma avaliação
@avaliacao_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_avaliacao(id):
    """
    Exclui uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404

        db.session.delete(avaliacao)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@avaliacao_bp.route('/por_nome_paciente/<nome_paciente>', methods=['GET']) # Mantido conforme sua preferência, embora uma rota mais específica como /por_nome_paciente/ seja comum
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_avaliacoes_by_paciente(nome_paciente):
    """
    Lista todas as avaliações de um paciente específico pelo nome (busca parcial).
    """
    try:
        # Encontra o paciente pelo nome (case-insensitive)
        paciente = Paciente.query.filter(Paciente.nome.ilike(f'%{nome_paciente}%')).first()
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        # Busca todas as avaliações associadas a este paciente
        avaliacoes = Avaliacao.query.filter_by(paciente_id=paciente.id).all()

        if not avaliacoes:
            return jsonify({'message': 'Nenhuma avaliação encontrada para este paciente.'}), 404

        return jsonify([avaliacao.to_json() for avaliacao in avaliacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
# Rota para obter as baterias de testes de uma avaliação específica
@avaliacao_bp.route('/baterias_testes/<id>')
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_baterias_by_avaliacao(id):
    """
    Lista todas as baterias de testes associadas a uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404

        baterias = avaliacao.baterias_testes
        return jsonify([bateria.to_json() for bateria in baterias]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter avaliações por unidade de saúde
@avaliacao_bp.route('/por_unidade_saude/<id>', methods=['GET']) # Mantido conforme sua preferência
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_avaliacoes_by_unidade_saude(id):
    """
    Lista todas as avaliações de uma unidade de saúde específica.
    """
    try:
        unidade_saude = UnidadeSaude.query.get(id)
        if not unidade_saude:
            return jsonify({'error': 'Unidade de saúde não encontrada'}), 404

        avaliacoes = Avaliacao.query.filter_by(unidade_saude_id=id).all()
        return jsonify([avaliacao.to_json() for avaliacao in avaliacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter avaliações completas por ID do paciente
@avaliacao_bp.route('/paciente/<paciente_id>', methods=['GET']) # Nome da rota mantido conforme solicitado
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente']) # Adicionado 'paciente' para permitir que vejam suas próprias avaliações
def get_avaliacoes_completas_by_paciente_id(paciente_id):
    """
    Lista todas as avaliações de um paciente específico pelo ID,
    incluindo suas baterias de testes e os respectivos questionários.
    """
    try:
        result = []
        # Eager load related data to reduce database queries
        avaliacoes = Avaliacao.query.options(
            selectinload(Avaliacao.baterias_testes).selectinload(BateriaTestes.questionario), # Carrega baterias e seus questionários
            joinedload(Avaliacao.medico),
            joinedload(Avaliacao.unidade_saude),
            joinedload(Avaliacao.paciente) # Carrega o paciente diretamente da avaliação
        ).filter_by(paciente_id=paciente_id).all()

        if not avaliacoes:
            paciente = Paciente.query.get(paciente_id)
            return jsonify(paciente.to_json()), 404
        

        for avaliacao in avaliacoes:
            
            lista_baterias_json = []
            for bateria in avaliacao.baterias_testes: # Acessa as baterias já carregadas
                bateria_json = bateria.to_json()
                if bateria.questionario: # Verifica se o questionário existe (já carregado)
                    bateria_json['questionario'] = bateria.questionario.to_json()
                else:
                    bateria_json['questionario'] = None
                lista_baterias_json.append(bateria_json)
            
            complete_obj = {
                "avaliacao": avaliacao.to_json(),
                "baterias_testes": lista_baterias_json,
                "medico": avaliacao.medico.to_json() if avaliacao.medico else None,
                "unidade_saude": avaliacao.unidade_saude.to_json() if avaliacao.unidade_saude else None,
                "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None
            }
            result.append(complete_obj)
            
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Ocorreu um erro interno ao processar a solicitação.'}), 500
    

            
            