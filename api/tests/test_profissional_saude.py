import unittest
import os
from app import create_app
from extensions import db
from models import ProfissionalSaude, User

class ProfissionalSaudeTestCase(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial antes de cada teste.
        """
        os.environ['FLASK_ENV'] = 'testing'
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Cria um usuário e profissional de saúde de teste
            user = User(email='profissional@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            profissional_saude = ProfissionalSaude(
                nome='Profissional Teste',
                user_id=user.id,
                registro_profissional='123456',
                tipo_registro='CRM',
                estado_registro='SP',
                enderecos='{"rua": "Rua Teste", "numero": "123"}',
                telefone='123456789'
            )
            db.session.add(profissional_saude)
            db.session.commit()
            self.profissional_id = profissional_saude.id  # Salva o ID do profissional

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_profissionais_saude(self):
        """
        Testa a rota GET /backend/profissionais_saude.
        """
        response = self.client.get(
            '/backend/profissionais_saude/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], 'Profissional Teste')

    def test_get_profissional_saude(self):
        """
        Testa a rota GET /backend/profissionais_saude/<id>.
        """
        response = self.client.get(
            f'/backend/profissionais_saude/{self.profissional_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Profissional Teste')

    def test_create_profissional_saude(self):
        """
        Testa a rota POST /backend/profissionais_saude.
        """
        response = self.client.post(
            '/backend/profissionais_saude/',
            json={
                'email': 'novo_profissional@example.com',
                'senha': 'newpassword123',
                'nome': 'Novo Profissional',
                'registro_profissional': '654321',
                'tipo_registro': 'CRM',
                'estado_registro': 'RJ',
                'enderecos': '{"rua": "Rua Nova", "numero": "456"}',
                'telefone': '987654321'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Novo Profissional')

    def test_update_profissional_saude(self):
        """
        Testa a rota PUT /backend/profissionais_saude/<id>.
        """
        response = self.client.put(
            f'/backend/profissionais_saude/{self.profissional_id}',
            json={
                'email': 'profissional_atualizado@example.com',
                'nome': 'Profissional Atualizado',
                'registro_profissional': '987654',
                'tipo_registro': 'CRM',
                'estado_registro': 'MG',
                'enderecos': '{"rua": "Rua Atualizada", "numero": "789"}',
                'telefone': '111222333'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Profissional Atualizado')
        self.assertEqual(data['telefone'], '111222333')

    def test_delete_profissional_saude(self):
        """
        Testa a rota DELETE /backend/profissionais_saude/<id>.
        """
        response = self.client.delete(
            f'/backend/profissionais_saude/{self.profissional_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)

        # Verifica se o profissional foi removido
        with self.app.app_context():
            profissional_saude = ProfissionalSaude.query.get(self.profissional_id)
            self.assertIsNone(profissional_saude)

    def test_get_profissional_saude_by_email(self):
        """
        Testa a rota GET /backend/profissionais_saude/email/<email>.
        """
        response = self.client.get(
            '/backend/profissionais_saude/email/profissional@example.com',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Profissional Teste')


if __name__ == '__main__':
    unittest.main()