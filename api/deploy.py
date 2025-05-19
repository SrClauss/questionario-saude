# zip_project.py
import os
import zipfile

EXCLUDE_DIRS = {'__pycache__', '.vscode', 'venv'}
OUTPUT_ZIP = 'projeto-noemi.zip'

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        # Remove diretórios a serem ignorados
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, path)
            ziph.write(filepath, arcname)

if __name__ == '__main__':
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('.', zipf)
    print(f'Projeto zipado em {OUTPUT_ZIP}')