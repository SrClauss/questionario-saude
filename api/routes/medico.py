from datetime import datetime, timedelta
from flask import Blueprint, current_app, request, jsonify
from models import User, Medico
from extensions import db
from flask import current_app
from utils.mail import send_confirmation_email_and_set_password
import jwt
from utils.auth import token_required

medico_bp = Blueprint('medico', __name__, url_prefix='/medicos')

#rota que retorna todos os profissionais de saúde
@medico_bp.route('/', methods=['GET'])
@medico_bp.route('/<page>/<len>', methods=['GET'])
def get_medicos(page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pagination = Medico.query.paginate(page=page, per_page=len, error_out=False)
        items = [medico.to_json() for medico in pagination.items]
        totalPages = pagination.pages  # total de páginas disponíveis
        return jsonify({
            "items": items,
            "totalPages": totalPages
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

#rota administrativa que cria um medico sem confirmação de email
@medico_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def  create_medico():
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota / (create_medico): {data}")
    
    try:
        user = User(email = data['email'], is_active = True)
        user.set_password(data['senha'])
        user.role = 'medico'
        db.session.add(user)
        db.session.flush()
        medico = Medico(
            nome=data['nome'],
            user_id=user.id,
            registro_profissional=data['registro_profissional'],
            tipo_registro=data['tipo_registro'],
            perfil=data['perfil'],
            estado_registro=data['estado_registro'],
            enderecos=data['enderecos'],
            telefone=data['telefone']
            
        )
        db.session.add(medico)
        db.session.commit()
        
        return jsonify(medico.to_json()), 201
    except Exception as e:   
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar médico. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
    
#rota que retorna um profissional de saúde pelo id

@medico_bp.route('/<id>', methods=['GET'])
def  get_medico(id):
    try:
        medico = Medico.query.get(id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404
        return jsonify(medico.to_json()), 200

    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500
    
#rota administrativa que atualiza um medico
@medico_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin'])
def  update_medico(id):
      
    try:
        # Inicia uma transação
        medico = Medico.query.get(id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        data = request.get_json()

        # Verifica se o e-mail já existe em outro usuário
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != medico.user_id:
            return jsonify({'error': 'Email já em uso'}), 400

        # Atualiza os dados do medico
        medico.nome = data['nome']
        medico.registro_profissional = data['registro_profissional']
        medico.tipo_registro = data['tipo_registro']
        medico.perfil = data['perfil']
        medico.estado_registro = data['estado_registro']
        medico.enderecos = data['enderecos']
        medico.telefone = data['telefone']

        # Atualiza o e-mail do usuário associado
        user = User.query.get(medico.user_id)
        if user:
            user.email = data['email']
            user.role = 'medico'

        # Confirma a transação
        db.session.commit()
        return jsonify(medico.to_json()), 200

    except Exception as e:
        # Reverte a transação em caso de erro
        db.session.rollback()
        print("e", e)
        return jsonify({'error': str(e)}), 400
    
#rota administrativa que deleta um medico
@medico_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin'])
def  delete_medico(id):
    try:
        # Busca o medico
        medico = Medico.query.get(id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        # Busca o usuário associado
        user = User.query.get(medico.user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Exclui ambas as entidades dentro de uma transação
        db.session.delete(medico)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    except Exception as e:
        # Reverte a transação em caso de erro
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
#rota que registra um medico e envia email de confirmação
@medico_bp.route('/register', methods=['POST'])
@token_required(roles=['admin'])
def  register_medico():
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota /register: {data}")
    try:
        user = User(email = data['email'], role="medico", is_active = False)
        db.session.add(user)
        db.session.flush()
        
        medico = Medico(
            nome=data['nome'],
            user_id=user.id,
            registro_profissional=data['registro_profissional'],
            cpf=data['cpf'],
            tipo_registro=data['tipo_registro'],
            estado_registro=data['estado_registro'],
            enderecos=data['enderecos'],
            telefone=data['telefone']
            
        )
        db.session.add(medico)
        db.session.commit()
        token = jwt.encode({"user_id": user.id, 'exp': datetime.now() + timedelta(hours=24)},
                current_app.config['SECRET_KEY'],
                algorithm='HS256')
        send_confirmation_email_and_set_password(token, user.email)
        return jsonify({
            "user": user.to_json(),
            "medico": medico.to_json()
            }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar médico. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
    
            
@medico_bp.route('/set-password-confirm-email', methods=['POST'])
@token_required(roles=['admin', 'medico'])
def  set_password_confirm_email():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    password = data['password']
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    try:
        user.set_password(password)
        user.is_active = True
        db.session.commit()
        return jsonify(user.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
#rota que retorna um medico pelo email
@medico_bp.route('/email/<email>', methods=['GET'])
def  get_medico_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        medico = Medico.query.filter_by(user_id=user.id).first()
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404
        return jsonify(medico.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#rota que retorna medicos pelo nome
@medico_bp.route('/filter_by_name/<name>', methods=['GET'])
@medico_bp.route('/filter_by_name/<name>/<page>/<len>', methods=['GET'])
def  get_medicos_by_name(name, page=1, len=10):
    
    try:
        page = int(page)
        len = int(len)
        medicos = Medico.query.filter(Medico.nome.ilike(f'%{name}%')).paginate(
            page=page,
            per_page=len,
            error_out=False)
        return jsonify([medico.to_json() for medico in medicos.items]), 200
    except Exception as e:
        
        print(e)
        return jsonify({'error': str(e)}), 500
    

