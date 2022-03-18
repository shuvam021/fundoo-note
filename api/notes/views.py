import json
import logging

from api.notes.models import Label, Note
from api.notes.serializers import LabelSerializer, NoteSerializer
from api.utils.views import CustomAuthentication, response
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

logger = logging.getLogger(__name__)


# Create your views here.
class NoteViewset(viewsets.ViewSet):
    serializer_class = NoteSerializer
    authentication_classes = (CustomAuthentication,)
    model = Note

    def list(self, request):
        queryset = Note.objects.filter(user=request.user)
        serialiser = self.serializer_class(queryset, many=True)
        if not cache.get(request.user.id):
            cache.set(request.user.id, serialiser.data)
        data = cache.get(request.user.id)
        return response(data=json.dumps(data), status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # update_cache(get_current_user(request).id, Note)
            return response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return response(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Note, user=request.user, pk=pk)
        serialiser = self.serializer_class(queryset)
        return response(data=serialiser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        data = request.data.copy()
        data['user'] = request.user.id
        try:
            queryset = get_object_or_404(Note, user=request.user, pk=pk)
            serializer = self.serializer_class(queryset, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # update_cache(get_current_user(request).id, Note)
            return response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return response(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Note, user=request.user, pk=pk)
        queryset.delete()
        # update_cache(get_current_user(request).id, Note)
        return response(data={}, status=status.HTTP_204_NO_CONTENT)
