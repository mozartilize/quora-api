from flask import current_app, render_template
from flask_mail import Message


def send_activation_token(email, token):
    msg = Message(
        subject='Activate Quora account',
        sender=('Quora Team', 'no-reply.support@quora.com'),
        recipients=[email],
        html=render_template('accounts/activation_mail.html',
                             token=token.decode('ascii'))
    )
    current_app.extensions['mailer'].send(msg)
