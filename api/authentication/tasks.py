from celery import shared_task
from config.celery import app as celery_app
from django.conf import settings
from django.core.mail import send_mail


def forget_password_email(token, email):
    subject = "Change your password"
    body = f"Hii, {email}\n"
    body += f"use this link to change your password\n"
    body += f"http://127.0.0.1:8000/api/update_password/{token}"
    return send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

def verification_mail(token, email):
    subject = "New user Verification Notifier"
    body = "Try this link to verify your account\n"
    body += f"f'http://127.0.0.1:8000/api/verify/{token}/'"
    return send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)


# @celery_app.task(name='send_forget_password_task')
@shared_task
def send_forget_password_task(token, email):
    forget_password_email(token, email)
    return('send_forget_password_task')


@celery_app.task(name='send_email_to_verify_user_task')
def send_email_to_verify_user_task(token, email):
    forget_password_email(token, email)
    return('send_email_to_verify_user_task')
