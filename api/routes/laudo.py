from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import CID, BateriaTestes, Laudo, Paciente, Medico, User, Avaliacao # Adicionado Avaliacao
from extensions import db
from utils.auth import token_required
from flask import current_app
import unidecode
import os # Adicionado import do os aqui
from utils.security import encrypt_data_for_qr, decrypt_data_from_qr, generate_qr_code_base64
from sqlalchemy.orm import joinedload

laudo_bp = Blueprint('laudo', __name__, url_prefix='/laudos')

# Rota para criar um novo laudo
@laudo_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'medico'])
def create_laudo():
    data = request.get_json()
    print(data)
    current_app.logger.debug(f"Dados recebidos na rota / (create_laudo): {data}")
    try:
        paciente_id = data.get('paciente_id')
        medico_id = data.get('medico_id')
        avaliacao_id = data.get('avaliacao_id') # Essencial para o Laudo

        if not paciente_id:
            return jsonify({'error': 'paciente_id é obrigatório'}), 400
        if not medico_id:
            return jsonify({'error': 'medico_id é obrigatório'}), 400
        if not avaliacao_id: # Laudo.avaliacao_id é nullable=False
            return jsonify({'error': 'avaliacao_id é obrigatório'}), 400

        # Verificar se o paciente existe
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        # Verificar se o médico existe
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        # Verificar se a avaliação existe
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404

        # Verificar se esta Avaliacao já possui um Laudo (devido ao unique=True em Laudo.avaliacao_id)
        if avaliacao.laudo:
            return jsonify({'error': f'Avaliação {avaliacao_id} já possui um laudo associado (Laudo ID: {avaliacao.laudo.id}).'}), 409

        novo_laudo = Laudo(
            paciente_id=paciente_id,
            medico_id=medico_id,
            avaliacao_id=avaliacao_id,  # Adicionar avaliacao_id aqui
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            parecer=data.get('parecer'),
            abordagem_terapeutica=data.get('abordagem_terapeutica')
        )

        # Lidar com múltiplos CIDs
        cid_codes = data.get('cids', []) # Espera um array de códigos CID
        if cid_codes and isinstance(cid_codes, list):
            for cid_code in cid_codes:
                cid_obj = CID.query.get(cid_code) # Esta query pode disparar autoflush
                if cid_obj:
                    novo_laudo.cids.append(cid_obj)
                else:
                    current_app.logger.warning(f"CID {cid_code} não encontrado ao criar laudo.")
        db.session.add(novo_laudo) # Adicionar à sessão após configurar os atributos principais
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

        if 'data' in data:
            laudo.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
        if 'parecer' in data:
            laudo.parecer = data['parecer']
        if 'abordagem_terapeutica' in data:
            laudo.abordagem_terapeutica = data['abordagem_terapeutica']

        # Lidar com múltiplos CIDs na atualização
        if 'cids' in data:
            laudo.cids = [] # Limpa os CIDs existentes para substituí-los
            cid_codes = data.get('cids', [])
            if cid_codes and isinstance(cid_codes, list):
                for cid_code in cid_codes:
                    cid_obj = CID.query.get(cid_code)
                    if cid_obj:
                        laudo.cids.append(cid_obj)

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
    




def format_fontes_literatura(fontes_json):
    """
    Formata a lista de fontes de literatura em strings legíveis.
    Exemplo de entrada: [{"autor": "Beck, A.T.", "ano": 1988, "titulo": "BAI Manual"}]
    Saída: ["Beck, A.T. (1988). BAI Manual."]
    """
    if not fontes_json:
        return []
    formatted_list = []
    for fonte in fontes_json:
        parts = []
        if isinstance(fonte, dict):
            if fonte.get("autor"):
                parts.append(fonte["autor"])
            if fonte.get("ano"):
                parts.append(f"({fonte['ano']})")
            if fonte.get("titulo"):
                parts.append(fonte["titulo"])
            if fonte.get("revista_ou_editora"): # Exemplo de campo adicional
                 parts.append(f"- {fonte['revista_ou_editora']}")
            formatted_list.append(" ".join(filter(None, parts)) + ".")
        elif isinstance(fonte, str): # Caso seja apenas um texto
            formatted_list.append(fonte)
    return formatted_list

@laudo_bp.route("/avaliacao/<string:avaliacao_id>/pdf_data", methods=["GET"])
def get_laudo_pdf_data(avaliacao_id):
    avaliacao = db.session.query(Avaliacao).options(
        joinedload(Avaliacao.paciente),
        joinedload(Avaliacao.unidade_saude),
        joinedload(Avaliacao.laudo).joinedload(Laudo.medico),
        joinedload(Avaliacao.laudo).joinedload(Laudo.cids),
        joinedload(Avaliacao.baterias_testes).joinedload(BateriaTestes.questionario)
    ).get(avaliacao_id)

    if not avaliacao:
        return jsonify({"error": "Avaliação não encontrada"}), 404
    if not avaliacao.laudo:
        return jsonify({"error": "Laudo não encontrado para esta avaliação"}), 404

    laudo = avaliacao.laudo
    paciente = avaliacao.paciente
    medico = laudo.medico
    unidade_saude = avaliacao.unidade_saude

    # Dados do Laudo
    laudo_info = {
        "id": laudo.id,
        "data_emissao": laudo.data.isoformat() if laudo.data else None,
        "parecer": laudo.parecer,
        "abordagem_terapeutica": laudo.abordagem_terapeutica,
        "medico": {
            "nome": medico.nome if medico else None,
            "crm": medico.crm if medico else None,
            "especialidade": medico.especialidade if medico else None,
            "id": medico.id if medico else None, # Adicionado ID do médico
        },
        "cids_associados": [cid.to_json() for cid in laudo.cids] if laudo.cids else []
    }

    # Dados do Paciente
    paciente_info = paciente.to_json() if paciente else {}
    if 'data_nascimento' in paciente_info and paciente_info['data_nascimento']:
         # Garantir que data_nascimento seja string se já não for
        if not isinstance(paciente_info['data_nascimento'], str):
            paciente_info['data_nascimento'] = paciente.data_nascimento.isoformat()


    # Dados da Avaliação
    avaliacao_info = {
        "id": avaliacao.id,
        "data_inicio": avaliacao.data_inicio.isoformat() if avaliacao.data_inicio else None,
        "unidade_saude": {
            "nome": unidade_saude.nome if unidade_saude else None,
            "cnpj": unidade_saude.cnpj if unidade_saude else None,
        }
    }

    # Questionários Aplicados e Referências
    questionarios_aplicados = []
    todas_referencias_bibliograficas_set = set()

    for bt in avaliacao.baterias_testes:
        if bt.questionario:
            questionario_data = {
                "questionario_id": bt.questionario.id,
                "titulo": bt.questionario.titulo,
                "data_aplicacao": bt.data_aplicacao.isoformat() if bt.data_aplicacao else None,
                "score": bt.respostas.get("pontuacao_total") if isinstance(bt.respostas, dict) else None, # Assumindo que 'pontuacao_total' está em respostas
                "fontes_literatura_formatadas": format_fontes_literatura(bt.questionario.fontes_literatura)
            }
            questionarios_aplicados.append(questionario_data)
            if bt.questionario.fontes_literatura:
                for ref_str in format_fontes_literatura(bt.questionario.fontes_literatura):
                    todas_referencias_bibliograficas_set.add(ref_str)
    
    # Ordenar para consistência, se desejado
    todas_referencias_bibliograficas_list = sorted(list(todas_referencias_bibliograficas_set))


    return jsonify({
        "laudo_info": laudo_info,
        "paciente_info": paciente_info,
        "avaliacao_info": avaliacao_info,
        "questionarios_aplicados": questionarios_aplicados,
        "todas_referencias_bibliograficas": todas_referencias_bibliograficas_list
    })

@laudo_bp.route("/gerar_qr_assinatura", methods=["POST"])
@token_required(roles=['admin', 'medico']) # Ajuste as roles conforme necessário
def gerar_qr_assinatura():
    data = request.get_json()
    medico_id = data.get("medico_id")
    timestamp_assinatura = data.get("timestamp_assinatura") # ex: laudo.data.isoformat() ou datetime.now().isoformat()

    if not medico_id or not timestamp_assinatura:
        return jsonify({"error": "medico_id e timestamp_assinatura são obrigatórios"}), 400

    try:
        # A URL base para a rota de verificação (ajuste conforme sua configuração de frontend/gateway)
        # Captura a URL raiz da requisição atual (ex: http://localhost:5000/ ou https://giftxz.top/)
        # e constrói a URL de verificação do frontend a partir dela.
        verification_base_url = f"{request.url_root.rstrip('/')}/verificar-assinatura"
        
        dados_criptografados_url_safe = encrypt_data_for_qr(medico_id, timestamp_assinatura)
        qr_code_img_base64 = generate_qr_code_base64(dados_criptografados_url_safe, verification_base_url)
        
        return jsonify({"qr_code_base64": qr_code_img_base64}), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao gerar QR code para assinatura: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro ao gerar QR code"}), 500


@laudo_bp.route("/verificar_assinatura_qr/<string:dados_criptografados>", methods=["GET"])
# Esta rota não precisa de token_required, pois é para verificação pública via QR code
def verificar_assinatura_qr(dados_criptografados):
    print(dados_criptografados)
    dados_descriptografados = decrypt_data_from_qr(dados_criptografados)
    print("dados_descriptografados:", dados_descriptografados)
    if not dados_descriptografados:
        return jsonify({"error": "Dados da assinatura inválidos ou corrompidos"}), 400

    medico_id, timestamp_assinatura = dados_descriptografados

    medico = Medico.query.get(medico_id)
    if not medico:
        return jsonify({"error": "Médico não encontrado"}), 404

    return jsonify({
        "medico_nome": medico.nome,
        "medico_crm": medico.crm, # Adicionar CRM pode ser útil
        "data_assinatura": timestamp_assinatura,
        "mensagem": "Assinatura verificada."
    }), 200
