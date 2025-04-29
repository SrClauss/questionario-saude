from datetime import datetime, timedelta
from flask import Blueprint, current_app, request, jsonify
from models import ProfissionalSaude
from models import User
from extensions import db
from flask import current_app
from utils.mail import send_confirmation_email_and_set_password
import jwt
from utils.auth import token_required
profissional_saude_bp = Blueprint('profissionais_saude', __name__)


@profissional_saude_bp.route('/', methods=['GET'])
@profissional_saude_bp.route('/profissionais_saude/<page>/<len>', methods=['GET'])
@token_required(roles=['admin'])
def  get_profissionais_saude(page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        profissionais_saude = ProfissionalSaude.query.paginate(page=page, per_page=len, error_out=False)
        return jsonify([profissional_saude.to_json() for profissional_saude in profissionais_saude.items]), 200
    except Exception as e:

        return jsonify({'error': str(e)}), 500

#rota administrativa que cria um profissional de saúde sem confirmação de email
@profissional_saude_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def  create_profissional_saude():
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota / (create_profissional_saude): {data}")
    
    try:
        user = User(email = data['email'], is_active = True)
        user.set_password(data['senha'])
        user.role = 'profissional_saude'
        db.session.add(user)
        db.session.flush()
        profissional_saude = ProfissionalSaude(
            nome=data['nome'],
            user_id=user.id,
            registro_profissional=data['registro_profissional'],
            tipo_registro=data['tipo_registro'],
            estado_registro=data['estado_registro'],
            enderecos=data['enderecos'],
            telefone=data['telefone']
            
        )
        db.session.add(profissional_saude)
        db.session.commit()
        
        return jsonify(profissional_saude.to_json()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar profissional de saúde. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400

#além da rota create quero uma register que cria o profissional de saude sem @token_required(roles=['admin'])


@profissional_saude_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin'])
def  get_profissional_saude(id):
    try:
        profissional_saude = ProfissionalSaude.query.get(id)
        if not profissional_saude:
            return jsonify({'error': 'Profissional de saúde não encontrado'}), 404
        return jsonify(profissional_saude.to_json()), 200

    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500
@profissional_saude_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin'])
def  update_profissional_saude(id):
    try:
        # Inicia uma transação
        profissional_saude = ProfissionalSaude.query.get(id)
        if not profissional_saude:
            return jsonify({'error': 'Profissional de saúde não encontrado'}), 404

        data = request.get_json()

        # Verifica se o e-mail já existe em outro usuário
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != profissional_saude.user_id:
            return jsonify({'error': 'Email já em uso'}), 400

        # Atualiza os dados do profissional de saúde
        profissional_saude.nome = data['nome']
        profissional_saude.registro_profissional = data['registro_profissional']
        profissional_saude.tipo_registro = data['tipo_registro']
        profissional_saude.estado_registro = data['estado_registro']
        profissional_saude.enderecos = data['enderecos']
        profissional_saude.telefone = data['telefone']

        # Atualiza o e-mail do usuário associado
        user = User.query.get(profissional_saude.user_id)
        if user:
            user.email = data['email']
            user.role = 'profissional_saude'

        # Confirma a transação
        db.session.commit()
        return jsonify(profissional_saude.to_json()), 200

    except Exception as e:
        # Reverte a transação em caso de erro
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@profissional_saude_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin'])
def  delete_profissional_saude(id):
    try:
        # Busca o profissional de saúde
        profissional_saude = ProfissionalSaude.query.get(id)
        if not profissional_saude:
            return jsonify({'error': 'Profissional de saúde não encontrado'}), 404

        # Busca o usuário associado
        user = User.query.get(profissional_saude.user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Exclui ambas as entidades dentro de uma transação
        db.session.delete(profissional_saude)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    except Exception as e:
        # Reverte a transação em caso de erro
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
@profissional_saude_bp.route('/register', methods=['POST'])
@token_required(roles=['admin'])
def  register_profissional_saude():
    data = request.get_json()
    current_app.logger.debug(f"Dados recebidos na rota /register: {data}")
    try:
        user = User(email = data['email'], role="profissional_saude", is_active = False)
        db.session.add(user)
        db.session.flush()
        
        profissional_saude = ProfissionalSaude(
            nome=data['nome'],
            user_id=user.id,
            registro_profissional=data['registro_profissional'],
            cpf=data['cpf'],
            tipo_registro=data['tipo_registro'],
            estado_registro=data['estado_registro'],
            enderecos=data['enderecos'],
            telefone=data['telefone']
            
        )
        db.session.add(profissional_saude)
        db.session.commit()
        
        token = jwt.encode(
        {"user_id": user.id, 'exp': datetime.now() + timedelta(hours=24)},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
        
        )
        send_confirmation_email_and_set_password(token, user.email)
        return jsonify({
            "user": user.to_json(),
            "profissional_saude": profissional_saude.to_json()
            
            }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar profissional de saúde. Dados: {data}. Erro: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
    
    
@profissional_saude_bp.route('/set-password-confirm-email', methods=['POST'])
@token_required(roles=['admin'])
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
        


@profissional_saude_bp.route('/email/<email>', methods=['GET'])
@token_required(roles=['admin'])
def  get_profissional_saude_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        profissional_saude = ProfissionalSaude.query.filter_by(user_id=user.id).first()
        if not profissional_saude:
            return jsonify({'error': 'Profissional de saúde não encontrado'}), 404
        return jsonify(profissional_saude.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@profissional_saude_bp.route('/filter_by_name/<name>/', methods=['GET'])
@profissional_saude_bp.route('/filter_by_name/<name>/<page>/<len>/', methods=['GET'])
@token_required(roles=['admin'])
def  get_profissionais_saude_by_name(name, page=1, len=10):
    
    try:
        page = int(page)
        len = int(len)
        profissionais_saude = ProfissionalSaude.query.filter(ProfissionalSaude.nome.ilike(f'%{name}%')).paginate(
            page=page,
            per_page=len,
            error_out=False)
        return jsonify([profissional_saude.to_json() for profissional_saude in profissionais_saude.items]), 200
    except Exception as e:
        
        print(e)
        return jsonify({'error': str(e)}), 500