from flask_mail import Message
from extensions import mail  # Importa a instância 'mail' do arquivo extensions.py
import os
from flask import current_app

#.env
#CONFIRMATION_EMAIL_URL=http://localhost:3000/confirm-email

def send_confirmation_email_and_set_password(token, receiver):
    with current_app.app_context():
        msg = Message('Confirme seu e-mail', recipients=[receiver])
        msg.body = f'Clique no link para confirmar seu e-mail e definir senha: {os.getenv("CONFIRMATION_EMAIL_URL")}/{token}'
        mail.send(msg)  # Usa a instância 'mail' importada

def send_reset_password_email(token, receiver):
    with current_app.app_context():
        msg = Message('Redefina sua senha', recipients=[receiver])
        msg.body = f'Clique no link para redefinir sua senha: {os.getenv("CONFIRMATION_EMAIL_URL")}/{token}'
        mail.send(msg)  # Usa a instância 'mail' importada

def send_email(subject, body, receiver):
    with current_app.app_context():
        msg = Message(subject, recipients=[receiver])
        msg.body = body
        mail.send(msg)  # Usa a instância 'mail' importada