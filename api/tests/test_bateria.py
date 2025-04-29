import unittest
import os
from datetime import date
from app import create_app
from extensions import db
from models import BateriaTestes, ProfissionalSaude, Paciente, Questionario, User

class BateriaTestesTestCase(unittest.TestCase):
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
            user = User(email='profissional@example.com', is_active=True, role='admin')
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()

            # Gera o token JWT usando o método to_json()
            user_json = user.to_json()
            self.token = user_json['token']

            # Cria um profissional de saúde de teste
            profissional = ProfissionalSaude(
                nome='Profissional Teste',
                registro_profissional='123456',
                tipo_registro='CRM',
                estado_registro='SP'
            )
            db.session.add(profissional)
            db.session.flush()
            self.profissional_id = profissional.id  # Salva apenas o ID

            # Cria um paciente de teste
            paciente = Paciente(
                nome='Paciente Teste',
                data_nascimento=date(1990, 1, 1)
            )
            db.session.add(paciente)
            db.session.flush()
            self.paciente_id = paciente.id  # Salva apenas o ID

            # Cria um questionário de teste
            questionario = Questionario(
                titulo='Questionario Teste',
                descricao='Descricao Teste',
                versao='1.0'
            )
            db.session.add(questionario)
            db.session.flush()
            self.questionario_id = questionario.id  # Salva apenas o ID

            # Cria uma bateria de testes de exemplo
            bateria = BateriaTestes(
                profissional_saude_id=self.profissional_id,
                paciente_id=self.paciente_id,
                questionario_id=self.questionario_id,
                data_aplicacao=date(2025, 4, 1),
                observacoes='Observação de teste',
                is_completo=False
            )
            db.session.add(bateria)
            db.session.commit()
            self.bateria_id = bateria.id  # Salva apenas o ID

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_baterias_testes(self):
        """
        Testa a rota GET /baterias_testes.
        """
        response = self.client.get(
            '/backend/baterias_testes',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['observacoes'], 'Observação de teste')

    def test_get_bateria_teste(self):
        """
        Testa a rota GET /baterias_testes/<id>.
        """
        response = self.client.get(
            f'/backend/baterias_testes/{self.bateria_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['observacoes'], 'Observação de teste')

    def test_create_bateria_teste(self):
        """
        Testa a rota POST /baterias_testes.
        """
        response = self.client.post(
            '/backend/baterias_testes',
            json={
                'profissional_saude_id': self.profissional_id,
                'paciente_id': self.paciente_id,
                'questionario_id': self.questionario_id,
                'data_aplicacao': date(2025, 4, 2).isoformat(),
                'observacoes': 'Nova bateria de teste',
                'is_completo': True
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['observacoes'], 'Nova bateria de teste')

    def test_update_bateria_teste(self):
        """
        Testa a rota PUT /baterias_testes/<id>.
        """
        response = self.client.put(
            f'/backend/baterias_testes/{self.bateria_id}',
            json={
                'profissional_saude_id': self.profissional_id,
                'paciente_id': self.paciente_id,
                'questionario_id': self.questionario_id,
                'data_aplicacao': date(2025, 4, 3).isoformat(),
                'observacoes': 'Bateria atualizada',
                'is_completo': True
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['observacoes'], 'Bateria atualizada')

    def test_delete_bateria_teste(self):
        """
        Testa a rota DELETE /baterias_testes/<id>.
        """
        response = self.client.delete(
            f'/backend/baterias_testes/{self.bateria_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 204)

        # Verifica se a bateria foi removida
        with self.app.app_context():
            bateria = BateriaTestes.query.get(self.bateria_id)
            self.assertIsNone(bateria)

    def test_get_baterias_by_paciente(self):
        """
        Testa a rota GET /baterias_testes/paciente/<paciente_id>.
        """
        response = self.client.get(
            f'/backend/baterias_testes/paciente/{self.paciente_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['paciente_id'], self.paciente_id)

    def test_get_baterias_by_profissional(self):
        """
        Testa a rota GET /baterias_testes/profissional/<profissional_id>.
        """
        response = self.client.get(
            f'/backend/baterias_testes/profissional/{self.profissional_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['profissional_saude_id'], self.profissional_id)

    def test_get_baterias_by_questionario(self):
        """
        Testa a rota GET /baterias_testes/questionario/<questionario_id>.
        """
        response = self.client.get(
            f'/backend/baterias_testes/questionario/{self.questionario_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['questionario_id'], self.questionario_id)


if __name__ == '__main__':
    unittest.main()