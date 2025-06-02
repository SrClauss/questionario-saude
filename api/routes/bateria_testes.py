from flask import Blueprint, request, jsonify
from models import Alternativa, BateriaTestes, Pergunta, ProfissionalSaude, Paciente, Questionario, Sessao
from extensions import db
from datetime import datetime
from utils.auth import token_required
from sqlalchemy import exc
from dateutil.relativedelta import relativedelta

bateria_testes_bp = Blueprint('baterias_testes', 'baterias_testes')

# Rota para listar todas as baterias de testes
@bateria_testes_bp.route('', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_testes():
    """
    Lista todas as baterias de testes.
    """
    baterias = BateriaTestes.query.all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para criar uma nova bateria de testes
@bateria_testes_bp.route('', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def create_bateria_teste():
    """
    Cria uma nova bateria de testes.
    """
    data = request.get_json()

    try:
        # Converte data_aplicacao para datetime.date
        data_aplicacao = datetime.strptime(data['data_aplicacao'], '%Y-%m-%d').date()

        bateria = BateriaTestes(
            profissional_saude_id=data['profissional_saude_id'],
            paciente_id=data['paciente_id'],
            colaborador_id=data.get('colaborador_id'),
            questionario_id=data['questionario_id'],
            avaliacao_id=data['avaliacao_id'],
            data_aplicacao=data_aplicacao,
            respostas=data.get('respostas'),
            observacoes=data.get('observacoes'),
            is_completo=data.get('is_completo', False)
        )
        db.session.add(bateria)
        db.session.commit()
        return jsonify(bateria.to_json()), 201
    except Exception as e:
        print(f"Erro ao criar bateria de testes: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para obter uma bateria de testes pelo ID
@bateria_testes_bp.route('/<id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_bateria_teste(id):
    """
    Retorna uma bateria de testes pelo ID.
    """
    bateria = BateriaTestes.query.get(id)
    if not bateria:
        return jsonify({'error': 'Bateria de testes não encontrada'}), 404
    return jsonify(bateria.to_json()), 200

@bateria_testes_bp.route('/<id>/complete', methods=['PUT'])
@token_required(roles=['paciente'])
def complete_bateria_teste(id):
    """
    Marca uma bateria de testes como completa.
    """
    data = request.get_json()
    try:
        bateria = BateriaTestes.query.get(id)
        if not bateria:
            return jsonify({'error': 'Bateria de testes não encontrada'}), 404

        # Atualiza o status da bateria para completo
        bateria.is_completo = True
        bateria.respostas = data.get('respostas', bateria.respostas)
        
        db.session.commit()
        return jsonify(bateria.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bateria_testes_bp.route('/<id>/respostas', methods=['PUT'])
@token_required(roles=['admin', 'profissional_saude', 'paciente'])
def update_bateria_teste_respostas(id):
    
    """
    Atualiza as respostas de uma bateria de testes.
    """
    data = request.get_json()
    try:
        bateria = BateriaTestes.query.get(id)
        if not bateria:
            return jsonify({'error': 'Bateria de testes não encontrada'}), 404

        # Atualiza apenas as respostas
        bateria.respostas = data.get('respostas', bateria.respostas)
        
        db.session.commit()
        return jsonify(bateria.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
# Rota para excluir uma bateria de testes
@bateria_testes_bp.route('/<id>', methods=['DELETE'])
@token_required(roles=['admin', 'profissional_saude'])
def delete_bateria_teste(id):
    """
    Exclui uma bateria de testes.
    """
    try:
        bateria = BateriaTestes.query.get(id)
        if not bateria:
            return jsonify({'error': 'Bateria de testes não encontrada'}), 404

        db.session.delete(bateria)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rota para listar baterias de testes por paciente
@bateria_testes_bp.route('/paciente/<paciente_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente'])
def get_baterias_by_paciente(paciente_id):
    """
    Lista todas as baterias de testes de um paciente específico,
    retornando um json do tipo:
      [{
          'bateria': bateria.to_json(),
          'qtd_perguntas': <total de perguntas nas sessões do questionário>,
          'questionario': questionario.to_json()
      }]
    """
    baterias = BateriaTestes.query.filter_by(paciente_id=paciente_id).all()
    result = []
    for bateria in baterias:
        # Busca a instância do questionário associado à bateria
        questionario = Questionario.query.get(bateria.questionario_id)
        # Carrega o questionário completo com sessões e perguntas
        qtd_perguntas = 0
        nome_profissional = None
        if bateria.profissional_saude_id:
            profissional = ProfissionalSaude.query.get(bateria.profissional_saude_id)
            if profissional:
                nome_profissional = profissional.nome
        try:
            questionario_completo = Questionario.query.options(
                db.joinedload(Questionario.sessoes)
                  .joinedload(Sessao.perguntas)
            ).get(bateria.questionario_id)

            if questionario_completo is None:
                raise Exception("Questionário não encontrado")

            for sessao in questionario_completo.sessoes:
                for pergunta in sessao.perguntas:
                    qtd_perguntas += 1
        except Exception as e:
            print(f"Erro ao carregar questionário: {e}")
            return jsonify({'error': 'Erro ao carregar questionário'}), 500
        if questionario:
            result.append({
                'bateria': bateria.to_json(),
                'qtd_perguntas': qtd_perguntas,
                'questionario': questionario.to_json(),
                'nome_profissional': nome_profissional
                
                
            })
    return jsonify(result), 200

@bateria_testes_bp.route('/profissional/<profissional_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_profissional(profissional_id):
    """
    Lista todas as baterias de testes de um profissional de saúde específico.
    """
    baterias = BateriaTestes.query.filter_by(profissional_saude_id=profissional_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para listar baterias de testes por colaborador
@token_required(roles=['admin', 'profissional_saude'])
@bateria_testes_bp.route('/colaborador/<colaborador_id>', methods=['GET'])
def get_baterias_by_colaborador(colaborador_id):
    """
    Lista todas as baterias de testes de um colaborador específico.
    """
    baterias = BateriaTestes.query.filter_by(colaborador_id=colaborador_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para listar baterias de testes por questionário
@bateria_testes_bp.route('/questionario/<questionario_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_questionario(questionario_id):
    """
    Lista todas as baterias de testes de um questionário específico.
    """
    baterias = BateriaTestes.query.filter_by(questionario_id=questionario_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200

# Rota para salvar várias baterias de testes em lote
@bateria_testes_bp.route('/batch_save', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude'])
def batch_save_baterias_testes():
    """
    Salva várias baterias de testes em lote (bulk operation).
    payload:
    {
        profissional_saude_id: ulid,
        baterias: [
            {
                paciente_id: ulid,
                colaborador_id: ulid,
                questionario_id: ulid,
                data_aplicacao: 'YYYY-MM-DD',
                respostas: {},
                observacoes: '',
                is_completo: true
            },
            ...
        ]
    }
    """
    data = request.get_json()
    baterias = []
    
    # Validar profissional_saude_id no payload principal
    profissional_saude_id = data.get('profissional_saude_id')
    if not profissional_saude_id:

        return jsonify({'error': 'profissional_saude_id é obrigatório'}), 403
    
    
    try:
        # Iterar sobre a lista de baterias, não sobre o objeto principal
        for item in data.get('baterias', []):
            
            # Converte data_aplicacao para datetime.date
            data_aplicacao = datetime.strptime(item['data_aplicacao'], '%Y-%m-%d').date()

            bateria = BateriaTestes(
                profissional_saude_id=profissional_saude_id,
                paciente_id=item['paciente_id'],
                colaborador_id=item.get('colaborador_id'),
                questionario_id=item['questionario_id'],
                data_aplicacao=data_aplicacao,
                respostas=item.get('respostas'),
                observacoes=item.get('observacoes'),
                is_completo=item.get('is_completo', False)
            )
            
            baterias.append(bateria)

        db.session.bulk_save_objects(baterias)
        db.session.commit()
        return jsonify({'message': 'Baterias de testes salvas com sucesso'}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(f"Erro ao salvar baterias de testes: {e}")
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        print(f"Erro de valor: {e}")
        db.session.rollback()
        return jsonify({'error': f'Erro de valor: {str(e)}'}), 400
    except Exception as e:
        print(f"Erro inesperado: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



@bateria_testes_bp.route('/ensure_perfil_de_saude/<paciente_id>', methods=['POST'])
@token_required(roles=['admin', 'profissional_saude', 'colaborador', 'paciente'])
def ensure_perfil_de_saude(paciente_id):
    
    """
    Garante que o paciente tenha um perfil de saúde associado.
    """
    
    # Verifica se o paciente existe
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({'error': 'Paciente não encontrado'}), 404
    
    
    perfil_de_saude = Questionario.query.filter_by(titulo="Questionário Detalhado de Perfil Básico de Saúde").first()
    
    if not perfil_de_saude:
        return jsonify({'error': 'Perfil de Saúde não encontrado'}), 404
    
    perfil_de_saude_paciente = BateriaTestes.query.filter_by(
        paciente_id=paciente_id,
        questionario_id=perfil_de_saude.id
    ).first()
    
    if perfil_de_saude_paciente:
        return jsonify({'message': 'Perfil de Saúde já existe para este paciente'}), 200
    
    perfil_de_saude_paciente = BateriaTestes(
        profissional_saude_id=None,
        paciente_id=paciente_id,
        colaborador_id=None,
        questionario_id=perfil_de_saude.id,
        data_aplicacao=datetime.now(),
        respostas={},
        observacoes='',
        is_completo=False
    )
    
    db.session.add(perfil_de_saude_paciente)
    db.session.commit()
    return jsonify({'message': 'Perfil de Saúde criado com sucesso'}), 201


# Rota para obter uma bateria de testes pelo ID com questionário detalhado
@bateria_testes_bp.route('/<id>/completo', methods=['GET'])
@token_required(roles=['paciente'])
def get_bateria_teste_completo(id):
    """
    Retorna uma bateria de testes pelo ID, juntamente com o questionário detalhado
    (incluindo sessões, perguntas e alternativas).
    """
    bateria = BateriaTestes.query.get(id)
    if not bateria:
        return jsonify({'error': 'Bateria de testes não encontrada'}), 404

    questionario = Questionario.query.get(bateria.questionario_id)
    if not questionario:
        return jsonify({'error': 'Questionário não encontrado'}), 404

    # Carrega as sessões do questionário, juntamente com as perguntas e alternativas
    sessoes = Sessao.query.filter_by(questionario_id=questionario.id).all()
    sessoes_json = []
    for sessao in sessoes:
        perguntas = Pergunta.query.filter_by(sessao_id=sessao.id).all()
        perguntas_json = []
        for pergunta in perguntas:
            alternativas = Alternativa.query.filter_by(pergunta_id=pergunta.id).all()
            alternativas_json = [alternativa.to_json() for alternativa in alternativas]
            
            pergunta_json = pergunta.to_json()
            pergunta_json['alternativas'] = alternativas_json
            perguntas_json.append(pergunta_json)
        
        sessao_json = sessao.to_json()
        sessao_json['perguntas'] = perguntas_json
        sessoes_json.append(sessao_json)

    questionario_json = questionario.to_json()
    questionario_json['sessoes'] = sessoes_json

    response = {
        'bateria': bateria.to_json(),
        'questionario': questionario_json
    }

    return jsonify(response), 200


@bateria_testes_bp.route('/profissional/<profissional_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_profissional_id(profissional_id):
    """
    Lista todas as baterias de testes de um profissional de saúde específico.
    """
    baterias = BateriaTestes.query.filter_by(profissional_saude_id=profissional_id).all()
    return jsonify([bateria.to_json() for bateria in baterias]), 200
# Rota para listar baterias de testes por colaborador

@bateria_testes_bp.route('/dashboard_profissional/<profissional_id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def dashboard_profissional(profissional_id):
    """
    Conta quantos pacientes têm pelo menos uma bateria de testes associada ao profissional de saúde.
    Fornece estatísticas importantes para o dashboard.
    """
    baterias_profissional = BateriaTestes.query.filter_by(profissional_saude_id=profissional_id).all()

    # Total de baterias e baterias abertas
    numero_total_baterias = len(baterias_profissional)
    numero_total_baterias_abertas = len([bateria for bateria in baterias_profissional if not bateria.is_completo])

    # IDs de pacientes únicos conectados ao profissional
    pacientes_ids = {bateria.paciente_id for bateria in baterias_profissional}
    qtd_pacientes = len(pacientes_ids)

    # Evolução de pacientes conectados nos últimos 6 meses
    hoje = datetime.now().date()
    pacientes_por_mes = []
    for i in range(6):
        inicio_mes = (hoje - relativedelta(months=i)).replace(day=1)
        fim_mes = (inicio_mes + relativedelta(months=1)) - relativedelta(days=1)
        pacientes_mes = {bateria.paciente_id for bateria in baterias_profissional if inicio_mes <= bateria.data_aplicacao <= fim_mes}
        pacientes_por_mes.append({
            'mes': inicio_mes.strftime('%Y-%m'),
            'qtd_pacientes': len(pacientes_mes)
        })

    # Inverter a ordem para exibir do mês mais antigo ao mais recente
    pacientes_por_mes.reverse()

    return jsonify({
        'numero_total_baterias': numero_total_baterias,
        'numero_total_baterias_abertas': numero_total_baterias_abertas,
        'numero_total_baterias_por_profissional': numero_total_baterias,
        'numero_total_baterias_abertas_por_profissional': numero_total_baterias_abertas,
        'numero_baterias_ultimo_mes': len([bateria for bateria in baterias_profissional if bateria.data_aplicacao >= hoje.replace(day=1)]),
        'numero_baterias_abertas_ultimo_mes': len([bateria for bateria in baterias_profissional if bateria.data_aplicacao >= hoje.replace(day=1) and not bateria.is_completo]),
        'evolucao_pacientes': pacientes_por_mes,
        'baterias_profissional': [bateria.to_json() for bateria in baterias_profissional],
    }), 200

#incluir no arquivo de produção

@bateria_testes_bp.route('/datas/<data_inicial>/<data_final>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_datas(data_inicial, data_final):
    """
    Lista todas as baterias de testes entre duas datas.
    """
    try:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
        
        baterias = BateriaTestes.query.filter(BateriaTestes.data_aplicacao.between(data_inicial, data_final)).all()
        return jsonify([bateria.to_json() for bateria in baterias]), 200
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
    
    
    
    
@bateria_testes_bp.route('/nome_paciente/<nome_paciente>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])

def get_baterias_by_nome_paciente(nome_paciente):
    """
    Lista todas as baterias de testes de um grupo de pacientes com um mesma substring no nome.
    """
    
    
    pacientes = Paciente.query.filter(Paciente.nome.ilike(f'%{nome_paciente}%')).all()
    if not pacientes:
        return jsonify({'error': 'Nenhum paciente encontrado com esse nome'}), 404
    pacientes_ids = [paciente.id for paciente in pacientes]
    
    baterias = BateriaTestes.query.filter(BateriaTestes.paciente_id.in_(pacientes_ids)).all()
    baterias.sort(key=lambda x: x.data_aplicacao, reverse=True)
    return jsonify([bateria.to_json() for bateria in baterias]), 200


        
    

@bateria_testes_bp.route('/titulo_descricao_questionario/<criterio>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude'])
def get_baterias_by_titulo_descricao_questionario(criterio):
    """
    Lista todas as baterias de testes de um grupo de questionários com um mesma substring no título ou descrição.
    """
    
    questionarios = Questionario.query.filter(
        (Questionario.titulo.ilike(f'%{criterio}%')) | 
        (Questionario.descricao.ilike(f'%{criterio}%'))
    ).all()
    if not questionarios:
        return jsonify({'error': 'Nenhum questionário encontrado com esse critério'}), 404
    
    questionarios_ids = [questionario.id for questionario in questionarios]
    
    baterias = BateriaTestes.query.filter(BateriaTestes.questionario_id.in_(questionarios_ids)).all()
    baterias.sort(key=lambda x: x.data_aplicacao, reverse=True)
    return jsonify([bateria.to_json() for bateria in baterias]), 200

    



