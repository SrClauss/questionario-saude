from flask import Blueprint, request, jsonify, current_app
from models import Questionario, Sessao, Pergunta, Alternativa
from extensions import db
from sqlalchemy.orm import joinedload
from utils.auth import token_required
questionario_bp = Blueprint('questionario', __name__)

# Rota para listar todos os questionários
@questionario_bp.route('/', methods=['GET'])
@questionario_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_questionarios(page=1, len=10):
    """
    Lista todos os questionários com paginação.
    """
    try:
        page = int(page)
        len = int(len)
        questionarios = Questionario.query.paginate(page=page, per_page=len, error_out=False)
        return jsonify([questionario.to_json() for questionario in questionarios.items]), 200
    except Exception as e:
        print(f"Erro ao listar questionários: {e}")
        return jsonify({'error': str(e)}), 500

# Rota para obter um questionário por ID
@questionario_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_questionario(id):
    """
    Retorna um questionário pelo ID.
    """
    questionario = Questionario.query.get(id)
    if not questionario:
        return jsonify({'error': 'Questionário não encontrado'}), 404
    return jsonify(questionario.to_json()), 200

# Rota para criar um novo questionário
@questionario_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_questionario():
    """
    Cria um novo questionário.
    """
    data = request.get_json()
    try:
        questionario = Questionario(
            titulo=data['titulo'],
            descricao=data.get('descricao', ''),
            versao=data.get('versao', '1.0'),
            fontes_literatura=data.get('fontes_literatura', None)
        )
        db.session.add(questionario)
        db.session.commit()
        return jsonify(questionario.to_json()), 201
    except Exception as e:
        print(f"Erro ao criar questionário: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para atualizar um questionário existente
@questionario_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_questionario(id):
    """
    Atualiza um questionário existente.
    """
    data = request.get_json()
    try:
        questionario = Questionario.query.get(id)
        if not questionario:
            return jsonify({'error': 'Questionário não encontrado'}), 404

        questionario.titulo = data['titulo']
        questionario.descricao = data.get('descricao', questionario.descricao)
        questionario.versao = data.get('versao', questionario.versao)
        questionario.fontes_literatura = data.get('fontes_literatura', questionario.fontes_literatura)
        questionario.is_active = data.get('is_active', questionario.is_active)

        db.session.commit()
        return jsonify(questionario.to_json()), 200
    except Exception as e:
        print(f"Erro ao atualizar questionário: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para deletar um questionário
@questionario_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_questionario(id):
    """
    Deleta um questionário.
    """
    try:
        questionario = Questionario.query.get(id)
        if not questionario:
            return jsonify({'error': 'Questionário não encontrado'}), 404

        db.session.delete(questionario)
        db.session.commit()
        return jsonify({'message': 'Questionário deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para listar todas as sessões de um questionário específico
@questionario_bp.route('/<questionario_id>/sessoes', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessoes_by_questionario(questionario_id):
    """
    Lista todas as sessões de um questionário específico.
    """
    try:
        questionario = Questionario.query.get(questionario_id)
        if not questionario:
            return jsonify({'error': 'Questionário não encontrado'}), 404
        sessoes = questionario.sessoes  # Assuming you have a relationship defined in the model
        return jsonify([sessao.to_json() for sessao in sessoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota detailed paginada que carrega todas os questionarios com suas sessoes
@questionario_bp.route('/detailed', methods=['GET'])
@questionario_bp.route('/detailed/<int:page>/<int:len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_questionarios_detailed(page=1, len=10):
    """
    Lista todos os questionarios com todas as sessoes utilizando joinedload para carregamento otimizado.
    """
    try:
        # Paginação com carregamento otimizado
        questionarios_pag = Questionario.query.options(
            joinedload(Questionario.sessoes)
            .joinedload(Sessao.perguntas)
            .joinedload(Pergunta.alternativas)
        ).paginate(page=page, per_page=len, error_out=False)

        # Montar o JSON hierárquico
        questionarios_json = []
        for questionario in questionarios_pag.items:
            questionario_json = questionario.to_json()
            questionario_json['sessoes'] = []

            for sessao in questionario.sessoes:
                sessao_json = sessao.to_json()
                sessao_json['perguntas'] = []

                for pergunta in sessao.perguntas:
                    pergunta_json = pergunta.to_json()
                    pergunta_json['alternativas'] = [
                        alternativa.to_json() for alternativa in pergunta.alternativas
                    ]
                    sessao_json['perguntas'].append(pergunta_json)

                questionario_json['sessoes'].append(sessao_json)

            questionarios_json.append(questionario_json)

        # Retornar o JSON hierárquico
        return jsonify({
            'questionarios': questionarios_json,
            'total': questionarios_pag.total,
            'page': questionarios_pag.page,
            'pages': questionarios_pag.pages
        }), 200

    except Exception as e:
        print(f"Erro ao listar questionários detalhados: {e}")
        return jsonify({'error': str(e)}), 500

# Rota detailed que retorna um questionário por ID com todas as sessões, perguntas e alternativas
@questionario_bp.route('/detailed/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_questionario_detailed(id):
    """
    Retorna um questionário específico (por ID) com todas as sessões, perguntas e alternativas utilizando joinedload.
    """
    try:
        # Carregar o questionário com todas as relações
        questionario = Questionario.query.options(
            joinedload(Questionario.sessoes)
            .joinedload(Sessao.perguntas)
            .joinedload(Pergunta.alternativas)
        ).get(id)

        if not questionario:
            return jsonify({'error': 'Questionário não encontrado'}), 404

        # Montar o JSON hierárquico
        questionario_json = questionario.to_json()
        questionario_json['sessoes'] = []

        for sessao in questionario.sessoes:
            sessao_json = sessao.to_json()
            sessao_json['perguntas'] = []

            for pergunta in sessao.perguntas:
                pergunta_json = pergunta.to_json()
                pergunta_json['alternativas'] = [
                    alternativa.to_json() for alternativa in pergunta.alternativas
                ]
                sessao_json['perguntas'].append(pergunta_json)

            questionario_json['sessoes'].append(sessao_json)

        # Retornar o JSON hierárquico
        return jsonify(questionario_json), 200

    except Exception as e:
        print(f"Erro ao listar questionário detalhado: {e}")
        return jsonify({'error': str(e)}), 500
    
    
    
@questionario_bp.route('/find_by_title_or_description/<string:search>/', methods=['GET'])
@questionario_bp.route('/find_by_title_or_description/<string:search>/<int:page>/<int:len>/', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def find_by_title_or_description(search, page=1, len=10):
    """
    Retorna questionários que contêm o termo de pesquisa no título ou na descrição.
    """
    try:
        search = f"%{search}%"
        questionarios = Questionario.query.filter(
            (Questionario.titulo.ilike(search)) | (Questionario.descricao.ilike(search))
        ).paginate(page=page, per_page=len, error_out=False)

        return jsonify([questionario.to_json() for questionario in questionarios.items]), 200
    except Exception as e:
        print(f"Erro ao buscar questionários: {e}")
        return jsonify({'error': str(e)}), 500