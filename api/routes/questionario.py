from itertools import count
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func
from models import Alternativa, Questionario, Sessao, Pergunta, BateriaTestes
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
    
    
    
@questionario_bp.route('/find_by_title_or_description/<string:search>', methods=['GET'])
@questionario_bp.route('/find_by_title_or_description/<string:search>/<int:page>/<int:len>', methods=['GET'])
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
    
    
    
@questionario_bp.route('/number_of_queries/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def number_of_queries(id):
    """
    Retorna o número de perguntas de um questionário específico.
    """
    try:
        questionario = Questionario.query.get(id)
        sessoes = Sessao.query.filter_by(questionario_id=id).all()
        perguntas_number = 0
        
        
        for sessao in sessoes:
            perguntas = Pergunta.query.filter_by(sessao_id=sessao.id).all()
            perguntas_number += len(perguntas)
        return jsonify({
            'questionario_id': questionario.id,
            'questionario_titulo': questionario.titulo,
            'number_of_questions': perguntas_number
        }), 200
    except Exception as e:
        print(f"Erro ao contar perguntas: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@questionario_bp.route('/has_baterias/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente'])
def has_baterias(id):
    """
    Verifica se um questionário possui baterias.
    """
    
    count_baterias = BateriaTestes.query.filter_by(questionario_id=id).count()
    has_baterias = count_baterias > 0
    print(has_baterias)
    if has_baterias:
        return jsonify({
            'questionario_id': id,
            'has_baterias': True
        }), 200
    else:
        return jsonify({
            'questionario_id': id,
            'has_baterias': False
        }), 200

@questionario_bp.route('/duplicate/<string:id>', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def duplicate_questionario(id):
    """
    Duplica um questionário existente, todas suas sessões, perguntas e alternativas.
    Atualiza o título para incluir a versão e define a nova versão.
    """
    try:
        # Obter dados da requisição
        data = request.get_json()
        nova_versao = data.get('versao')
        
        if not nova_versao:
            return jsonify({'error': 'É necessário fornecer uma nova versão'}), 400
        
        # Carregar o questionário original com todas as relações
        questionario_original = Questionario.query.options(
            joinedload(Questionario.sessoes)
            .joinedload(Sessao.perguntas)
            .joinedload(Pergunta.alternativas)
        ).get(id)
        
        if not questionario_original:
            return jsonify({'error': 'Questionário não encontrado'}), 404
        
        # Extrai o título base (removendo qualquer "(versão: X)" existente)
        import re
        titulo_base = re.sub(r'\s*\(versão:\s*[^)]*\)\s*', '', questionario_original.titulo)
        
        # Verifica se já existe um questionário com esse título base e a mesma versão
        novo_titulo = f"{titulo_base} (versão: {nova_versao})"
        questionario_existente = Questionario.query.filter_by(titulo=novo_titulo).first()
        
        if questionario_existente:
            return jsonify({
                'error': f'Já existe um questionário com o título "{novo_titulo}"',
                'questionario_id': questionario_existente.id
            }), 409
        
        # Iniciar transação
        db.session.begin_nested()  # Cria um savepoint
        
        # Criar o novo questionário com o título limpo + nova versão
        novo_questionario = Questionario(
            titulo=novo_titulo,
            descricao=questionario_original.descricao,
            versao=nova_versao,  # Define a nova versão
            fontes_literatura=questionario_original.fontes_literatura,
            is_active=questionario_original.is_active
        )
        
        db.session.add(novo_questionario)
        db.session.flush()
        
        # Mapeamento para rastrear IDs antigos para novos
        sessoes_map = {}  # {id_antigo: id_novo}
        perguntas_map = {}  # {id_antigo: id_novo}
        
        # Duplicar sessões
        for sessao_original in questionario_original.sessoes:
            nova_sessao = Sessao(
                questionario_id=novo_questionario.id,
                titulo=sessao_original.titulo,
                descricao=sessao_original.descricao,
                ordem=sessao_original.ordem
            )
            db.session.add(nova_sessao)
            db.session.flush()
            
            sessoes_map[sessao_original.id] = nova_sessao.id
            
            # Duplicar perguntas da sessão
            for pergunta_original in sessao_original.perguntas:
                nova_pergunta = Pergunta(
                    sessao_id=nova_sessao.id,
                    texto=pergunta_original.texto,
                    tipo_resposta=pergunta_original.tipo_resposta,
                    metodo_pontuacao=pergunta_original.metodo_pontuacao,
                    ordem=pergunta_original.ordem
                )
                db.session.add(nova_pergunta)
                db.session.flush()
                
                perguntas_map[pergunta_original.id] = nova_pergunta.id
                
                # Duplicar alternativas
                for alternativa_original in pergunta_original.alternativas:
                    nova_alternativa = Alternativa(
                        pergunta_id=nova_pergunta.id,
                        texto=alternativa_original.texto,
                        valor=alternativa_original.valor,
                        ordem=alternativa_original.ordem
                    )
                    db.session.add(nova_alternativa)
        
        # Verificar e duplicar lógica condicional das sessões
        for sessao_original in questionario_original.sessoes:
            if sessao_original.pergunta_condicional:  # Verifica se há uma pergunta condicional definida
                nova_sessao_id = sessoes_map.get(sessao_original.id)
                if nova_sessao_id:
                    nova_sessao = Sessao.query.get(nova_sessao_id)
                    # Copia o JSON existente
                    nova_pergunta_condicional = sessao_original.pergunta_condicional.copy() if isinstance(sessao_original.pergunta_condicional, dict) else sessao_original.pergunta_condicional
                    # Se for um dicionário e conter o id da pergunta, atualiza esse id com o novo valor se existir no mapeamento
                    if isinstance(nova_pergunta_condicional, dict) and "id" in nova_pergunta_condicional:
                        old_id = nova_pergunta_condicional["id"]
                        if old_id in perguntas_map:
                            nova_pergunta_condicional["id"] = perguntas_map[old_id]
                    nova_sessao.pergunta_condicional = nova_pergunta_condicional
                    # Caso haja respostas condicionais, simplesmente copie o JSON
                    if sessao_original.respostas_condicionais:
                        nova_sessao.respostas_condicionais = sessao_original.respostas_condicionais
        
        # Commit da transação
        db.session.commit()
        
        # Carregar o novo questionário completo para retorno
        novo_questionario_completo = Questionario.query.options(
            joinedload(Questionario.sessoes)
            .joinedload(Sessao.perguntas)
            .joinedload(Pergunta.alternativas)
        ).get(novo_questionario.id)
        
        # Montar o JSON hierárquico para retorno
        questionario_json = novo_questionario_completo.to_json()
        questionario_json['sessoes'] = []
        
        for sessao in novo_questionario_completo.sessoes:
            sessao_json = sessao.to_json()
            sessao_json['perguntas'] = []
            
            for pergunta in sessao.perguntas:
                pergunta_json = pergunta.to_json()
                pergunta_json['alternativas'] = [
                    alternativa.to_json() for alternativa in pergunta.alternativas
                ]
                sessao_json['perguntas'].append(pergunta_json)
            
            questionario_json['sessoes'].append(sessao_json)
        
        return jsonify(questionario_json), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao duplicar questionário: {e}")
        return jsonify({'error': f'Erro ao duplicar questionário: {str(e)}'}), 500




@questionario_bp.route('/<string:id>/delete-todas-baterias', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_todas_baterias(id):
    """
    Deleta todas as baterias de um questionário específico.
    """
    try:
        # Carregar o questionário
        questionario = Questionario.query.get(id)
        if not questionario:
            return jsonify({'error': 'Questionário não encontrado'}), 404

        # Deletar todas as baterias associadas ao questionário
        BateriaTestes.query.filter_by(questionario_id=id).delete()
        db.session.commit()

        return jsonify({'message': 'Todas as baterias deletadas com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar baterias: {e}")
        return jsonify({'error': str(e)}), 500