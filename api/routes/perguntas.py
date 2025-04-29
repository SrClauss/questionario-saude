from flask import Blueprint, request, jsonify
from models import Pergunta
from extensions import db
from sqlalchemy.orm import joinedload
from utils.auth import token_required

perguntas_bp = Blueprint('perguntas', __name__)


# Rota para listar todas as perguntas
@perguntas_bp.route('/', methods=['GET'])
@perguntas_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_perguntas(page=1, len=10):
    """
    Lista todas as perguntas com paginação.
    """
    try:
        page = int(page)
        len = int(len)
        perguntas = Pergunta.query.paginate(page=page, per_page=len, error_out=False)
        return jsonify([pergunta.to_json() for pergunta in perguntas.items]), 200
    except Exception as e:
        print(f"Erro ao listar perguntas: {e}")
        return jsonify({'error': str(e)}), 500

@perguntas_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_pergunta(id):
    """
    Retorna uma pergunta pelo ID.
    """
    pergunta = Pergunta.query.get(id)
    if not pergunta:
        return jsonify({'error': 'Pergunta não encontrada'}), 404
    return jsonify(pergunta.to_json()), 200

@perguntas_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_pergunta():
    """
    Cria uma nova pergunta.
    """
    data = request.get_json()
    try:
        pergunta = Pergunta(
            texto=data['texto'],
            sessao_id=data['sessao_id'],
            tipo_resposta=data.get('tipo_resposta', 'multipla_escolha'),
            ordem=data.get('ordem', 0)
        )
        db.session.add(pergunta)
        db.session.commit()
        return jsonify(pergunta.to_json()), 201
    except Exception as e:
        print(f"Erro ao criar pergunta: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@perguntas_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_pergunta(id):
    """
    Atualiza uma pergunta.
    """
    data = request.get_json()
    try:
        pergunta = Pergunta.query.get(id)
        if not pergunta:
            return jsonify({'error': 'Pergunta não encontrada'}), 404

        pergunta.texto = data['texto']
        pergunta.sessao_id = data['sessao_id']  # Corrigido para usar sessao_id
        pergunta.tipo_resposta = data.get('tipo_resposta', pergunta.tipo_resposta)
        pergunta.ordem = data.get('ordem', pergunta.ordem)
        
        db.session.commit()
        return jsonify(pergunta.to_json()), 200
    except Exception as e:
        print(f"Erro ao atualizar pergunta: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@perguntas_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_pergunta(id):
    """
    Deleta uma pergunta.
    """
    try:
        pergunta = Pergunta.query.get(id)
        if not pergunta:
            return jsonify({'error': 'Pergunta não encontrada'}), 404

        db.session.delete(pergunta)
        db.session.commit()
        return '', 204  # Retorna 204 (No Content)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rotas adicionais úteis
@perguntas_bp.route('/sessao/<sessao_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_perguntas_by_sessao(sessao_id):
    """
    Lista todas as perguntas de uma sessão específica.
    """
    try:
        perguntas = Pergunta.query.filter_by(sessao_id=sessao_id).all()
        return jsonify([pergunta.to_json() for pergunta in perguntas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@perguntas_bp.route('/<id>/alternativas', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_alternativas_by_pergunta(id):
    """
    Lista todas as alternativas de uma pergunta específica.
    """
    try:
        from models import Alternativa
        alternativas = Alternativa.query.filter_by(pergunta_id=id).all()
        return jsonify([alternativa.to_json() for alternativa in alternativas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Rota detailed paginada que carrega todas as perguntas com suas alternativas
@perguntas_bp.route('/detailed', methods=['GET'])
@perguntas_bp.route('/detailed/<int:page>/<int:len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_perguntas_detailed(page=1, len=10):
    """
    Lista todas as perguntas com todas as alternativas utilizando joinedload para carregamento otimizado.
    """
    try:
        perguntas_pag = Pergunta.query.options(joinedload(Pergunta.alternativas)).paginate(page=page, per_page=len, error_out=False)
        resultado = []
        for pergunta in perguntas_pag.items:
            pergunta_json = pergunta.to_json()
            pergunta_json['alternativas'] = [alt.to_json() for alt in pergunta.alternativas]
            resultado.append(pergunta_json)
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro ao listar perguntas detalhadas: {e}")
        return jsonify({'error': str(e)}), 500

# Rota detailed que retorna uma pergunta por ID com todas as alternativas
@perguntas_bp.route('/detailed/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def  get_pergunta_detailed(id):
    """
    Retorna uma pergunta específica (por ID) com todas as alternativas utilizando joinedload.
    """
    try:
        pergunta = Pergunta.query.options(joinedload(Pergunta.alternativas)).get(id)
        if not pergunta:
            return jsonify({'error': 'Pergunta não encontrada'}), 404
        pergunta_json = pergunta.to_json()
        pergunta_json['alternativas'] = [alt.to_json() for alt in pergunta.alternativas]
        return jsonify(pergunta_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500