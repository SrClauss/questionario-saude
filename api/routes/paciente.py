from datetime import datetime, timedelta
from flask import Blueprint, config, request, jsonify, current_app
from models import Paciente, User
from utils.mail import send_confirmation_email_and_set_password
from extensions import db
import jwt
from utils.auth import token_required

paciente_bp = Blueprint('pacientes', __name__)
@paciente_bp.route('/', methods=['GET'])
@paciente_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_pacientes_paginated(page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        pacientes = Paciente.query.order_by(Paciente.nome).paginate(page=page, per_page=len, error_out=False)
        
        # Serializa os itens para JSON
        items = [paciente.to_json() for paciente in pacientes.items]
        
        # Calcula o total de páginas
        total_pages = pacientes.pages
        
        # Retorna os itens e o total de páginas
        return jsonify({'items': items, 'totalPages': total_pages}), 200
    except Exception as e:
        print(f"Erro na rota GET /pacientes: {e}")  # Log do erro
        return jsonify({'error': str(e)}), 500


@paciente_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def create_paciente():
    data = request.get_json()
    try:
        user = User(email=data['email'], is_active=True)
        user.set_password(data['senha'])
        db.session.add(user)
        db.session.flush()

        # Converte data_nascimento para um objeto date
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        paciente = Paciente(
            nome=data['nome'],
            user_id=user.id,
            telefone=data['telefone'],
            enderecos=data['enderecos'],
            data_nascimento=data_nascimento
        )
        db.session.add(paciente)
        db.session.commit()

        return jsonify(paciente.to_json()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro na rota POST /pacientes: {e}")  # Log do erro
        return jsonify({'error': str(e)}), 400

@paciente_bp.route('/register', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def register_paciente():
    data = request.get_json()
    try:
        # Validação do formato de data
        try:
            data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        # Criação do usuário
        user = User(email=data['email'], is_active=False)
        db.session.add(user)
        db.session.flush()

        # Criação do paciente
        paciente = Paciente(
            nome=data['nome'],
            user_id=user.id,
            telefone=data['telefone'],
            enderecos=data['enderecos'],
            cpf=data['cpf'],
            data_nascimento=data_nascimento  # Agora é um objeto date
        )
        db.session.add(paciente)
        db.session.commit()

        # Geração do token
        token = jwt.encode(
            {"user_id": user.id, "nome": data["nome"], 'exp': datetime.now() + timedelta(hours=24)},           
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        send_confirmation_email_and_set_password(token, user.email)
        return jsonify({
            "user": user.to_json(),
            "paciente": paciente.to_json()
        }), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        print("Erro ao registrar paciente:", traceback.format_exc())  # Log detalhado do erro
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 400

@paciente_bp.route('/<id>', methods=['GET'])
def get_paciente(id):
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        return jsonify(paciente.to_json()), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500

@paciente_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def update_paciente(id):
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        data = request.get_json()

        # Verifica se o e-mail já existe em outro usuário
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != paciente.user_id:
            return jsonify({'error': 'Email já em uso'}), 400

        # Atualiza os dados do paciente
        paciente.nome = data['nome']
        paciente.telefone = data['telefone']
        paciente.enderecos = data['enderecos']

        # Converte data_nascimento para um objeto date
        paciente.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        # Atualiza o e-mail do usuário associado
        user = User.query.get(paciente.user_id)
        if user:
            user.email = data['email']

        db.session.commit()
        return jsonify(paciente.to_json()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro na rota PUT /pacientes/{id}: {e}")  # Log do erro
        return jsonify({'error': str(e)}), 400

@paciente_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def delete_paciente(id):
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        user = User.query.get(paciente.user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        db.session.delete(paciente)
        db.session.delete(user)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@paciente_bp.route('/email/<email>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_paciente_by_email(email):
    try:
        paciente = Paciente.query.join(User).filter(User.email == email).first()
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        return jsonify(paciente.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paciente_bp.route('/filter_by_name/<name>', methods=['GET'])
@paciente_bp.route('/filter_by_name/<name>/<int:page>/<int:len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_paciente_by_name(name, page=1, len=10):
    try:
        pacientes = Paciente.query.filter(Paciente.nome.ilike(f'%{name}%')).paginate(
            page=page, per_page=len, error_out=False
        )
        return jsonify([paciente.to_json() for paciente in pacientes.items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@paciente_bp.route('/get_paciente_by_user_id/<user_id>', methods=['GET'])
def get_paciente_by_user_id(user_id):
    try:
        paciente = Paciente.query.filter_by(user_id=user_id).first()
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        return jsonify(paciente.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500