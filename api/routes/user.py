import datetime
import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from PIL import Image
import io
from utils.auth import token_required
from flask import Blueprint, request, jsonify
from models import Avaliacao, BateriaTestes, Colaborador, Laudo, Medico, Paciente, ProfissionalSaude, Questionario, User
from extensions import db
from utils.auth import token_required

user_bp = Blueprint('user', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/', methods=['GET'])
@token_required(roles=['admin'])
def get_users():
    """
    Retorna todos os usuários.
    """
    users = User.query.all()
    return jsonify([user.to_json() for user in users]), 200

@user_bp.route('/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_user(id):
    """
    Retorna um usuário pelo ID.
    """
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(user.to_json()), 200

@user_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def create_user():
    """
    Cria um novo usuário.
    """
    data = request.get_json()
    try:
        user = User(
            email=data['email'],
            role=data['role'],
            is_active=data['is_active']
        )
        user.set_password(data['senha'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@user_bp.route('/<string:id>', methods=['PUT'])
@token_required(roles=['admin'])
def update_user(id):
    """
    Atualiza um usuário existente.
    """
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    data = request.get_json()
    try:
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)
        if 'senha' in data:
            user.set_password(data['senha'])
        db.session.commit()
        return jsonify(user.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@user_bp.route('/<string:id>', methods=['DELETE'])
@token_required(roles=['admin'])
def delete_user(id):
    """
    Deleta um usuário pelo ID.
    """
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Realiza o login de um usuário.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    print(user)
    if user is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    print(user)
    paciente = Paciente.query.filter_by(user_id=user.id).first()
    colaborador = Colaborador.query.filter_by(user_id=user.id).first()
    profissional_saude = ProfissionalSaude.query.filter_by(user_id=user.id).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    result = {
        'user': user.to_json(),
        'paciente': paciente.to_json() if paciente else None,
        'colaborador': colaborador.to_json() if colaborador else None,
        'profissional_saude': profissional_saude.to_json() if profissional_saude else None
    }
    print(result)
    return jsonify(result), 200

@user_bp.route('/<string:user_id>/upload', methods=['POST'])
#@token_required(roles=['admin', 'profissional', 'paciente', 'colaborador'])
def upload_profile_picture(user_id):
    """
    Rota para upload de imagem de perfil.
    Remove qualquer arquivo antigo do usuário antes de salvar o novo.
    Aceita png, jpg, jpeg, gif e bmp.
    """
    import glob

    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Extensão de arquivo não permitida'}), 400

    # Verifica o tamanho do arquivo (máximo 1MB)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > 1024 * 1024:
        return jsonify({'message': 'Tamanho do arquivo excede 1MB'}), 400
    file.seek(0)

    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # Remove arquivos antigos do usuário (qualquer extensão suportada)
        for old_file in glob.glob(os.path.join(upload_folder, f"{user_id}.*")):
            os.remove(old_file)

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{user_id}.{ext}")
        filepath = os.path.join(upload_folder, filename)

        # Abre a imagem usando Pillow
        img = Image.open(file)

        # Comprime e salva como JPEG se for jpg/jpeg, senão salva no formato original
        img_io = io.BytesIO()
        if ext in ['jpg', 'jpeg']:
            img.save(img_io, 'JPEG', quality=70)
        elif ext == 'png':
            img.save(img_io, 'PNG', optimize=True)
        elif ext == 'gif':
            img.save(img_io, 'GIF')
        elif ext == 'bmp':
            img.save(img_io, 'BMP')
        elif ext == 'webp':
            img.save(img_io, 'WEBP', quality=70)
        else:
            img.save(img_io)
        img_io.seek(0)

        with open(filepath, 'wb') as f:
            f.write(img_io.read())

        return jsonify({'message': 'Imagem de perfil enviada com sucesso', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao processar o arquivo: {str(e)}'}), 500

@user_bp.route('/<string:user_id>/image', methods=['GET'])
def get_profile_picture(user_id):
    """
    Rota para obter a imagem de perfil.
    Tenta encontrar a imagem nos formatos jpeg, jpg e png.
    """
    try:
        allowed_exts = ALLOWED_EXTENSIONS
        upload_folder = current_app.config['UPLOAD_FOLDER']
        for ext in allowed_exts:
            filename = f"{user_id}.{ext}"
            filepath = os.path.join(upload_folder, filename)
            if os.path.isfile(filepath):
                return send_from_directory(upload_folder, filename)
        return jsonify({'message': 'Imagem não encontrada'}), 404
    except Exception as e:
        return jsonify({'message': f'Erro ao processar o arquivo: {str(e)}'}), 500

@user_bp.route('/set_password', methods=['PUT'])
def set_password():
    """
    Rota para definir a senha de um usuário.
    """
    data = request.get_json()
    id = data.get('id')
    password = data.get('password')
    
    
    if not id or not password:
        return jsonify({'error': 'ID e senha são obrigatórios'}), 400
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    try:
        user.set_password(password)
        db.session.commit()
        return jsonify({'message': 'Senha atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



@user_bp.route('/admin_metrics', methods=['GET'])
@token_required(roles=['admin'])
def admin_metrics():
    """
    Rota para obter métricas de administração.
    """
    
    numero_usuarios = User.query.count()
    numero_pacientes = Paciente.query.count()
    pacientes_ultimos_30_dias = Paciente.query.filter(Paciente.created_at >= datetime.datetime.now() - datetime.timedelta(days=30)).count()
    numero_colaboradores = Colaborador.query.count()
    numero_profissionais_saude = ProfissionalSaude.query.count()
    numero_medicos = Medico.query.count()
    numero_usuarios = User.query.count()
    numero_usuarios_sem_autenticacao = User.query.filter_by(is_active=False).count()
    baterias_aplicadas_total = BateriaTestes.query.count()
    baterias_ultimos_30_dias = BateriaTestes.query.filter(BateriaTestes.data_aplicacao >= datetime.datetime.now() - datetime.timedelta(days=30)).count()
    baterias_respondidas_ultimos_30_dias = BateriaTestes.query.filter(BateriaTestes.data_aplicacao >= datetime.datetime.now() - datetime.timedelta(days=30), BateriaTestes.is_completo == True).count()
    questionarios_cadastrados = Questionario.query.count()
    avaliacoes_cadastrados = Avaliacao.query.count()
    laudos_emitidos = Laudo.query.count()
    laudos_emitidos_ultimos_30_dias = Laudo.query.filter(Laudo.updated_at >= datetime.datetime.now() - datetime.timedelta(days=30)).count()
    
    
    return jsonify({
        'numero_usuarios': numero_usuarios,
        'numero_pacientes': numero_pacientes,
        'pacientes_ultimos_30_dias': pacientes_ultimos_30_dias,
        'numero_colaboradores': numero_colaboradores,
        'numero_profissionais_saude': numero_profissionais_saude,
        'numero_medicos': numero_medicos,
        'numero_usuarios': numero_usuarios,
        'numero_usuarios_sem_autenticacao': numero_usuarios_sem_autenticacao,
        'baterias_aplicadas_total': baterias_aplicadas_total,
        'baterias_ultimos_30_dias': baterias_ultimos_30_dias,
        'baterias_respondidas_ultimos_30_dias': baterias_respondidas_ultimos_30_dias,
        'questionarios_cadastrados': questionarios_cadastrados,
        'avaliacoes_cadastrados': avaliacoes_cadastrados,
        'laudos_emitidos': laudos_emitidos,
        'laudos_emitidos_ultimos_30_dias': laudos_emitidos_ultimos_30_dias
    })
    
@user_bp.route('/find_user_by_name/<string:substring>', methods=['GET'])
@token_required(roles=['admin'])
def find_user_by_name(substring):
    
    """
        rota que pesquisa nos 4 tipos de usuários pelo nome e retorna os objetos com id, nome e role
    """
    pacientes = Paciente.query.filter(Paciente.nome.like(f'%{substring}%')).all()
    medicos = Medico.query.filter(Medico.nome.like(f'%{substring}%')).all()
    colaboradores = Colaborador.query.filter(Colaborador.nome.like(f'%{substring}%')).all()
    profissionais = ProfissionalSaude.query.filter(ProfissionalSaude.nome.like(f'%{substring}%')).all()
    
    result = []
    
    
    for paciente in pacientes:
        result.append({
            'id': paciente.user_id,
            'nome': paciente.nome,
            'role': 'paciente'
        })
    for medico in medicos:
        result.append({
            'id': medico.id,
            'nome': medico.nome,
            'role': 'medico'
        })
    for colaborador in colaboradores:
        result.append({
            'id': colaborador.id,
            'nome': colaborador.nome,
            'role': 'colaborador'
        })
    for profissional in profissionais:
        result.append({
            'id': profissional.id,
            'nome': profissional.nome,
            'role': 'profissional'
        })
    
    return jsonify(result), 200



@user_bp.route('/all_admins/<int:page>/<int:len>', methods=['GET'])
@token_required(roles=['admin'])
def all_admins(page, len):
    admins = User.query.filter_by(role='admin').paginate(page=page, per_page=len, error_out=False)
    return jsonify([admin.to_json() for admin in admins.items]), 200
    
@user_bp.route('/delete_admin/<string:id>', methods=['DELETE'])
@token_required(roles=['admin'])
def delete_admin(id):
    len_admins = User.query.filter_by(role='admin').count()
    if len_admins == 1:
        return jsonify({'error': 'Nao pode deletar o ultimo admin'}), 400
    admin = User.query.get(id)
    if not admin:
        return jsonify({'error': 'Admin nao encontrado'}), 404
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'message': 'Admin deletado com sucesso'}), 200