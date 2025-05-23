from functools import wraps
from flask import request, jsonify, abort
import jwt
from flask import current_app

def token_required(roles=None):
    """
    Middleware para validar o token JWT e verificar roles (opcional).
    :param roles: Lista de roles permitidas para acessar a rota.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None

            # Verifica se o token está no cabeçalho Authorization
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                # Substitua por abort(401) para acionar o errorhandler
                abort(401, description="Token não fornecido")

            try:
                # Decodifica o token usando a SECRET_KEY do Flask
                data = jwt.decode(
                    token, 
                    current_app.config['SECRET_KEY'], 
                    algorithms=["HS256"]
                )

                # Verifica se a role do usuário está permitida
                if roles and data.get('role') not in roles:
                    abort(403, description="Usuário não autorizado")

                # Adiciona os dados do token ao request para uso posterior
                request.user = data

            except jwt.ExpiredSignatureError:
                abort(401, description="Token expirado")
            except jwt.InvalidTokenError:
                abort(401, description="Token inválido")

            return f(*args, **kwargs)
        return decorated_function
    return decorator