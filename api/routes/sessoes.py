from flask import Blueprint, request, jsonify
from models import Pergunta, Sessao, Alternativa  # Importe o modelo Alternativa
from extensions import db
from sqlalchemy.orm import joinedload
from utils.auth import token_required

sessoes_bp = Blueprint('sessoes', __name__)

# Rota para listar todas as sessões
@sessoes_bp.route('/', methods=['GET'])
@sessoes_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessoes(page=1, len=10):
    """
    Lista todas as sessões com paginação.
    """
    try:
        page = int(page)
        len = int(len)
        sessoes = Sessao.query.paginate(page=page, per_page=len, error_out=False)
        return jsonify([sessao.to_json() for sessao in sessoes.items]), 200
    except Exception as e:
        print(f"Erro ao listar sessões: {e}")
        return jsonify({'error': str(e)}), 500

# Rota para obter uma sessão por ID
@sessoes_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessao(id):
    """
    Retorna uma sessão pelo ID.
    """
    sessao = Sessao.query.get(id)
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    return jsonify(sessao.to_json()), 200

# Rota para criar uma nova sessão
@sessoes_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_sessao():
    """
    Cria uma nova sessão e determina a ordem automaticamente.
    """
    data = request.get_json()
    try:
        # Determina a ordem automaticamente no backend
        questionario_id = data['questionario_id']
        # Busca a maior ordem existente para este questionário
        maior_ordem = db.session.query(db.func.max(Sessao.ordem)).filter_by(
            questionario_id=questionario_id
        ).scalar() or 0
        
        # Cria a sessão com ordem incrementada
        sessao = Sessao(
            questionario_id=questionario_id,
            titulo=data['titulo'],
            descricao=data.get('descricao', ''),
            ordem=maior_ordem + 1,  # Incrementa a ordem automaticamente
            regras_visibilidade=data.get('regras_visibilidade', None)
        )
        db.session.add(sessao)
        db.session.commit()
        
        return jsonify(sessao.to_json()), 201
    except Exception as e:
        print(f"Erro ao criar sessão: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para atualizar uma sessão existente
@sessoes_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def update_sessao(id):
    """
    Atualiza uma sessão existente.
    """
    data = request.get_json()
    print(f"Dados recebidos para atualização: {data}")
    try:
        sessao = Sessao.query.get(id)
        if not sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        sessao.questionario_id = data['questionario_id']
        sessao.titulo = data['titulo']
        sessao.descricao = data.get('descricao', sessao.descricao)
        sessao.ordem = data['ordem']
        # sessao.pergunta_condicional = data.get('pergunta_condicional', sessao.pergunta_condicional) # Campo antigo
        # sessao.respostas_condicionais = data.get('respostas_condicionais', sessao.respostas_condicionais) # Campo antigo
        sessao.regras_visibilidade = data.get('regras_visibilidade', sessao.regras_visibilidade)

        db.session.commit()
        return jsonify(sessao.to_json()), 200
    except Exception as e:
        print(f"Erro ao atualizar sessão: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para deletar uma sessão
@sessoes_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_sessao(id):
    """
    Deleta uma sessão.
    """
    try:
        sessao = Sessao.query.get(id)
        if not sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        db.session.delete(sessao)
        db.session.commit()
        return jsonify({'message': 'Sessão deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para listar todas as sessões de um questionário específico
@sessoes_bp.route('/questionario/<questionario_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessoes_by_questionario(questionario_id):
    """
    Lista todas as sessões de um questionário específico.
    """
    try:
        sessoes = Sessao.query.filter_by(questionario_id=questionario_id).all()
        return jsonify([sessao.to_json() for sessao in sessoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota detailed paginada que carrega todas as sessões com suas perguntas
@sessoes_bp.route('/detailed', methods=['GET'])
@sessoes_bp.route('/detailed/<int:page>/<int:len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessoes_detailed(page=1, len=10):
    """
    Lista todas as sessões com todas as perguntas utilizando joinedload para carregamento otimizado.
    """
    try:
        sessoes_pag = Sessao.query.options(joinedload(
                      Sessao.perguntas).joinedload(
                      Pergunta.alternativas)).paginate(page=page, per_page=len, error_out=False).items
        
        # Lista para armazenar as sessões processadas
        sessoes_json = []
        
        for sessao in sessoes_pag:
            sessao_json = sessao.to_json()
            sessao_json['perguntas'] = []
            for pergunta in sessao.perguntas:
                pergunta_json = pergunta.to_json()
                pergunta_json['alternativas'] = []
                for alternativa in pergunta.alternativas:
                    alternativa_json = alternativa.to_json()
                    pergunta_json['alternativas'].append(alternativa_json)
                sessao_json['perguntas'].append(pergunta_json)
            sessoes_json.append(sessao_json)
            
        return jsonify(sessoes_json), 200
    except Exception as e:
        print(f"Erro ao listar sessões detalhadas: {e}")
        return jsonify({'error': str(e)}), 500

# Rota detailed que retorna uma sessão por ID com todas as perguntas
@sessoes_bp.route('/detailed/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_sessao_detailed(id):
    """
    Retorna uma sessão específica (por ID) com todas as perguntas utilizando joinedload.
    """
    try:
        # Carrega a sessão com seus relacionamentos
        sessao = Sessao.query.options(
            joinedload(Sessao.perguntas).joinedload(Pergunta.alternativas)
        ).get(id)
        
        if not sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        # Serializa a sessão
        sessao_json = sessao.to_json()
        sessao_json['perguntas'] = []
        
        # Serializa as perguntas e suas alternativas
        for pergunta in sessao.perguntas:
            pergunta_json = pergunta.to_json()
            pergunta_json['alternativas'] = []
            
            # Serializa as alternativas
            for alternativa in pergunta.alternativas:
                alternativa_json = alternativa.to_json()
                pergunta_json['alternativas'].append(alternativa_json)
                
            sessao_json['perguntas'].append(pergunta_json)
            
        return jsonify(sessao_json), 200
        
    except Exception as e:
        print(f"Erro ao buscar sessão detalhada: {e}")
        return jsonify({'error': str(e)}), 500

@sessoes_bp.route('/<sessao_id>/alternativas-lote', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def update_alternativas_lote_for_sessao(sessao_id):
    """
    Recebe um payload com tipo_resposta e um array de alternativas. Atualiza o tipo_resposta
    de todas as perguntas da sessão e substitui as alternativas existentes pelas novas.
    Payload esperado:
    {
        "tipo_resposta": "booleano",
        "alternativas": [
            {"texto": "Sim", "valor": 1, "ordem": 1},
            {"texto": "Não", "valor": 0, "ordem": 2}
        ]
    }
    """
    data = request.get_json()
    print(data)

    if not isinstance(data, dict) or 'tipo_resposta' not in data or 'alternativas' not in data:
        return jsonify({'error': 'Payload inválido. Esperado: {"tipo_resposta": string, "alternativas": list}'}), 400

    tipo_resposta = data['tipo_resposta']
    alternativas = data['alternativas']

    if not isinstance(alternativas, list):
        return jsonify({'error': 'A lista de alternativas deve ser um array.'}), 400

    try:
        # Busca a sessão com suas perguntas
        sessao = Sessao.query.options(db.joinedload(Sessao.perguntas)).get(sessao_id)
        if not sessao:
            return jsonify({'error': 'Sessão não encontrada.'}), 404

        # Atualiza o tipo_resposta de todas as perguntas da sessão
        for pergunta in sessao.perguntas:
            pergunta.tipo_resposta = tipo_resposta
            # Remove as alternativas existentes
            db.session.query(Alternativa).filter(Alternativa.pergunta_id == pergunta.id).delete()
            # Adiciona as novas alternativas
            for alt in alternativas:
                nova_alternativa = Alternativa(
                    texto=alt['texto'],
                    valor=alt['valor'],
                    ordem=alt['ordem'],
                    pergunta_id=pergunta.id
                )
                db.session.add(nova_alternativa)

        db.session.commit()
        return jsonify({'message': f'Tipo de resposta das perguntas atualizado para "{tipo_resposta}" e alternativas atualizadas.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500