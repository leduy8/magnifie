from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.connect()
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_team_account_email(user, password):
    send_email(
        '[IMPORTANT] Your judge\'s account',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/send_info_judge.txt', user=user, password=password),
        html_body=render_template('email/send_info_judge.html', user=user, password=password)
    )