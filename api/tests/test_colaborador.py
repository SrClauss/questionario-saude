import unittest
import os
from app import create_app
from models import Colaborador, User
from extensions import db

class ColaboradorTestCase(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial antes de cada teste.
        """
        # Define a variável de ambiente para 'testing'
        os.environ['FLASK_ENV'] = 'testing'

        # Cria a aplicação com a configuração de teste
        self.app = create_app()
        self.client = self.app.test_client()

        # Cria o contexto da aplicação e inicializa o banco de dados
        with self.app.app_context():
            db.create_all()

            # Cria um usuário e colaborador de teste
            user = User(email='colaborador@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            colaborador = Colaborador(
                nome='Colaborador Teste',
                user_id=user.id,
                telefone='123456789',
                enderecos='{"rua": "Rua Teste", "numero": "123"}',
                funcao='Gerente'
            )
            db.session.add(colaborador)
            db.session.commit()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_colaboradores(self):
        """
        Testa a rota GET /backend/colaboradores com e sem argumentos.
        """
        response = self.client.get(
            '/backend/colaboradores',
            headers={'Authorization': f'Bearer {self.token}'},
            follow_redirects=True  # Segue automaticamente os redirecionamentos
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Verifica se o colaborador de teste está na lista
        nomes = [colaborador['nome'] for colaborador in data]
        self.assertIn('Colaborador Teste', nomes)

        # Opcional: Verifica se o tamanho da lista é maior ou igual a 1
        self.assertGreaterEqual(len(data), 1)

    def test_get_colaborador(self):
        """
        Testa a rota GET /backend/colaboradores/<id>.
        """
        with self.app.app_context():
            colaborador = Colaborador.query.filter_by(nome='Colaborador Teste').first()
            response = self.client.get(
                f'/backend/colaboradores/{colaborador.id}',
                headers={'Authorization': f'Bearer {self.token}'},
                follow_redirects=True  # Segue automaticamente os redirecionamentos
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['nome'], 'Colaborador Teste')

    def test_create_colaborador(self):
        """
        Testa a rota POST /backend/colaboradores.
        """
        response = self.client.post(
            '/backend/colaboradores/',
            json={
                'email': 'novo_colaborador@example.com',
                'senha': 'newpassword123',
                'nome': 'Novo Colaborador',
                'telefone': '987654321',
                'enderecos': '{"rua": "Rua Nova", "numero": "456"}',
                'funcao': 'Assistente'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Novo Colaborador')

    def test_update_colaborador(self):
        """
        Testa a rota PUT /backend/colaboradores/<id>.
        """
        with self.app.app_context():
            colaborador = Colaborador.query.first()
            response = self.client.put(
                f'/backend/colaboradores/{colaborador.id}',
                json={
                    'email': 'colaborador_atualizado@example.com',
                    'nome': 'Colaborador Atualizado',
                    'telefone': '111222333',
                    'enderecos': '{"rua": "Rua Atualizada", "numero": "789"}',
                    'funcao': 'Supervisor'
                },
                headers={'Authorization': f'Bearer {self.token}'}
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['nome'], 'Colaborador Atualizado')
            self.assertEqual(data['telefone'], '111222333')

    def test_delete_colaborador(self):
        """
        Testa a rota DELETE /backend/colaboradores/<id>.
        """
        with self.app.app_context():
            colaborador = Colaborador.query.first()
            response = self.client.delete(
                f'/backend/colaboradores/{colaborador.id}',
                headers={'Authorization': f'Bearer {self.token}'}
            )
            self.assertEqual(response.status_code, 204)

            # Verifica se o colaborador foi removido
            colaborador = Colaborador.query.get(colaborador.id)
            self.assertIsNone(colaborador)

    def test_get_colaborador_by_email(self):
        """
        Testa a rota GET /backend/colaboradores/email/<email>.
        """
        response = self.client.get(
            '/backend/colaboradores/email/colaborador@example.com',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Colaborador Teste')

if __name__ == '__main__':
    unittest.main()