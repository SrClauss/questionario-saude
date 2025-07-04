# d:\Source\projeto-noemi\api\utils\security.py (NOVO ARQUIVO ou adicionar a um existente)
from cryptography.fernet import Fernet, InvalidToken # Importar InvalidToken
import qrcode
import io
import base64
import os
from urllib.parse import quote_plus, unquote_plus

# Carregar a chave de uma variável de ambiente
# Gere uma chave com Fernet.generate_key() e armazene-a de forma segura
ENCRYPTION_KEY = os.getenv('PDF_SIGNATURE_ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    raise ValueError("Chave de criptografia PDF_SIGNATURE_ENCRYPTION_KEY não definida.")

cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data_for_qr(medico_id: str, timestamp: str) -> str:
    """Criptografa dados para serem incluídos no QR code."""
    data_string = f"{medico_id}|{timestamp}"
    encrypted_data = cipher_suite.encrypt(data_string.encode())
    # URL-safe base64 encoding and then URL encode for safety in URL path
    return quote_plus(base64.urlsafe_b64encode(encrypted_data).decode())
# security.py
# ... (imports e configuração da chave) ...

def decrypt_data_from_qr(encrypted_url_safe_data: str) -> tuple[str, str] | None:
    """Descriptografa dados de um QR code."""
    print(f"[decrypt_data_from_qr] Recebido encrypted_url_safe_data: {encrypted_url_safe_data}")
    try:
        # Etapa 1: Decodificar da URL (remover %xx encoding)
        b64_encoded_data_str = unquote_plus(encrypted_url_safe_data)
        print(f"[decrypt_data_from_qr] Após unquote_plus: {b64_encoded_data_str}")
        
        # Etapa 2: Decodificar Base64 URL-safe para bytes
        encrypted_data_bytes = base64.urlsafe_b64decode(b64_encoded_data_str.encode('utf-8'))
        print(f"[decrypt_data_from_qr] Após base64.urlsafe_b64decode (bytes iniciais): {encrypted_data_bytes[:20]}...") 
        
        # Etapa 3: Descriptografar com Fernet
        decrypted_data_bytes = cipher_suite.decrypt(encrypted_data_bytes)
        print(f"[decrypt_data_from_qr] Após cipher_suite.decrypt (bytes): {decrypted_data_bytes}")
        decrypted_data_string = decrypted_data_bytes.decode('utf-8')
        print(f"[decrypt_data_from_qr] Após decode('utf-8'): {decrypted_data_string}")
        
        # Etapa 4: Separar os dados
        medico_id, timestamp = decrypted_data_string.split('|', 1)
        print(f"[decrypt_data_from_qr] Sucesso! Medico ID: {medico_id}, Timestamp: {timestamp}")
        return medico_id, timestamp
    except InvalidToken:
        print("[decrypt_data_from_qr] Erro: Token inválido. Chave incorreta ou dados corrompidos/alterados.")
        return None
    except base64.binascii.Error as b64_error:
        print(f"[decrypt_data_from_qr] Erro: Falha na decodificação Base64. Detalhes: {b64_error}")
        return None
    except ValueError as ve:
        print(f"[decrypt_data_from_qr] Erro: Formato de dados inesperado após descriptografia (split falhou). Detalhes: {ve}")
        return None
    except Exception as e: 
        print(f"[decrypt_data_from_qr] Erro inesperado: {type(e).__name__} - {e}")
        return None
# ...

def generate_qr_code_base64(data_to_encode: str, verification_base_url: str) -> str:
    """Gera um QR code para a URL de verificação e retorna como string base64."""
    qr_url = f"{verification_base_url}/{data_to_encode}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
