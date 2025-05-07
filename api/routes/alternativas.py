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

@alternativas_bp.route('/batch', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_alternativas_batch():
    """
    Atualiza uma lista de alternativas em batch sem uso de loop explícito.
    O payload recebido pode conter campos extras (ex: created_at, updated_at)
    que serão removidos. Exemplo de payload:
    [
        {
            "id": "01JS0F7WVMS1033WG0HJ66FQ3A",
            "pergunta_id": "01JS0F7WV8PN6YQA3P3WKEBNFE",
            "texto": "Sim",
            "valor": 10,
            "ordem": 1,
            "created_at": "2025-04-16T23:34:11.572450",
            "updated_at": "2025-04-16T23:34:11.572450"
        },
        {
            "id": "01JS0F7WVTTFMV2JH71ZCCVNTF",
            "pergunta_id": "01JS0F7WV8PN6YQA3P3WKEBNFE",
            "texto": "Não",
            "valor": 0,
            "ordem": 2,
            "created_at": "2025-04-16T23:34:11.578455",
            "updated_at": "2025-04-16T23:34:11.578455"
        }
    ]
    """
    data = request.get_json()
    print(data)
    if not isinstance(data, list):
        return jsonify({'error': 'O payload deve ser uma lista de alternativas'}), 400

    try:
        # Filtra os campos permitidos pelo modelo: id, pergunta_id, texto, valor, ordem
        allowed_fields = {"id", "pergunta_id", "texto", "valor", "ordem"}
        mappings = [{ key: alt[key] for key in alt if key in allowed_fields } for alt in data ]
        db.session.bulk_update_mappings(Alternativa, mappings)
        db.session.commit()
        return jsonify({'message': 'Alternativas atualizadas com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
