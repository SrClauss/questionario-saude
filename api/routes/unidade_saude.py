from models import UnidadeSaude
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from extensions import db
from flask import current_app
from utils.auth import token_required

unidade_saude_bp = Blueprint('unidade_saude', __name__, url_prefix='/unidades_saude')

# Rota para obter todas as unidades de saúde
@unidade_saude_bp.route('/', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_unidades_saude():
    try:
        unidades = UnidadeSaude.query.all()
        return jsonify([unidade.to_json() for unidade in unidades]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter unidades de saúde: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Rota para criar uma nova unidade de saúde
@unidade_saude_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def create_unidade_saude():
    data = request.get_json()
    print(data)
    current_app.logger.debug(f"Dados recebidos na rota / (create_unidade_saude): {data}")
    try:
        unidade = UnidadeSaude(
            nome=data['nome'],
            cnpj=data['cnpj'],
            endereco=data['endereco'],
            telefone=data.get('telefone'),
            email=data.get('email')
        )
        db.session.add(unidade)
        db.session.commit()
        return jsonify(unidade.to_json()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar unidade de saúde. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400

# Rota para obter uma unidade de saúde pelo ID
@unidade_saude_bp.route('/<int:id>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_unidade_saude(id):
    try:
        unidade = UnidadeSaude.query.get(id)
        if not unidade:
            return jsonify({'error': 'Unidade de saúde não encontrada'}), 404
        return jsonify(unidade.to_json()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter unidade de saúde com ID {id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Rota para atualizar uma unidade de saúde
@unidade_saude_bp.route('/<int:id>', methods=['PUT'])
@token_required(roles=['admin'])
def update_unidade_saude(id):
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota /<id> (update_unidade_saude) para ID {id}: {data}")
    try:
        unidade = UnidadeSaude.query.get(id)
        if not unidade:
            return jsonify({'error': 'Unidade de saúde não encontrada'}), 404

        unidade.nome = data.get('nome', unidade.nome)
        unidade.endereco = data.get('endereco', unidade.endereco)
        unidade.telefone = data.get('telefone', unidade.telefone)
        unidade.email = data.get('email', unidade.email)

        db.session.commit()
        return jsonify(unidade.to_json()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar unidade de saúde com ID {id}. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400

# Rota para deletar uma unidade de saúde
@unidade_saude_bp.route('/<string:id>', methods=['DELETE'])
@token_required(roles=['admin'])
def delete_unidade_saude(id):
    try:
        unidade = UnidadeSaude.query.get(id)
        if not unidade:
            return jsonify({'error': 'Unidade de saúde não encontrada'}), 404

        db.session.delete(unidade)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar unidade de saúde com ID {id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
        
# Rota para obter unidades de saúde por nome
@unidade_saude_bp.route('/filter_by_name/<name>', methods=['GET'])
@unidade_saude_bp.route('/filter_by_name/<name>/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'paciente'])
def get_unidades_saude_by_name(name, page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pagination = UnidadeSaude.query.filter(UnidadeSaude.nome.ilike(f'%{name}%')).paginate(
            page=page,
            per_page=len,
            error_out=False)
        items = [unidade.to_json() for unidade in pagination.items]
        totalPages = pagination.pages
        return jsonify({
            "items": items,
            "totalPages": totalPages
        }), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao obter unidades de saúde por nome '{name}': {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

