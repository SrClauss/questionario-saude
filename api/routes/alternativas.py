from flask import Blueprint, jsonify, request
from models import Alternativa
from extensions import db
from utils.auth import token_required
alternativas_bp = Blueprint('alternativas', __name__)

@alternativas_bp.route('/', methods=['GET'])
@alternativas_bp.route('/<int:page>/<int:per_page>/', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_alternativas(page=1, per_page=10):
    """
    Lista todas as alternativas com suporte a paginação.
    
    Args:
        page (int): Número da página (default: 1)
        per_page (int): Itens por página (default: 10)
    """
    try:
        alternativas = Alternativa.query.order_by(Alternativa.ordem).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        return jsonify([alternativa.to_json() for alternativa in alternativas.items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para obter uma alternativa específica
@alternativas_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_alternativa(id):
    """
    Obtém uma alternativa específica.
    """
    alternativa = Alternativa.query.get(id)
    if not alternativa:
        return jsonify({'error': 'Alternativa não encontrada'}), 404
    return jsonify(alternativa.to_json()), 200

# Rota para criar uma nova alternativa
@alternativas_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_alternativa():
    """
    Cria uma nova alternativa.
    """
    data = request.get_json()
    try:
        alternativa = Alternativa(
            pergunta_id=data['pergunta_id'],
            texto=data['texto'],
            valor=data['valor'],
            ordem=data['ordem']
        )
        db.session.add(alternativa)
        db.session.commit()
        return jsonify(alternativa.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para atualizar uma alternativa
@alternativas_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_alternativa(id):
    """
    Atualiza uma alternativa existente.
    """
    data = request.get_json()
    alternativa = Alternativa.query.get(id)
    if not alternativa:
        return jsonify({'error': 'Alternativa não encontrada'}), 404
    try:
        alternativa.pergunta_id = data['pergunta_id']
        alternativa.texto = data['texto']
        alternativa.valor = data['valor']
        alternativa.ordem = data['ordem']
        db.session.commit()
        return jsonify(alternativa.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para deletar uma alternativa
@alternativas_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_alternativa(id):
    """
    Deleta uma alternativa existente.
    """
    alternativa = Alternativa.query.get(id)
    if not alternativa:
        return jsonify({'error': 'Alternativa não encontrada'}), 404
    try:
        db.session.delete(alternativa)
        db.session.commit()
        return '', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

