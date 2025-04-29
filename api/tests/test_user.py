import unittest
from app import create_app
from extensions import db
from models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial antes de cada teste.
        """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            # Limpa o banco de dados
            db.drop_all()
            db.create_all()

            # Cria um único usuário admin de teste
            self.user = User(email='admin@example.com', role='admin', is_active=True)
            self.user.set_password('password123')
            db.session.add(self.user)
            db.session.commit()

            # Gera o token JWT
            self.token = self.user.to_json()['token']

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        """
        Testa a rota GET /backend/user/users.
        """
        response = self.client.get(
            '/backend/user/users',  # Corrigido com o prefixo completo
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['email'], 'admin@example.com')
    
    
    def test_get_user(self):
        """"
        Testa a rota GET /backend/user/<id>.
        """
        response = self.client.get(
            f'/backend/user/users/{self.user.id}',  
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
    def test_create_user(self):
        """
        Testa a rota POST /backend/user/users.
        """
        response = self.client.post(
            f'/backend/user/users',
            headers={'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'},
            json={
            'email': 'newuser@example.com',
            'senha': 'newpassword123',
            'role': 'paciente',
            'is_active': True
        })
        
        self.assertEqual(response.status_code, 201)
        
        
    def test_update_user(self):
        """
        Testa a rota PUT /backend/user/users/<id>.
        """
        response = self.client.put(
            f'/backend/user/users/{self.user.id}',
            headers={
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={'email': 'updated@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], 'updated@example.com')
    
    
    def test_delete_user(self):
        """
        Testa a rota DELETE /backend/user/users/<id>.
        """
        response = self.client.delete(
            f'/backend/user/users/{self.user.id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)
        
        
    def test_delete_user_without_token(self):
        """
        Testa a rota DELETE /backend/user/users/<id> sem token.
        """
        response = self.client.delete(
            f'/backend/user/users/{self.user.id}'
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
    
    
    def test_login(self):
        """
        Testa a rota POST /backend/user/login.
        """
        response = self.client.post(
            f'/backend/user/users/login',
            headers={'Content-Type': 'application/json'},
            json={
                "email": "admin@example.com",
                "password": "password123"
            }   
        )
        self.assertEqual(response.status_code, 200)
        