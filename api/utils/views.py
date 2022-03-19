import logging

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import authentication, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLevelName(__name__)


# Create your views here.
def response(stats, data=None, message=None):
    msg = {
        200: 'Success',
        201: 'Data saved',
        202: 'Retrieved',
        204: 'Deleted',
        400: 'Error',
        401: 'Login required',
        404: 'Data not found',
    }
    if not message and msg.get(stats):
        message = msg[stats]
    res = {
        'status': status,
        'message': message,
        'data': data
    }
    return Response(data=res, status=stats)


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def get_user_id_from_token(token):
    payload = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=['HS256']
    )
    return payload.get('user_id')


def get_current_user(request):
    jwt_authenticator = JWTAuthentication()
    res = jwt_authenticator.authenticate(request)
    if res is not None:
        user, token = res
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
        print(endpoint)

        return cls.send(subject, body, email)

    @classmethod
    def forget_password_mail(cls, token, email, request):
        endpoint = reverse_lazy('api:update_password',
                                kwargs={'token': token},
                                request=request)
        subject = "Change your password"
        body = f"Hii, {email}\n"
        body += f"use this link to change your password\n"
        body += f"{endpoint}"
        return cls.send(subject, body, email)

    @staticmethod
    def send(subject, body, email):
        return send_mail(subject, body, settings.EMAIL_HOST, [email], fail_silently=False)


class CustomAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return None
        try:
            user = get_current_user(request)
            if user:
                return tuple(user, None)
            return None
        except Exception as e:
            logger.exception(e)
            raise exceptions.AuthenticationFailed('No such user')


class CustomIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return None
        try:
            user = get_current_user(request)
            if request.user == user:
                return True
            return False
        except jwt.ExpiredSignatureError as e:
            logger.exception(e)
            raise exceptions.PermissionDenied("token expired")
