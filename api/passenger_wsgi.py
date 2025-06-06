import importlib.util
import os
import sys

# Adicione o diretório atual ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Carregue o módulo app.py dinamicamente
spec = importlib.util.spec_from_file_location("app", "app.py")
wsgi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wsgi)

# Crie a aplicação Flask usando a função create_app
application = wsgi.create_app()