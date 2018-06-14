from flask import current_app
from flask_mail import Message


def send_activation_token(email, token):
    template = current_app.jinja_env.get_template('accounts/activation_mail.html')
    msg = Message(
        subject='Activate Quora account',
        sender=('Quora Team', 'no-reply.support@quora.com'),
        recipients=[email],
        html=template.render(token=token.decode('ascii'))
    )
    current_app.extensions['mailer'].send(msg)
