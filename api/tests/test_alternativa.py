import unittest
import os
import jwt
from datetime import datetime, timedelta, timezone
from app import create_app
from extensions import db
from models import Alternativa, Pergunta


class AlternativaTestCase(unittest.TestCase):
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
            from models import User
            user = User(
                email='test_user@admin.com',
                role='admin',
                is_active=True
            )
            user.set_password('password123')  # Define uma senha para o usuário
            db.session.add(user)
            db.session.flush()  # Salva o usuário no banco sem commit
            self.user_id = user.id  # Salva o ID do usuário

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria uma pergunta de teste
            pergunta = Pergunta(
                sessao_id='01JQSS5C8RYT9S8P0KMB9H902D',  # ID fictício para a sessão
                texto='Pergunta Teste',
                tipo_resposta='texto',
                ordem=1
            )
            db.session.add(pergunta)
            db.session.flush()
            self.pergunta_id = pergunta.id  # Salva o ID da pergunta

            # Cria uma alternativa de teste
            alternativa = Alternativa(
                pergunta_id=self.pergunta_id,
                texto='Alternativa Teste',
                valor=1.0,
                ordem=1
            )
            db.session.add(alternativa)
            db.session.commit()
            self.alternativa_id = alternativa.id  # Salva o ID da alternativa

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_alternativas(self):
        """
        Testa a rota GET /backend/alternativas com e sem argumentos.
        """
        # Testa a rota sem parâmetros
        response = self.client.get(
            '/backend/alternativas/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['texto'], 'Alternativa Teste')

        # Testa a rota com parâmetros de paginação
        response = self.client.get(
            '/backend/alternativas/1/10/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['texto'], 'Alternativa Teste')

    def test_get_alternativa(self):
        """
        Testa a rota GET /backend/alternativas/<id>.
        """
        response = self.client.get(
            f'/backend/alternativas/{self.alternativa_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Alternativa Teste')

    def test_create_alternativa(self):
        """
        Testa a rota POST /backend/alternativas.
        """
        response = self.client.post(
            '/backend/alternativas/',
            json={
                'pergunta_id': self.pergunta_id,
                'texto': 'Nova Alternativa',
                'valor': 2.0,
                'ordem': 2
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Nova Alternativa')

    def test_update_alternativa(self):
        """
        Testa a rota PUT /backend/alternativas/<id>.
        """
        response = self.client.put(
            f'/backend/alternativas/{self.alternativa_id}',
            json={
                'pergunta_id': self.pergunta_id,
                'texto': 'Alternativa Atualizada',
                'valor': 3.0,
                'ordem': 1
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['texto'], 'Alternativa Atualizada')
        self.assertEqual(data['valor'], 3.0)

    def test_delete_alternativa(self):
        """
        Testa a rota DELETE /backend/alternativas/<id>.
        """
        response = self.client.delete(
            f'/backend/alternativas/{self.alternativa_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Verifica se a alternativa foi removida
        with self.app.app_context():
            alternativa = Alternativa.query.get(self.alternativa_id)
            self.assertIsNone(alternativa)


if __name__ == '__main__':
    unittest.main()