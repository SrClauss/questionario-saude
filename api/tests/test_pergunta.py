import unittest
import os
from app import create_app
from extensions import db
from models import Pergunta, Sessao, User
from datetime import date

class PerguntaTestCase(unittest.TestCase):
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
            user = User(email='pergunta@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria uma sessão de teste
            sessao = Sessao(
                titulo='Sessão Teste',
                descricao='Descrição da Sessão',
                ordem=1
            )
            db.session.add(sessao)
            db.session.flush()
            self.sessao_id = sessao.id  # Salva o ID da sessão

            # Cria uma pergunta de teste
            pergunta = Pergunta(
                sessao_id=self.sessao_id,
                texto='Pergunta Teste',
                tipo_resposta='texto',
                ordem=1
            )
            db.session.add(pergunta)
            db.session.commit()
            self.pergunta_id = pergunta.id  # Salva o ID da pergunta

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_perguntas(self):
        """
        Testa a rota GET /backend/perguntas com e sem argumentos.
        """
        response = self.client.get(
            '/backend/perguntas/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['texto'], 'Pergunta Teste')

    def test_get_pergunta(self):
        """
        Testa a rota GET /backend/perguntas/<id>.
        """
        response = self.client.get(
            f'/backend/perguntas/{self.pergunta_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Pergunta Teste')

    def test_create_pergunta(self):
        """
        Testa a rota POST /backend/perguntas.
        """
        response = self.client.post(
            '/backend/perguntas/',
            json={
                'sessao_id': self.sessao_id,
                'texto': 'Nova Pergunta',
                'tipo_resposta': 'numerica',
                'ordem': 2
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Nova Pergunta')

    def test_update_pergunta(self):
        """
        Testa a rota PUT /backend/perguntas/<id>.
        """
        response = self.client.put(
            f'/backend/perguntas/{self.pergunta_id}',
            json={
                'sessao_id': self.sessao_id,
                'texto': 'Pergunta Atualizada',
                'tipo_resposta': 'texto',
                'ordem': 1
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Pergunta Atualizada')

    def test_delete_pergunta(self):
        """
        Testa a rota DELETE /backend/perguntas/<id>.
        """
        response = self.client.delete(
            f'/backend/perguntas/{self.pergunta_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)

        # Verifica se a pergunta foi removida
        with self.app.app_context():
            pergunta = Pergunta.query.get(self.pergunta_id)
            self.assertIsNone(pergunta)

    def test_get_perguntas_by_sessao(self):
        """
        Testa a rota GET /backend/perguntas/sessao/<sessao_id>.
        """
        response = self.client.get(
            f'/backend/perguntas/sessao/{self.sessao_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['sessao_id'], self.sessao_id)


if __name__ == '__main__':
    unittest.main()