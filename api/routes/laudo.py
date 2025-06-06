from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import CID, Laudo, Paciente, Medico, User
from extensions import db
from utils.auth import token_required
from flask import current_app
import unidecode

laudo_bp = Blueprint('laudo', __name__, url_prefix='/laudos')

# Rota para criar um novo laudo
@laudo_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'medico'])
def create_laudo():
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota / (create_laudo): {data}")
    try:
        # Verificar se o paciente existe
        paciente = Paciente.query.get(data['paciente_id'])
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        # Verificar se o médico existe
        medico = Medico.query.get(data['medico_id'])
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        novo_laudo = Laudo(
            paciente_id=data['paciente_id'],
            medico_id=data['medico_id'],
            data_emissao=datetime.strptime(data['data_emissao'], '%Y-%m-%d'),
            conteudo=data['conteudo'],
            status=data.get('status', 'emitido') # Default status
        )
        db.session.add(novo_laudo)
        db.session.commit()
        return jsonify(novo_laudo.to_json()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar laudo. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400

# Rota para obter todos os laudos
@laudo_bp.route('/', methods=['GET'])
@laudo_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_laudos(page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pagination = Laudo.query.paginate(page=page, per_page=len, error_out=False)
        items = [laudo.to_json() for laudo in pagination.items]
        totalPages = pagination.pages
        return jsonify({
            "items": items,
            "totalPages": totalPages
        }), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter laudos. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Rota para obter um laudo específico pelo ID
@laudo_bp.route('/<int:laudo_id>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_laudo(laudo_id):
    try:
        laudo = Laudo.query.get(laudo_id)
        if not laudo:
            return jsonify({'error': 'Laudo não encontrado'}), 404
        return jsonify(laudo.to_json()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter laudo com ID {laudo_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
# Rota para atualizar um laudo
@laudo_bp.route('/<int:laudo_id>', methods=['PUT'])
@token_required(roles=['admin', 'medico'])
def update_laudo(laudo_id):
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota PUT /{laudo_id} (update_laudo): {data}")
    try:
        laudo = Laudo.query.get(laudo_id)
        if not laudo:
            return jsonify({'error': 'Laudo não encontrado'}), 404

        # Verificar se o paciente existe (se fornecido)
        if 'paciente_id' in data:
            paciente = Paciente.query.get(data['paciente_id'])
            if not paciente:
                return jsonify({'error': 'Paciente não encontrado'}), 404
            laudo.paciente_id = data['paciente_id']

        # Verificar se o médico existe (se fornecido)
        if 'medico_id' in data:
            medico = Medico.query.get(data['medico_id'])
            if not medico:
                return jsonify({'error': 'Médico não encontrado'}), 404
            laudo.medico_id = data['medico_id']

        if 'data_emissao' in data:
            laudo.data_emissao = datetime.strptime(data['data_emissao'], '%Y-%m-%d')
        if 'conteudo' in data:
            laudo.conteudo = data['conteudo']
        if 'status' in data:
            laudo.status = data['status']

        db.session.commit()
        return jsonify(laudo.to_json()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar laudo com ID {laudo_id}. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
# Rota para deletar um laudo
@laudo_bp.route('/<int:laudo_id>', methods=['DELETE'])
@token_required(roles=['admin', 'medico'])
def delete_laudo(laudo_id):
    try:
        laudo = Laudo.query.get(laudo_id)
        if not laudo:
            return jsonify({'error': 'Laudo não encontrado'}), 404

        db.session.delete(laudo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar laudo com ID {laudo_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Rota para obter laudos por paciente_id
@laudo_bp.route('/paciente/<int:paciente_id>', methods=['GET'])
@laudo_bp.route('/paciente/<int:paciente_id>/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_laudos_by_paciente(paciente_id, page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pagination = Laudo.query.filter_by(paciente_id=paciente_id).paginate(page=page, per_page=len, error_out=False)
        items = [laudo.to_json() for laudo in pagination.items]
        totalPages = pagination.pages
        return jsonify({
            "items": items,
            "totalPages": totalPages
        }), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter laudos para paciente {paciente_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Rota para obter laudos por medico_id
@laudo_bp.route('/medico/<int:medico_id>', methods=['GET'])
@laudo_bp.route('/medico/<int:medico_id>/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_laudos_by_medico(medico_id, page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pagination = Laudo.query.filter_by(medico_id=medico_id).paginate(page=page, per_page=len, error_out=False)
        items = [laudo.to_json() for laudo in pagination.items]
        totalPages = pagination.pages
        return jsonify({
            "items": items,
            "totalPages": totalPages
        }), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter laudos para médico {medico_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
#rota para obter o laudo pela avalicacao
@laudo_bp.route('/avaliacao/<int:avaliacao_id>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_laudo_by_avaliacao(avaliacao_id):
    try:
        laudo = Laudo.query.filter_by(avaliacao_id=avaliacao_id).first()
        if not laudo:
            return jsonify({'error': 'Laudo não encontrado para esta avaliação'}), 404
        return jsonify(laudo.to_json()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter laudo para avaliação {avaliacao_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
        
@laudo_bp.route('/get_cid_by_description/<string:substring>', methods=['GET'])
def get_cid_by_description(substring):
    try:
        cids = CID.query.filter(CID.unidecode_descricao.contains(unidecode.unidecode(substring.lower()))).all()
        return jsonify([cid.to_json() for cid in cids]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter CIDs com substring {substring}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@laudo_bp.route("/get_disease_by_cid/<string:cid_id>", methods=["GET"])
def get_disease_by_cid(cid_id):
    try:
        cid = CID.query.get(cid_id)
        if not cid:
            return jsonify({'error': 'CID não encontrada'}), 404
        return jsonify(cid.to_json()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter CID {cid_id}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500