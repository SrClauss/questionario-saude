import os
from zipfile import ZipFile
import tempfile
import zipfile
from flask import Blueprint, abort, jsonify, request, send_file, current_app, after_this_request # Adicionado current_app e after_this_request
from utils.auth import token_required
from models import Avaliacao, Exame, Paciente
from extensions import db
from werkzeug.utils import secure_filename # Adicionado secure_filename

exame_bp = Blueprint('exames', "exames")

import os
from zipfile import ZipFile
import tempfile
import zipfile
from flask import Blueprint, abort, jsonify, request, send_file, current_app # Adicionado current_app
from utils.auth import token_required # Adicionar ConfiguracaoApp
from models import Avaliacao, Exame, Paciente
from extensions import db
from werkzeug.utils import secure_filename # Adicionado secure_filename

exame_bp = Blueprint('exames', "exames")
# UPLOAD_FOLDER_BASE = 'api/uploads' # Removido para usar a configuração do app
@exame_bp.route('/', methods=['GET'])
@token_required(roles=['admin'])
def get_exames():
    exames = Exame.query.all()
    return jsonify([exame.to_json() for exame in exames]), 200


@exame_bp.route('/<string:id>/<int:page>/<int:len>', methods=['GET'])
@exame_bp.route('/<string:id>', methods=['GET'])
@token_required(roles=['admin', 'profissional_saude', 'medico',  "colaborador", "paciente"])
def get_exames_by_id(id, page=1, len=10):
    try:
        page = int(page)
        len = int(len)
        exames = Exame.query.filter_by(id=id).paginate(page=page, per_page=len, error_out=False)
        return jsonify([exame.to_json() for exame in exames.items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exame_bp.route('/<string:id>', methods=['DELETE'])
@token_required(roles=['admin', 'paciente'])
def delete_exame(id):
    exame = Exame.query.get(id)
    if not exame:
        return jsonify({'error': 'Exame nao encontrado'}), 404

    try:
        # Construir o caminho do arquivo
        paciente_obj = Paciente.query.get(exame.paciente_id)
        nome_paciente_formatado = paciente_obj.nome.upper().replace(' ', '_') if paciente_obj else "PACIENTE_DESCONHECIDO"
        data_exame_formatada = exame.created_at.strftime('%Y%m%d')
        
        nome_arquivo_exame = f"{data_exame_formatada}-{nome_paciente_formatado}-{exame.id}.pdf"
        
        upload_folder_path = current_app.config['UPLOAD_FOLDER']
        pasta_exame = os.path.join(upload_folder_path, "exames", f"p-{exame.paciente_id}", f"a-{exame.avaliacao_id}")
        file_path = os.path.join(pasta_exame, nome_arquivo_exame)

        # Deletar o arquivo físico
        if os.path.exists(file_path):
            os.remove(file_path)
            current_app.logger.info(f"Arquivo {file_path} deletado com sucesso.")
        else:
            current_app.logger.warning(f"Arquivo {file_path} não encontrado para deleção.")

        # Deletar o registro do exame no banco
        db.session.delete(exame)
        db.session.commit()

        # Verificar se a pasta do exame está vazia e deletá-la
        if os.path.exists(pasta_exame) and not os.listdir(pasta_exame):
            os.rmdir(pasta_exame)
            current_app.logger.info(f"Pasta da avaliação {pasta_exame} deletada pois estava vazia.")

            # Verificar se a pasta do paciente (pasta mãe de pasta_exame) está vazia e deletá-la
            pasta_paciente = os.path.dirname(pasta_exame) # Obtém o diretório pai (p-{paciente_id})
            if os.path.exists(pasta_paciente) and not os.listdir(pasta_paciente):
                os.rmdir(pasta_paciente)
                current_app.logger.info(f"Pasta do paciente {pasta_paciente} deletada pois estava vazia.")

        return jsonify({'message': 'Exame deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar exame {id} ou seu arquivo: {str(e)}", exc_info=True)
        return jsonify({'error': f'Erro ao deletar exame: {str(e)}'}), 500

@exame_bp.route('marcar_desmarcar_para_delecao/<string:id>', methods=['PUT'])
@token_required(roles=['paciente'])
def marcar_exame(id):
    exame = Exame.query.get(id)
    if not exame:
        return jsonify({'error': 'Exame nao encontrado'}), 404
    
    exame.marcado_para_delecao = not exame.marcado_para_delecao
    db.session.commit()
    if exame.marcado_para_delecao:
        return jsonify({'message': 'Exame marcado para delecao'}), 200
    else:
        return jsonify({'message': 'Exame desmarcado para delecao'}), 200
@exame_bp.route('/deletar_marcados', methods=['DELETE'])
@token_required(roles=['admin'])
def deletar_exames_marcados():
    exames = Exame.query.filter_by(marcado_para_delecao=True)
    exames.delete()
    db.session.commit()
    return jsonify({'message': 'Exames marcados para delecao deletados com sucesso'}), 200

@exame_bp.route('/', methods=['POST'])
@token_required(roles=['paciente'])
def create_exame():
    saved_filepath = None  # Para rastrear o arquivo salvo para limpeza em caso de erro
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        # Ler dados do formulário, não de request.json
        avaliacao_id = request.form.get('avaliacao_id') 

        if not avaliacao_id:
            return jsonify({'error': 'avaliacao_id é obrigatório'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        # Validação do tipo e tamanho do arquivo
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Extensão de arquivo não permitida. Apenas PDF.'}), 400
        
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        
        # Obter o tamanho do arquivo
        file.seek(0, os.SEEK_END) # Vai para o final do arquivo
        tamanho_em_bytes = file.tell() # Pega a posição atual (tamanho em bytes)
        file.seek(0) # Volta para o início do arquivo para o save()

        if tamanho_em_bytes > MAX_FILE_SIZE:
            return jsonify({'error': f'Tamanho do arquivo excede {MAX_FILE_SIZE // (1024*1024)}MB'}), 400
        
        # Busca Avaliacao para obter paciente_id
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            return jsonify({'error': 'Avaliação não encontrada'}), 404
        
        paciente_id = avaliacao.paciente_id
        if not paciente_id:
            current_app.logger.error(f"Avaliação {avaliacao_id} não possui paciente_id associado.")
            return jsonify({'error': 'ID do paciente não encontrado para esta avaliação'}), 500

        # --- INÍCIO DA LÓGICA DE VERIFICAÇÃO DE LIMITE TOTAL POR PACIENTE (50MB) ---
        LIMITE_MAXIMO_BYTES_PACIENTE = 50 * 1024 * 1024  # 50MB em bytes

        # Calcula o total de bytes já enviados pelo paciente
        soma_bytes_existentes_paciente = db.session.query(db.func.sum(Exame.tamanho_pdf)).filter_by(paciente_id=paciente_id).scalar() or 0.0
        
        # tamanho_em_bytes já foi calculado antes para o arquivo atual
        tamanho_novo_arquivo_bytes = float(tamanho_em_bytes) 

        if (soma_bytes_existentes_paciente + tamanho_novo_arquivo_bytes) > LIMITE_MAXIMO_BYTES_PACIENTE:
            limite_em_mb = LIMITE_MAXIMO_BYTES_PACIENTE / (1024 * 1024)
            return jsonify({'error': f'Upload excede o limite de armazenamento total de {limite_em_mb:.0f}MB para este paciente.'}), 413 # Payload Too Large
        # --- FIM DA LÓGICA DE VERIFICAÇÃO DE LIMITE TOTAL POR PACIENTE ---

        # Cria a entidade Exame
        exame = Exame(
            paciente_id=paciente_id,
            avaliacao_id=avaliacao_id,
       
            tamanho_pdf=float(tamanho_em_bytes) # Armazena o tamanho em bytes como float
        )
        db.session.add(exame)
        db.session.flush()  # Para obter o exame.id e exame.created_at antes do commit final

        # Busca o nome do paciente para o nome do arquivo
        paciente_obj = Paciente.query.get(exame.paciente_id)
        nome_paciente_formatado = paciente_obj.nome.upper().replace(' ', '_') if paciente_obj else "PACIENTE_DESCONHECIDO"
        data_exame_formatada = exame.created_at.strftime('%Y%m%d')

        # Define o caminho de armazenamento do arquivo
        upload_folder_path = current_app.config['UPLOAD_FOLDER']
        pasta = os.path.join(upload_folder_path, "exames", f"p-{exame.paciente_id}", f"a-{exame.avaliacao_id}")
        if not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        filename_on_disk = f"{data_exame_formatada}-{nome_paciente_formatado}-{exame.id}.pdf"
        saved_filepath = os.path.join(pasta, filename_on_disk)
        
        file.save(saved_filepath)
        db.session.commit()

        return jsonify(exame.to_json()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar exame: {str(e)}", exc_info=True)
        if saved_filepath and os.path.exists(saved_filepath):
            try:
                os.remove(saved_filepath)
            except Exception as e_remove:
                current_app.logger.error(f"Erro ao remover arquivo {saved_filepath} após falha: {str(e_remove)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao processar o upload do exame.'}), 500

@exame_bp.route('/file/<string:exame_id>', methods=['GET'])
@token_required(roles=['paciente', 'medico', 'admin'])
def download_exame(exame_id):
    try:
        exame = Exame.query.get(exame_id)
        paciente = Paciente.query.get(exame.paciente_id)
        # avaliacao = Avaliacao.query.get(exame.avaliacao_id) # Avaliacao object not strictly needed for filename if we use exame.avaliacao_id
        
        nome_paciente_formatado = paciente.nome.upper().replace(' ', '_') if paciente else "PACIENTE_DESCONHECIDO"
        data_exame_formatada = exame.created_at.strftime('%Y%m%d')
        nome_arquivo_exame = f"{data_exame_formatada}-{nome_paciente_formatado}-{exame.id}.pdf"
        upload_folder_path = current_app.config['UPLOAD_FOLDER']
        path = os.path.join(upload_folder_path, "exames", f"p-{exame.paciente_id}", f"a-{exame.avaliacao_id}", nome_arquivo_exame)
        return send_file(path, mimetype='application/pdf')
    except:
        return jsonify({'error': 'Exame nao encontrado'}), 404

                              # ex: os.path.join(os.getcwd(), 'uploads')

@exame_bp.route('/dowload/all/<string:avaliacao_id>', methods=['GET']) # Usando UUID para ID da avaliação
@token_required(roles=['paciente', 'medico', 'admin'])
def download_all_avaliacao_exames(avaliacao_id):
  
    exames = Exame.query.filter_by(avaliacao_id=avaliacao_id).all()
    if not exames:
        abort(404, description="Nenhum exame encontrado para esta avaliação.")
    paciente = Paciente.query.get(exames[0].paciente_id)
    avaliacao = Avaliacao.query.get(exames[0].avaliacao_id)
    if not paciente or not avaliacao:
        abort(500, description="Dados de paciente ou avaliação não encontrados para os exames.")
    
    zip_display_name = f"{paciente.nome.upper().replace(' ', '_')}-{avaliacao.created_at.strftime('%Y%m%d')}.zip"
    
    # Usar um nome de arquivo temporário que será gerenciado pelo 'with' statement
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip_file:
        zip_path = temp_zip_file.name # Pega o caminho real do arquivo temporário
    
    upload_folder_path = current_app.config['UPLOAD_FOLDER']
    
    try:
        # Abrir o arquivo ZIP usando 'with' para garantir que seja fechado
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for exame in exames:
                # Para o nome do arquivo dentro do ZIP, precisamos do nome do paciente e data do exame
                paciente_do_exame_obj = Paciente.query.get(exame.paciente_id)
                nome_paciente_formatado_zip = paciente_do_exame_obj.nome.upper().replace(' ', '_') if paciente_do_exame_obj else "PACIENTE_DESCONHECIDO"
                data_exame_formatada_zip = exame.created_at.strftime('%Y%m%d')

                nome_arquivo_no_disco = f"{data_exame_formatada_zip}-{nome_paciente_formatado_zip}-{exame.id}.pdf"
                arcname = nome_arquivo_no_disco # Nome do arquivo dentro do ZIP

                pdf_file_path = os.path.join(
                    upload_folder_path,
                    "exames",
                    f"p-{exame.paciente_id}",
                    f"a-{exame.avaliacao_id}",
                    nome_arquivo_no_disco
                )
                if os.path.exists(pdf_file_path) and os.path.isfile(pdf_file_path):
                    zipf.write(pdf_file_path, arcname)
                else:
                    current_app.logger.warning(f"Arquivo PDF não encontrado para Exame ID {exame.id} no caminho: {pdf_file_path}. Ignorando.")
        
        # O arquivo ZIP é fechado automaticamente aqui ao sair do bloco 'with zipfile.ZipFile(...)'
        response = send_file(zip_path, mimetype='application/zip', download_name=zip_display_name, as_attachment=True)

        # Agenda a remoção do arquivo temporário após a requisição ser completada
        @after_this_request
        def cleanup(response_after):
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except Exception as e_remove:
                current_app.logger.error(f"Erro ao remover arquivo temporário {zip_path}: {e_remove}", exc_info=True)
            return response_after
        
        return response

    except Exception as e:
        current_app.logger.error(f"Falha ao criar ou enviar o arquivo ZIP para avaliação {avaliacao_id}: {e}", exc_info=True)
        abort(500, description="Erro interno ao gerar o arquivo de exames. Tente novamente mais tarde.")

@exame_bp.route('/all_list/<string:avaliacao_id>', methods=['GET'])
@token_required(roles=['paciente', 'medico', 'admin'])
def list_all_avaliacao_exames(avaliacao_id):
    exames = Exame.query.filter_by(avaliacao_id=avaliacao_id).all()
    return jsonify([exame.to_json() for exame in exames]), 200


@exame_bp.route('/all/<string:avaliacao_id>', methods=['GET'])
@token_required(roles=['paciente', 'medico', 'admin'])
def get_all_avaliacao_exames(avaliacao_id):
    exames = Exame.query.filter_by(avaliacao_id=avaliacao_id).all()
    return jsonify([exame.to_json() for exame in exames]), 200


@exame_bp.route('/total_size/<string:avaliacao_id>', methods=['GET'])
@token_required(roles=['paciente', 'medico', 'admin', 'profissional_saude'])
def get_total_exames_size_by_avaliacao(avaliacao_id):
    """
    Calcula e retorna o tamanho total (em bytes) de todos os exames associados a uma avaliação.
    """
    try:
        exames = Exame.query.filter_by(avaliacao_id=avaliacao_id).all()
        if not exames:
            return jsonify({'avaliacao_id': avaliacao_id, 'total_size_bytes': 0, 'message': 'Nenhum exame encontrado para esta avaliação.'}), 200

        total_size_bytes = sum(exame.tamanho_pdf for exame in exames if exame.tamanho_pdf is not None)

        return jsonify({'avaliacao_id': avaliacao_id, 'total_size_bytes': total_size_bytes}), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao calcular o tamanho total dos exames para a avaliação {avaliacao_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f'Erro ao calcular o tamanho total dos exames: {str(e)}'}), 500



@exame_bp.route('/has_exames/<string:avaliacao_id>', methods=['GET'])
@token_required(roles=['paciente', 'medico', 'admin', 'profissional_saude'])
def has_exames(avaliacao_id):
    """
    Verifica se há exames associados a uma avaliação.
    """
    exames = Exame.query.filter_by(avaliacao_id=avaliacao_id).all()
    return jsonify({'has_exames': len(exames) > 0}), 200