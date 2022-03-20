import logging

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLevelName(__name__)


# Create your views here.
def response(status, data=None, message=None):
    msg = {
        200: 'Success',
        201: 'Data saved',
        202: 'Retrieved',
        204: 'Deleted',
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

class CustomAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return None
        try:
            user = get_current_user(request)
            if user:
                return (user, None)
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
