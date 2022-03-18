import logging

from api.notes.models import Label, Note
from api.notes.serializers import LabelSerializer, NoteSerializer
from api.utils.views import (CustomAuthentication, CustomIsAuthenticated,
                             response)
from django.core.cache import cache
from django.forms.models import model_to_dict
from rest_framework import status, viewsets

logger = logging.getLogger(__name__)


# Create your views here.
class NoteViewset(viewsets.ViewSet):
    serializer_class = NoteSerializer
    authentication_classes = (CustomAuthentication,)
    permission_classes = (CustomIsAuthenticated,)
    model = Note

    @staticmethod
    def update_cache(queryset, user_id):
        json_data = [{item.id: model_to_dict(item)} for item in queryset]
        cache.set(int(user_id), json_data)

    def list(self, request):
        dataset = cache.get(int(request.user.id))
        data = []
        if dataset:
            data = [v for item in dataset for k, v in item.items()]

        return response(data=data, status=status.HTTP_200_OK)

    def create(self, request):
        queryset = Note.objects.filter(user=request.user)
        data = request.data.copy()
        data['user'] = request.user.id
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if len(cache.get(request.user.id)) != len(queryset):
                self.update_cache(queryset, request.user.id)

            return response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return response(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        dataset = [i.get(pk) for i in cache.get(int(request.user.id))]
        dataset = list(filter(None, dataset))
        data = {} if dataset == [] else dataset[0]
        return response(data=data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Note.objects.filter(user=request.user)
        data = request.data.copy()
        data['user'] = request.user.id
        try:
            query = queryset.get(pk=pk)
            serializer = self.serializer_class(query, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.update_cache(queryset, request.user.id)
            return response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return response(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Note.objects.filter(user=request.user)
        query = queryset.get(pk=pk)
        if query:
            query.delete()

        if len(cache.get(request.user.id)) != len(queryset):
            self.update_cache(queryset, request.user.id)

        return response(data={}, status=status.HTTP_204_NO_CONTENT)
