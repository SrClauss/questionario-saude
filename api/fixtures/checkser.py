import json
import os

# Estrutura esperada para validação
expected_structure = {
    "titulo": str,
    "descricao": str,
    "versao": str | None,
    "fontes_literatura": list,
    "is_active": bool,
    "sessoes": list
}

expected_fontes_literatura = {
    "titulo": str,
    "autores": str,
    "ano": int | str | None,
}

expected_sessao = {
    "titulo": str,
    "descricao": str | None,
    "ordem": int,
    "perguntas": list
}

expected_pergunta = {
    "texto": str,
    "tipo_resposta": str,
    "metodo_pontuacao": str,
    "ordem": int,
    "is_obrigatoria": bool,
    "alternativas": list
}

expected_alternativa = {
    "texto": str,
    "valor": float,
    "ordem": int
}

# Função para validar a estrutura de um dicionário
def validate_structure(data, expected, path=""):
    errors = []
    for key, expected_type in expected.items():
        if key not in data:
            errors.append(f"Chave ausente: {path}{key}")
        elif not isinstance(data[key], expected_type):
            errors.append(f"Tipo incorreto para {path}{key}: esperado {expected_type}, encontrado {type(data[key])}")
    return errors

# Função para validar listas de dicionários
def validate_list(data, expected, path=""):
    errors = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"Elemento na posição {path}[{i}] não é um dicionário.")
        else:
            errors.extend(validate_structure(item, expected, f"{path}[{i}]."))
    return errors

# Função para validar o JSON completo
def validate_questionario(questionario):
    errors = validate_structure(questionario, expected_structure)
    
    # Validar fontes_literatura
    if "fontes_literatura" in questionario:
        errors.extend(validate_list(questionario["fontes_literatura"], expected_fontes_literatura, "fontes_literatura"))
    
    # Validar sessoes
    if "sessoes" in questionario:
        for i, sessao in enumerate(questionario["sessoes"]):
            path = f"sessoes[{i}]."
            errors.extend(validate_structure(sessao, expected_sessao, path))
            if "perguntas" in sessao:
                for j, pergunta in enumerate(sessao["perguntas"]):
                    path_pergunta = f"{path}perguntas[{j}]."
                    errors.extend(validate_structure(pergunta, expected_pergunta, path_pergunta))
                    if "alternativas" in pergunta:
                        errors.extend(validate_list(pergunta["alternativas"], expected_alternativa, path_pergunta + "alternativas"))
    return errors

# Função para carregar o JSON com informações de linha
def load_json_with_line_numbers(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    decoder = json.JSONDecoder()
    data = []
    idx = 0
    while idx < len(content):
        obj, idx = decoder.raw_decode(content, idx)
        line_number = content[:idx].count('\n') + 1
        data.append((obj, line_number))
        while idx < len(content) and content[idx].isspace():
            idx += 1
    return data

# Caminho relativo ao diretório do script
script_dir = os.path.dirname(__file__)
json_path = os.path.join(script_dir, 'questionario.json')

# Carregar o arquivo JSON com informações de linha
with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Validar cada questionário
for i, questionario in enumerate(data.get("questionarios", [])):
    print(f"Validando questionário {i + 1}...")
    errors = validate_questionario(questionario)
    if errors:
        print(f"Erros encontrados no questionário {i + 1}:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"Questionário {i + 1} está válido.")