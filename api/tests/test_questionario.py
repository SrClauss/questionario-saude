import unittest
import os
from app import create_app
from extensions import db
from models import Questionario, Sessao, User

class QuestionarioTestCase(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial antes de cada teste.
        """
        os.environ['FLASK_ENV'] = 'testing'
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Cria um usuário de teste
            user = User(email='admin@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria um questionário de teste
            self.questionario = Questionario(
                titulo='Questionario Teste',
                descricao='Descricao Teste',
                versao='1.0'
            )
            db.session.add(self.questionario)
            db.session.flush()
            self.questionario_id = self.questionario.id

            # Cria uma sessão de teste
            self.sessao = Sessao(
                questionario_id=self.questionario_id,
                titulo='Sessao Teste',
                ordem=1
            )
            db.session.add(self.sessao)
            db.session.commit()

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_questionarios(self):
        """
        Testa a rota GET /backend/questionario com e sem argumentos de paginação.
        """
        response = self.client.get(
            '/backend/questionario/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Questionario Teste')

        response = self.client.get(
            '/backend/questionario/1/10',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Questionario Teste')

    def test_get_questionario(self):
        """
        Testa a rota GET /backend/questionario/<id>.
        """
        response = self.client.get(
            f'/backend/questionario/{self.questionario_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Questionario Teste')

    def test_create_questionario(self):
        """
        Testa a rota POST /backend/questionario.
        """
        response = self.client.post(
            '/backend/questionario/',
            json={
                'titulo': 'Novo Questionario',
                'descricao': 'Descricao Nova',
                'versao': '2.0'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Novo Questionario')

    def test_update_questionario(self):
        """
        Testa a rota PUT /backend/questionario/<id>.
        """
        response = self.client.put(
            f'/backend/questionario/{self.questionario_id}',
            json={
                'titulo': 'Questionario Atualizado',
                'descricao': 'Descricao Atualizada',
                'versao': '3.0'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Questionario Atualizado')

    def test_delete_questionario(self):
        """
        Testa a rota DELETE /backend/questionario/<id>.
        """
        response = self.client.delete(
            f'/backend/questionario/{self.questionario_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Verifica se o questionário foi removido dentro de um contexto de aplicação
        with self.app.app_context():
            questionario = Questionario.query.get(self.questionario_id)
            self.assertIsNone(questionario)

    def test_get_sessoes_by_questionario(self):
        """
        Testa a rota GET /backend/questionario/<questionario_id>/sessoes.
        """
        response = self.client.get(
            f'/backend/questionario/{self.questionario_id}/sessoes',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')

    def test_get_questionarios_detailed(self):
        """
        Testa a rota GET /backend/questionario/detailed com e sem paginação.
        """
        response = self.client.get(
            '/backend/questionario/detailed',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('questionarios', data)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['page'], 1)

        questionarios = data['questionarios']
        self.assertEqual(len(questionarios), 1)
        self.assertEqual(questionarios[0]['titulo'], 'Questionario Teste')
        self.assertEqual(len(questionarios[0]['sessoes']), 1)
        self.assertEqual(questionarios[0]['sessoes'][0]['titulo'], 'Sessao Teste')

    def test_get_questionario_detailed(self):
        """
        Testa a rota GET /backend/questionario/detailed/<id>.
        """
        response = self.client.get(
            f'/backend/questionario/detailed/{self.questionario_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Questionario Teste')
        self.assertEqual(len(data['sessoes']), 1)
        self.assertEqual(data['sessoes'][0]['titulo'], 'Sessao Teste')


if __name__ == '__main__':
    unittest.main()