from flask import current_app, render_template
from flask_mail import Message


def send_activation_token(email, subject, sender, url, token):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=[email],
        html=render_template('accounts/activation_mail.html',
                             url=url, token=token.decode('ascii'))
    )
    current_app.extensions['mailer'].send(msg)
