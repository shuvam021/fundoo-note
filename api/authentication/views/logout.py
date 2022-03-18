import logging

from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


# Create your views here.
class LogoutAPIView(APIView):
    def post(self, request):
        print(request.META.get("HTTP_AUTHORIZATION"))
        response = Response()
        if request.COOKIES.get('jwt'):
            response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success'
        }
        return response
