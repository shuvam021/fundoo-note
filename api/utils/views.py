from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


def response(status: status, data=None, message=None):
    msg = {
        200: 'Success',
        400: 'Error',
        401: 'Login required',
        404: 'Data not found',
    }
    if not message and msg.get(status):
        message = msg[status]
    res = {
        'status': status,
        'message': message,
        'data': data
    }
    return Response(data=res, status=status)


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def get_current_user(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        user, token = response
        return user
    return None


class CustomEMailer:
    @classmethod
    def verification_mail(cls, token, email):
        endpoint = settings.SITE_URI + \
            reverse('api:verify', kwargs={'token': token})
        subject = "New user Verification Notifier"
        body = "Try this link to verify your account\n"
        body += f"{endpoint}"

        return cls.mail_send(subject, body, email)

    @staticmethod
    def mail_send(subject, body, email):
        return send_mail(subject, body, settings.EMAIL_HOST, [email], fail_silently=False)


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return None
        try:
            user = get_current_user(request)
        except:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)
