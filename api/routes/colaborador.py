from datetime import datetime, timedelta
from flask import Blueprint, current_app, request, jsonify
from models import Colaborador, User
from utils.mail import send_confirmation_email_and_set_password
from extensions import db
import jwt
from utils.auth import token_required

colaborador_bp = Blueprint('colaboradores', __name__)
@colaborador_bp.route('/', methods=['GET'])
@colaborador_bp.route('/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_colaboradores_paginated(page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        colaboradores = Colaborador.query.paginate(page=page, per_page=len, error_out=False)

        return jsonify([colaborador.to_json() for colaborador in colaboradores.items]), 200
    except Exception as e:
        print(f"Erro na rota GET /colaboradores: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@colaborador_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def create_colaborador():
    data = request.get_json()
    try:
        user = User(email=data['email'], role="colaborador", is_active=True)
        user.set_password(data['senha'])
        db.session.add(user)
        db.session.flush()

        colaborador = Colaborador(
            nome=data['nome'],
            user_id=user.id,
            cpf=data['cpf'],
            telefone=data['telefone'],
            enderecos=data['enderecos'],
            funcao=data['funcao']
        )
        db.session.add(colaborador)
        db.session.commit()

        return jsonify(colaborador.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@colaborador_bp.route('/register', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def register_colaborador():
    data = request.get_json()
    try:
        user = User(email=data['email'],role="colaborador", is_active=False)
        db.session.add(user)
        db.session.flush()

        colaborador = Colaborador(
            nome=data['nome'],
            user_id=user.id,
            cpf=data['cpf'],
            telefone=data['telefone'],
            enderecos=data['enderecos'],
            funcao=data['funcao']
        )
        db.session.add(colaborador)
        db.session.commit()

        token = jwt.encode(
            {"user_id": user.id, 'exp': datetime.now() + timedelta(hours=24)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        send_confirmation_email_and_set_password(token, user.email)
        return jsonify({
            "user": user.to_json(),
            "colaborador": colaborador.to_json()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar colaborador: {e}")  # Adicione este log
        return jsonify({'error': str(e)}), 400

@colaborador_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_colaborador(id):
    try:
        colaborador = Colaborador.query.get(id)
        if not colaborador:
            return jsonify({'error': 'Colaborador não encontrado'}), 404
        return jsonify(colaborador.to_json()), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500

@colaborador_bp.route('/<id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def update_colaborador(id):
    try:
        colaborador = Colaborador.query.get(id)
        if not colaborador:
            return jsonify({'error': 'Colaborador não encontrado'}), 404

        data = request.get_json()

        # Verifica se o e-mail já existe em outro usuário
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != colaborador.user_id:
            return jsonify({'error': 'Email já em uso'}), 400

        # Atualiza os dados do colaborador
        colaborador.nome = data['nome']
        colaborador.telefone = data['telefone']
        colaborador.cpf = data['cpf']
        colaborador.enderecos = data['enderecos']
        colaborador.funcao = data['funcao']

        # Atualiza o e-mail do usuário associado
        user = User.query.get(colaborador.user_id)
        if user:
            user.email = data['email']

        db.session.commit()
        return jsonify(colaborador.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@colaborador_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def delete_colaborador(id):
    try:
        colaborador = Colaborador.query.get(id)
        if not colaborador:
            return jsonify({'error': 'Colaborador não encontrado'}), 404

        user = User.query.get(colaborador.user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        db.session.delete(colaborador)
        db.session.delete(user)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@colaborador_bp.route('/email/<email>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_colaborador_by_email(email):
    try:
        colaborador = Colaborador.query.join(User).filter(User.email == email).first()
        if not colaborador:
            return jsonify({'error': 'Colaborador não encontrado'}), 404
        return jsonify(colaborador.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@colaborador_bp.route('/filter_by_name/<name>', methods=['GET'])
@colaborador_bp.route('/filter_by_name/<name>/<page>/<len>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_colaboradores_by_name(name, page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        colaboradores = Colaborador.query.filter(Colaborador.nome.ilike(f'%{name}%')).paginate(
            page=page, per_page=len, error_out=False
        )
        return jsonify([colaborador.to_json() for colaborador in colaboradores.items]), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500