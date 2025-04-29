import unittest
import os
from app import create_app
from extensions import db
from models import Paciente, User
from datetime import date

class PacienteTestCase(unittest.TestCase):
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

            # Cria um usuário de teste
            user = User(email='paciente@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria um paciente de teste
            paciente = Paciente(
                nome='Paciente Teste',
                user_id=user.id,
                telefone='123456789',
                enderecos='{"rua": "Rua Teste", "numero": "123"}',
                data_nascimento=date(1990, 1, 1)
            )
            db.session.add(paciente)
            db.session.commit()
            self.paciente_id = paciente.id  # Salva o ID do paciente

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_pacientes(self):
        """
        Testa a rota GET /backend/pacientes com e sem argumentos.
        """
        response = self.client.get(
            '/backend/pacientes/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], 'Paciente Teste')

    def test_get_paciente(self):
        """
        Testa a rota GET /backend/pacientes/<id>.
        """
        response = self.client.get(
            f'/backend/pacientes/{self.paciente_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Paciente Teste')

    def test_create_paciente(self):
        """
        Testa a rota POST /backend/pacientes.
        """
        response = self.client.post(
            '/backend/pacientes/',
            json={
                'email': 'novo_paciente@example.com',
                'senha': 'newpassword123',
                'nome': 'Novo Paciente',
                'telefone': '987654321',
                'enderecos': '{"rua": "Rua Nova", "numero": "456"}',
                'data_nascimento': '1995-05-05'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Novo Paciente')

    def test_update_paciente(self):
        """
        Testa a rota PUT /backend/pacientes/<id>.
        """
        response = self.client.put(
            f'/backend/pacientes/{self.paciente_id}',
            json={
                'email': 'paciente_atualizado@example.com',
                'nome': 'Paciente Atualizado',
                'telefone': '111222333',
                'enderecos': '{"rua": "Rua Atualizada", "numero": "789"}',
                'data_nascimento': '2000-02-02'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Paciente Atualizado')
        self.assertEqual(data['telefone'], '111222333')

    def test_delete_paciente(self):
        """
        Testa a rota DELETE /backend/pacientes/<id>.
        """
        response = self.client.delete(
            f'/backend/pacientes/{self.paciente_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)

        # Verifica se o paciente foi removido
        with self.app.app_context():
            paciente = Paciente.query.get(self.paciente_id)
            self.assertIsNone(paciente)

    def test_get_paciente_by_email(self):
        """
        Testa a rota GET /backend/pacientes/email/<email>.
        """
        response = self.client.get(
            '/backend/pacientes/email/paciente@example.com',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nome'], 'Paciente Teste')


if __name__ == '__main__':
    unittest.main()