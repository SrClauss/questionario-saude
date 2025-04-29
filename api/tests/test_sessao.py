import unittest
import os
from app import create_app
from extensions import db
from models import Sessao, Questionario, Pergunta, User
from flask import Blueprint, jsonify
from decorators import token_required

backend_sessoes_bp = Blueprint('backend_sessoes', __name__)

@backend_sessoes_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin'])
def delete_sessao(id):
    """
    Deleta uma sessão.
    """
    sessao = Sessao.query.get(id)
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404

    try:
        db.session.delete(sessao)
        db.session.commit()
        return '', 204  # Retorna 204 (No Content)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

class SessaoTestCase(unittest.TestCase):
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
            user = User(email='admin@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria um questionário de teste
            questionario = Questionario(
                titulo='Questionario Teste',
                descricao='Descricao Teste',
                versao='1.0'
            )
            db.session.add(questionario)
            db.session.flush()
            self.questionario_id = questionario.id  # Salva o ID do questionário

            # Cria uma sessão de teste
            self.sessao = Sessao(
                questionario_id=self.questionario_id,
                titulo='Sessao Teste',
                ordem=1
            )
            db.session.add(self.sessao)
            db.session.commit()
            self.sessao_id = self.sessao.id
            
            # Cria uma pergunta de teste associada à sessão
            self.pergunta = Pergunta(
                sessao_id=self.sessao_id,
                texto='Pergunta Teste',
                tipo_resposta='texto',
                ordem=1
            )
            db.session.add(self.pergunta)
            db.session.commit()
            self.pergunta_id = self.pergunta.id

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_sessoes(self):
        """
        Testa a rota GET /backend/sessoes com e sem argumentos de paginação.
        """
        response = self.client.get(
            '/backend/sessoes/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')

        response = self.client.get(
            '/backend/sessoes/1/10',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')

    def test_get_sessao(self):
        """
        Testa a rota GET /backend/sessoes/<id>.
        """
        response = self.client.get(
            f'/backend/sessoes/{self.sessao_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Sessao Teste')

    def test_create_sessao(self):
        """
        Testa a rota POST /backend/sessoes.
        """
        response = self.client.post(
            '/backend/sessoes/',
            json={
                'questionario_id': self.questionario_id,  # Usando o ID diretamente
                'titulo': 'Nova Sessao',
                'ordem': 2
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Nova Sessao')

    def test_update_sessao(self):
        """
        Testa a rota PUT /backend/sessoes/<id>.
        """
        response = self.client.put(
            f'/backend/sessoes/{self.sessao_id}',
            json={
                'questionario_id': self.questionario_id,  # Usando o ID diretamente
                'titulo': 'Sessao Atualizada',
                'ordem': 3
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Sessao Atualizada')

    def test_delete_sessao(self):
        """
        Testa a rota DELETE /backend/sessoes/<id>.
        """
        response = self.client.delete(
            f'/backend/sessoes/{self.sessao_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)

        # Verifica se a sessão foi removida
        with self.app.app_context():
            sessao = Sessao.query.get(self.sessao_id)
            self.assertIsNone(sessao)

    def test_get_sessoes_by_questionario(self):
        """
        Testa a rota GET /backend/sessoes/questionario/<id>.
        """
        response = self.client.get(
            f'/backend/sessoes/questionario/{self.questionario_id}',  # Usando o ID diretamente
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')

    def test_get_sessoes_detailed(self):
        """
        Testa a rota GET /backend/sessoes/detailed com e sem paginação.
        """
        response = self.client.get(
            '/backend/sessoes/detailed',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')
        self.assertEqual(len(data[0]['perguntas']), 1)
        self.assertEqual(data[0]['perguntas'][0]['texto'], 'Pergunta Teste')

        response = self.client.get(
            '/backend/sessoes/detailed/1/10',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['titulo'], 'Sessao Teste')
        self.assertEqual(len(data[0]['perguntas']), 1)
        self.assertEqual(data[0]['perguntas'][0]['texto'], 'Pergunta Teste')

    def test_get_sessao_detailed(self):
        """
        Testa a rota GET /backend/sessoes/detailed/<id>.
        """
        response = self.client.get(
            f'/backend/sessoes/detailed/{self.sessao_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['titulo'], 'Sessao Teste')
        self.assertEqual(len(data['perguntas']), 1)
        self.assertEqual(data['perguntas'][0]['texto'], 'Pergunta Teste')


if __name__ == '__main__':
    unittest.main()