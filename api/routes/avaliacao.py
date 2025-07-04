
from flask import Blueprint, request, jsonify
from models import Alternativa, Avaliacao, BateriaTestes, Paciente, Pergunta, Questionario, Sessao, UnidadeSaude, Medico
from extensions import db
from datetime import datetime
from utils.auth import token_required
from sqlalchemy.orm import joinedload, selectinload
import os
from flask import current_app # Adicionado para current_app.config
from sqlalchemy import exc
from collections import Counter
avaliacao_bp = Blueprint('avaliacoes', __name__, url_prefix='/avaliacoes')

# Rota para criar uma nova avaliação
@avaliacao_bp.route('', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_avaliacao():
    """
    Cria uma nova avaliação.
    """
    data = request.get_json()
    print(data) 
    try:
        data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()

        avaliacao = Avaliacao(
           paciente_id = data['paciente_id'],
           unidade_saude_id = data['unidade_saude_id'],
           data_inicio = data_inicio,
           
       )
        db.session.add(avaliacao)
        db.session.commit()
        return jsonify(avaliacao.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para obter uma avaliação pelo ID
@avaliacao_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_avaliacao(id):
    """
    Retorna uma avaliação pelo ID.
    """
    avaliacao = Avaliacao.query.get(id)
    if not avaliacao:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    return jsonify(avaliacao.to_json()), 200
# Rota para atualizar uma avaliação
@avaliacao_bp.route('/set_medico/<avaliacao_id>/<medico_id>', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude'])
def set_medico(avaliacao_id, medico_id):
    """
    Atualiza o médico de uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            
            return jsonify({'error': 'Avaliação não encontrada'}), 404
        
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico nao encontrado'}), 404
        
        avaliacao.medico_id = medico_id
        db.session.commit()
        return jsonify(avaliacao.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
        

        
        
# Rota para excluir uma avaliação
@avaliacao_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_avaliacao(id):
    """
    Exclui uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404

        # Busca todos os exames associados a esta avaliação
        exames_a_deletar = list(avaliacao.exames) # Cria uma cópia da lista para iteração segura

        # Itera sobre cada exame para excluir o arquivo associado
        for exame in exames_a_deletar:
            paciente_do_exame = Paciente.query.get(exame.paciente_id)
            if not paciente_do_exame:
                current_app.logger.warning(f"Paciente {exame.paciente_id} não encontrado para o exame {exame.id} durante a deleção da avaliação {avaliacao.id}.")
                # Decide se continua ou aborta. Por segurança, pode ser melhor continuar para deletar outros arquivos/registros.
                nome_paciente_formatado = "PACIENTE_DESCONHECIDO"
            else:
                nome_paciente_formatado = paciente_do_exame.nome.upper().replace(' ', '_')
            
            data_exame_formatada = exame.created_at.strftime('%Y%m%d')
            nome_arquivo_exame = f"{data_exame_formatada}-{nome_paciente_formatado}-{exame.id}.pdf"

            upload_folder_path = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder_path, f"p-{exame.paciente_id}", f"a-{avaliacao.id}", nome_arquivo_exame)
            # Exclui o arquivo se ele existir
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    # print(f"Arquivo {file_path} deletado com sucesso.") # Opcional: log
                # else:
                    # print(f"Arquivo {file_path} não encontrado.") # Opcional: log, pode ser normal
            except Exception as e_file:
                db.session.rollback()
                return jsonify({'error': f'Erro ao deletar arquivo do exame {exame.id}: {str(e_file)}'}), 500

        # Deleta todos os registros de exames associados à avaliação do banco de dados
        for exame in exames_a_deletar:
            db.session.delete(exame)

        # Finalmente, deleta a avaliação
        db.session.delete(avaliacao)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        db.session.rollback()        
        return jsonify({'error': str(e)}), 400

@avaliacao_bp.route('/por_nome_paciente/<nome_paciente>', methods=['GET']) # Mantido conforme sua preferência, embora uma rota mais específica como /por_nome_paciente/ seja comum
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_avaliacoes_by_paciente(nome_paciente):
    """
    Lista todas as avaliações de um paciente específico pelo nome (busca parcial).
    """
    try:
        # Encontra o paciente pelo nome (case-insensitive)
        paciente = Paciente.query.filter(Paciente.nome.ilike(f'%{nome_paciente}%')).first()
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404

        # Busca todas as avaliações associadas a este paciente
        avaliacoes = Avaliacao.query.filter_by(paciente_id=paciente.id).all()

        if not avaliacoes:
            return jsonify({'message': 'Nenhuma avaliação encontrada para este paciente.'}), 404

        return jsonify([avaliacao.to_json() for avaliacao in avaliacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
# Rota para obter as baterias de testes de uma avaliação específica
@avaliacao_bp.route('/baterias_testes/<id>')
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_baterias_by_avaliacao(id):
    """
    Lista todas as baterias de testes associadas a uma avaliação.
    """
    try:
        avaliacao = Avaliacao.query.get(id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404

        baterias = avaliacao.baterias_testes
        return jsonify([bateria.to_json() for bateria in baterias]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter avaliações por unidade de saúde
@avaliacao_bp.route('/por_unidade_saude/<id>', methods=['GET']) # Mantido conforme sua preferência
@token_required(roles=['admin', 'profissional_saude', 'colaborador'])
def get_avaliacoes_by_unidade_saude(id):
    """
    Lista todas as avaliações de uma unidade de saúde específica.
    """
    try:
        unidade_saude = UnidadeSaude.query.get(id)
        if not unidade_saude:
            return jsonify({'error': 'Unidade de saúde não encontrada'}), 404

        avaliacoes = Avaliacao.query.filter_by(unidade_saude_id=id).all()
        return jsonify([avaliacao.to_json() for avaliacao in avaliacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter avaliações completas por ID do paciente
@avaliacao_bp.route('/paciente/<paciente_id>', methods=['GET']) # Nome da rota mantido conforme solicitado
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente']) # Adicionado 'paciente' para permitir que vejam suas próprias avaliações
def get_avaliacoes_completas_by_paciente_id(paciente_id):
    """
    Lista todas as avaliações de um paciente específico pelo ID,
    incluindo suas baterias de testes e os respectivos questionários.
    """
    try:
        result = []
        # Eager load related data to reduce database queries
        avaliacoes = Avaliacao.query.options(
            selectinload(Avaliacao.baterias_testes).selectinload(BateriaTestes.questionario), # Carrega baterias e seus questionários
            joinedload(Avaliacao.medico),
            joinedload(Avaliacao.unidade_saude),
            joinedload(Avaliacao.paciente) # Carrega o paciente diretamente da avaliação
        ).filter_by(paciente_id=paciente_id).all()

        if not avaliacoes:
            paciente = Paciente.query.get(paciente_id)
            return jsonify(paciente.to_json()), 404
        

        for avaliacao in avaliacoes:
            
            lista_baterias_json = []
            for bateria in avaliacao.baterias_testes: # Acessa as baterias já carregadas
                bateria_json = bateria.to_json()
                if bateria.questionario: # Verifica se o questionário existe (já carregado)
                    bateria_json['questionario'] = bateria.questionario.to_json()
                else:
                    bateria_json['questionario'] = None
                lista_baterias_json.append(bateria_json)
            
            complete_obj = {
                "avaliacao": avaliacao.to_json(),
                "baterias_testes": lista_baterias_json,
                "medico": avaliacao.medico.to_json() if avaliacao.medico else None,
                "unidade_saude": avaliacao.unidade_saude.to_json() if avaliacao.unidade_saude else None,
                "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None
            }
            result.append(complete_obj)
            
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Ocorreu um erro interno ao processar a solicitação.'}), 500
    

def _build_detailed_bateria_json(bateria_obj, tipos_graficaveis_validos, app_config):
    """
    Constrói o JSON detalhado para um objeto BateriaTestes.
    Esta função encapsula a lógica que você forneceu.
    """
    bateria_json = bateria_obj.to_json()
    
    if bateria_obj.questionario:
        bateria_json['questionario'] = bateria_obj.questionario.to_json()
        respostas = bateria_obj.respostas if bateria_obj.respostas else {}
        
        sessoes_list_para_bateria = []
        for sessao_obj in bateria_obj.questionario.sessoes:
            # Inicializar acumuladores para estatísticas da sessão
            soma_pont_obtida_sessao = 0.0
            soma_pont_max_sessao = 0.0
            lista_pontuacoes_obtidas_sessao = []
            perguntas_respondidas_com_valor_count = 0
            
            is_sessao_plotavel = False
            if sessao_obj.perguntas:
                primeiro_tipo_resposta_sessao = sessao_obj.perguntas[0].tipo_resposta
                todas_perguntas_mesmo_tipo = all(
                    p.tipo_resposta == primeiro_tipo_resposta_sessao for p in sessao_obj.perguntas
                )
                tipo_uniforme_e_graficavel = primeiro_tipo_resposta_sessao in tipos_graficaveis_validos
                todas_perguntas_tem_alternativas = all(p.alternativas for p in sessao_obj.perguntas)

                if todas_perguntas_mesmo_tipo and tipo_uniforme_e_graficavel and todas_perguntas_tem_alternativas:
                    is_sessao_plotavel = True

            perguntas_list_para_sessao = []
            for pergunta_obj in sessao_obj.perguntas:
                alternativa_selecionada_id = respostas.get(str(pergunta_obj.id))
                alternativa_selecionada_texto = None
                alternativa_selecionada_valor = None

                if alternativa_selecionada_id and pergunta_obj.alternativas:
                    alt_escolhida = next(
                        (alt for alt in pergunta_obj.alternativas if str(alt.id) == str(alternativa_selecionada_id)),
                        None
                    )
                    if alt_escolhida:
                        alternativa_selecionada_texto = alt_escolhida.texto
                        alternativa_selecionada_valor = alt_escolhida.valor
                
                pergunta_info = {
                    "pergunta_id": str(pergunta_obj.id),
                    "pergunta_texto": pergunta_obj.texto,
                    "tipo_resposta": pergunta_obj.tipo_resposta,
                    "resposta_id": alternativa_selecionada_id,
                    "resposta_texto": alternativa_selecionada_texto,
                    "resposta_valor_escolhido": alternativa_selecionada_valor,
                    "alternativas_disponiveis": [
                        {"alternativa_id": alt.id, "texto": alt.texto, "valor": alt.valor}
                        for alt in pergunta_obj.alternativas
                    ]
                }

                if is_sessao_plotavel and \
                   pergunta_obj.tipo_resposta in tipos_graficaveis_validos and \
                   pergunta_obj.alternativas:
                    
                    valores_alt_pergunta = [alt.valor for alt in pergunta_obj.alternativas if alt.valor is not None]
                    pontuacao_maxima_pergunta = float(max(valores_alt_pergunta)) if valores_alt_pergunta else 0.0
                    pergunta_info["pontuacao_maxima_possivel_pergunta"] = pontuacao_maxima_pergunta
                    soma_pont_max_sessao += pontuacao_maxima_pergunta

                    if alternativa_selecionada_valor is not None:
                        soma_pont_obtida_sessao += float(alternativa_selecionada_valor)
                        lista_pontuacoes_obtidas_sessao.append(float(alternativa_selecionada_valor))
                        perguntas_respondidas_com_valor_count += 1
                    
                    # Estatísticas por alternativa da pergunta
                    estatisticas_alternativas_pergunta = []
                    for alt_obj_stats in pergunta_obj.alternativas:
                        contagem_abs = 1 if alternativa_selecionada_id and alt_obj_stats.id == alternativa_selecionada_id else 0
                        # Para uma única avaliação, a relativa é 100% se escolhida, 0% caso contrário.
                        contagem_rel = 100.0 if contagem_abs == 1 else 0.0 
                        estatisticas_alternativas_pergunta.append({
                            "alternativa_id": alt_obj_stats.id,
                            "alternativa_texto": alt_obj_stats.texto,
                            "valor": alt_obj_stats.valor,
                            "contagem_absoluta": contagem_abs,
                            "contagem_relativa_percentual": contagem_rel 
                        })
                    pergunta_info["estatisticas_alternativas_pergunta"] = estatisticas_alternativas_pergunta

                perguntas_list_para_sessao.append(pergunta_info)
            
            sessao_info_para_bateria = sessao_obj.to_json()
            sessao_info_para_bateria['perguntas_com_respostas'] = perguntas_list_para_sessao
            sessao_info_para_bateria['is_plotavel'] = is_sessao_plotavel

            if is_sessao_plotavel:
                moda_pontuacao = []
                if lista_pontuacoes_obtidas_sessao:
                    count = Counter(lista_pontuacoes_obtidas_sessao)
                    if count: # Garante que o contador não está vazio
                        max_freq = max(count.values())
                        moda_pontuacao = [k for k, v in count.items() if v == max_freq]

                sessao_info_para_bateria['estatisticas_sessao'] = {
                    "total_pontuacao_obtida": soma_pont_obtida_sessao,
                    "total_pontuacao_maxima_possivel": soma_pont_max_sessao,
                    "media_pontuacao_obtida_por_pergunta_respondida": (soma_pont_obtida_sessao / perguntas_respondidas_com_valor_count) if perguntas_respondidas_com_valor_count > 0 else 0.0,
                    "moda_pontuacao_obtida_nas_perguntas": moda_pontuacao,
                    "percentual_aproveitamento": (soma_pont_obtida_sessao / soma_pont_max_sessao * 100) if soma_pont_max_sessao > 0 else 0.0
                }

            sessoes_list_para_bateria.append(sessao_info_para_bateria)
        bateria_json['sessoes_detalhadas'] = sessoes_list_para_bateria
    else:
        bateria_json['questionario'] = None
        bateria_json['sessoes_detalhadas'] = []
    return bateria_json

@avaliacao_bp.route('/estatisticas/<avaliacao_id>', methods=['GET'])
@token_required(roles=['admin', 'medico', 'profissional_saude'])
def get_avaliacao_estatisticas_laudo(avaliacao_id):
    """
    Retorna dados detalhados e estatísticas das respostas para cada bateria de uma avaliação.
    A bateria de "Perfil de Saúde" é sempre detalhada.
    Outras sessões são marcadas como graficáveis ou não, com estatísticas apropriadas.
    """
    try:
        avaliacao = Avaliacao.query.options(
            selectinload(Avaliacao.baterias_testes)
                .selectinload(BateriaTestes.questionario)
                .selectinload(Questionario.sessoes)
                .selectinload(Sessao.perguntas)
                .selectinload(Pergunta.alternativas),
            joinedload(Avaliacao.paciente)
        ).options(joinedload(Avaliacao.medico)).get(avaliacao_id) # Adicionado joinedload para Medico

        
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404
        if not avaliacao.paciente:
            return jsonify({'error': 'Paciente da avaliação não encontrado'}), 404
     
        # Inicializa o payload de acordo com a interface PayloadEstatisticas do frontend
        payload = {
            "avaliacao_id": avaliacao.id,
            "fechada": avaliacao.fechada,
            "paciente_nome": avaliacao.paciente.nome,
            "data_avaliacao": avaliacao.data_inicio.isoformat() if avaliacao.data_inicio else None,
            "paciente_id": avaliacao.paciente.id, # Mantido para compatibilidade, mas o objeto completo estará disponível
            "perfil_de_saude_detalhado": None, 
            "outras_baterias": [],
            "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None, # Adicionado objeto Paciente completo
            "medico": avaliacao.medico.to_json() if avaliacao.medico else None       # Adicionado objeto Medico completo
        }

        # Definindo os tipos de resposta que consideramos graficáveis
        TIPOS_RESPOSTA_GRAFICAVEIS_VALIDOS = [
            'booleano', 
            'escala_likert_3', 
            'escala_likert_4', 
            'escala_likert_5',
            'escala_likert_10', # Adicionado conforme padrão comum
            'multipla_escolha_unica', # Adicionado conforme padrão comum
            'escolha_personalizada' # Mantido, assumindo que 'personalizado' aqui se refere a uma escolha com alternativas
        ]

        titulo_perfil_saude_config = current_app.config.get('PERFIL_DE_SAUDE') # Ajustado para PERFIL_DE_SAUDE_TITULO se essa for a chave correta
        
        # 1. Buscar e processar a bateria "Perfil de Saúde" para o paciente desta avaliação
        if titulo_perfil_saude_config and avaliacao.paciente_id:
            # Primeiro, encontrar o Questionario "Perfil de Saúde" pelo título
            perfil_de_saude_questionario = Questionario.query.filter_by(titulo=titulo_perfil_saude_config).first()
            
            if perfil_de_saude_questionario:
                # Depois, buscar a BateriaTestes associada a este paciente e a este questionário
                # É importante carregar as relações para que _build_detailed_bateria_json funcione corretamente
                perfil_de_saude_bateria_obj = BateriaTestes.query.options(
                    selectinload(BateriaTestes.questionario)
                        .selectinload(Questionario.sessoes)
                        .selectinload(Sessao.perguntas)
                        .selectinload(Pergunta.alternativas)
                ).filter_by(
                    paciente_id=avaliacao.paciente_id,
                    questionario_id=perfil_de_saude_questionario.id
                ).order_by(BateriaTestes.data_aplicacao.desc()).first() # Pega a mais recente, caso haja múltiplas

                if perfil_de_saude_bateria_obj:
                    payload['perfil_de_saude_detalhado'] = _build_detailed_bateria_json(
                        perfil_de_saude_bateria_obj, 
                        TIPOS_RESPOSTA_GRAFICAVEIS_VALIDOS, 
                        current_app.config
                    )

        # 2. Processar as baterias que estão diretamente ligadas à 'avaliacao' atual
        for bateria_da_avaliacao_obj in avaliacao.baterias_testes:
            bateria_detalhada_json = _build_detailed_bateria_json(bateria_da_avaliacao_obj, TIPOS_RESPOSTA_GRAFICAVEIS_VALIDOS, current_app.config)
            payload['outras_baterias'].append(bateria_detalhada_json)
        
        return jsonify(payload), 200

    except Exception as e:
        current_app.logger.error(f"Erro em get_avaliacao_estatisticas_laudo para avaliação {avaliacao_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500



@avaliacao_bp.route('/por_medico/<medico_id>', methods=['GET'])
@token_required(roles=['admin', 'medico'])
def get_avaliacoes_by_medico(medico_id):
    """
    Lista todas as avaliações de um médico específico,
    incluindo seus pacientes e baterias de testes com questionários.
    """
    try:
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        result = []
        # Eager load related data to reduce database queries
        avaliacoes = Avaliacao.query.options(
            selectinload(Avaliacao.baterias_testes)
                .selectinload(BateriaTestes.questionario), # Carrega baterias e seus questionários
            joinedload(Avaliacao.paciente) # Carrega o paciente diretamente da avaliação
        ).filter_by(medico_id=medico_id, fechada=False).all() # Adicionado filtro para avaliações abertas
 
        if not avaliacoes:
            return jsonify([]), 200 # Retorna lista vazia se o médico existe mas não tem avaliações

        for avaliacao in avaliacoes:
            lista_baterias_json = []
            for bateria in avaliacao.baterias_testes: # Acessa as baterias já carregadas
                bateria_json = bateria.to_json()
                if bateria.questionario: # Verifica se o questionário existe (já carregado)
                    bateria_json['questionario'] = bateria.questionario.to_json()
                else:
                    bateria_json['questionario'] = None
                lista_baterias_json.append(bateria_json)
            
            avaliacao_fetch_obj = {
                "avaliacao": avaliacao.to_json(),
                "baterias_testes": lista_baterias_json,
                "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None
            }
            result.append(avaliacao_fetch_obj)
            
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar avaliações por médico {medico_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro interno ao processar a solicitação.'}), 500
    



@avaliacao_bp.route("/<id>/fechar", methods=["PUT"])
@token_required(roles=['admin',  'medico'])
def fechar_avaliacao(id):
    try:
        avaliacao = Avaliacao.query.get(id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação nao encontrada'}), 404

        avaliacao.fechada = True
        db.session.commit()
        return jsonify(avaliacao.to_json()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao fechar avaliação {id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro interno ao processar a solicitação.'}), 500


@avaliacao_bp.route('/por_medico_e_filtro_paciente/<string:medico_id>', methods=['GET'])
@token_required(roles=['admin', 'medico'])
def get_avaliacoes_por_medico_e_filtro_paciente(medico_id):
    """
    Lista avaliações de um médico específico, com filtros opcionais por nome do paciente e status da avaliação.
    Query params:
        - nome_paciente (string): Para busca parcial no nome do paciente.
        - status (string): "abertas", "fechadas" ou "todas" (padrão).
    """
    try:
        nome_paciente_filtro = request.args.get('nome_paciente', None)
        status_filtro = request.args.get('status', 'todas').lower()

        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404

        query = Avaliacao.query.options(
            selectinload(Avaliacao.baterias_testes)
                .selectinload(BateriaTestes.questionario),
            joinedload(Avaliacao.paciente)
        ).filter(Avaliacao.medico_id == medico_id)

        if nome_paciente_filtro:
            query = query.join(Paciente).filter(Paciente.nome.ilike(f'%{nome_paciente_filtro}%'))

        if status_filtro == 'abertas':
            query = query.filter(Avaliacao.fechada == False)
        elif status_filtro == 'fechadas':
            query = query.filter(Avaliacao.fechada == True)
        # Se 'todas' ou inválido, não aplica filtro de status adicional

        avaliacoes = query.all()

        result = []
        for avaliacao in avaliacoes:
            lista_baterias_json = []
            for bateria in avaliacao.baterias_testes:
                bateria_json = bateria.to_json()
                if bateria.questionario:
                    bateria_json['questionario'] = bateria.questionario.to_json()
                else:
                    bateria_json['questionario'] = None
                lista_baterias_json.append(bateria_json)
            
            avaliacao_fetch_obj = {
                "avaliacao": avaliacao.to_json(),
                "baterias_testes": lista_baterias_json,
                "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None
            }
            result.append(avaliacao_fetch_obj)
            
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar avaliações por médico {medico_id} e filtro de paciente: {str(e)}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro interno ao processar a solicitação.'}), 500
