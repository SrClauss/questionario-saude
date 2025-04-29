from flask import Blueprint, jsonify
import json
from models import Questionario, Sessao, Pergunta, Alternativa, User  # Certifique-se de importar o modelo User
from extensions import db
from utils.auth import token_required
populate_bp = Blueprint('populate', __name__)



@populate_bp.route('/popular-banco', methods=['POST'])

def popular_banco():
    """
    Rota para popular o banco de dados com os questionários do arquivo JSON.
    """
    try:
        # Caminho para o arquivo JSON
        json_path = 'D:\\Source\\projeto-noemi\\api\\fixtures\\questionario.json'

        # Cria o usuário admin
        admin_email = 'admin@admin.com'
        admin_password = 'admin'

        # Verifica se o usuário já existe
        admin_existente = db.session.query(User).filter_by(email=admin_email).first()
        if not admin_existente:
            admin_user = User(email=admin_email, is_active=True, role='admin')  # Define a role como 'admin'
            admin_user.set_password(admin_password)  # Certifique-se de que o método set_password está implementado no modelo User
            db.session.add(admin_user)
            db.session.commit()
            print(f"Usuário admin criado: {admin_email}")

        # Carrega os dados do arquivo JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Contadores para o relatório
        questionarios_criados = 0
        sessoes_criadas = 0
        perguntas_criadas = 0
        alternativas_criadas = 0

        # Itera sobre os questionários no JSON
        for questionario_data in data['questionarios']:
            # Verifica se o questionário já existe
            questionario_existente = db.session.query(Questionario).filter_by(
                titulo=questionario_data['titulo'],
                versao=questionario_data['versao']
            ).first()

            if questionario_existente:
                continue  # Pula se já existir

            # Cria um novo questionário
            novo_questionario = Questionario(
                titulo=questionario_data['titulo'],
                descricao=questionario_data['descricao'],
                versao=questionario_data['versao'],
                fontes_literatura=questionario_data.get('fontes_literatura', []),
                is_active=questionario_data['is_active']
            )
            db.session.add(novo_questionario)
            db.session.commit()
            questionarios_criados += 1

            # Itera sobre as sessões do questionário
            for sessao_data in questionario_data['sessoes']:
                nova_sessao = Sessao(
                    questionario_id=novo_questionario.id,
                    titulo=sessao_data['titulo'],
                    descricao=sessao_data['descricao'],
                    ordem=sessao_data['ordem']
                )
                db.session.add(nova_sessao)
                db.session.commit()
                sessoes_criadas += 1

                # Itera sobre as perguntas da sessão
                for pergunta_data in sessao_data['perguntas']:
                    nova_pergunta = Pergunta(
                        sessao_id=nova_sessao.id,
                        texto=pergunta_data['texto'],
                        tipo_resposta=pergunta_data['tipo_resposta'],
                        metodo_pontuacao=pergunta_data['metodo_pontuacao'],
                        ordem=pergunta_data['ordem'],
                        is_obrigatoria=pergunta_data['is_obrigatoria']
                    )
                    db.session.add(nova_pergunta)
                    db.session.commit()
                    perguntas_criadas += 1

                    # Itera sobre as alternativas da pergunta
                    for alternativa_data in pergunta_data['alternativas']:
                        nova_alternativa = Alternativa(
                            pergunta_id=nova_pergunta.id,
                            texto=alternativa_data['texto'],
                            valor=alternativa_data['valor'],
                            ordem=alternativa_data['ordem']
                        )
                        db.session.add(nova_alternativa)
                        db.session.commit()
                        alternativas_criadas += 1

        # Fecha a sessão
        db.session.close()

        # Retorna uma resposta com o número de registros criados
        return jsonify({
            'status': 'success',
            'message': 'Banco de dados populado com sucesso!',
            'data': {
                'questionarios_criados': questionarios_criados,
                'sessoes_criadas': sessoes_criadas,
                'perguntas_criadas': perguntas_criadas,
                'alternativas_criadas': alternativas_criadas
            }
        }), 201

    except Exception as e:
        # Em caso de erro, faz rollback e retorna mensagem de erro
        if 'session' in locals():
            db.session.rollback()
            db.session.close()

        return jsonify({
            'status': 'error',
            'message': f'Erro ao popular o banco de dados: {str(e)}'
        }), 500