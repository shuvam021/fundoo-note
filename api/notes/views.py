import logging

from api.notes.models import Label, Note
from api.notes.serializers import LabelSerializer, NoteSerializer
from api.utils.views import (CustomAuthentication, CustomIsAuthenticated,
                             response)
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger(__name__)


# Create your views here.
class NoteViewset(viewsets.ViewSet):
    """Note APIs class"""
    serializer_class = NoteSerializer
    authentication_classes = (CustomAuthentication,)
    permission_classes = (CustomIsAuthenticated,)
    model = Note

    @staticmethod
    def update_cache(queryset, user_id):
        """Update cached memory"""
        json_data = [{item.id: model_to_dict(item)} for item in queryset]
        cache.set(int(user_id), json_data)

    def list(self, request):
        """Return list of notes from cached memory"""
        try:
            dataset = cache.get(int(request.user.id))
            data = []
            if dataset:
                data = [v for item in dataset for k, v in item.items()]
            return response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return response(data=[], status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=serializer_class)
    def create(self, request):
        """Add new note to Database and Return it"""
        data = request.data.copy()
        try:
            queryset = Note.objects.filter(user=request.user)
            data['user'] = request.user.id
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.update_cache(queryset, request.user.id)

            return response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return response(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Return the logged in user's note searched by pk from cahed memory"""
        dataset = [i.get(pk) for i in cache.get(int(request.user.id))]
        dataset = list(filter(None, dataset))
        data = {} if dataset == [] else dataset[0]
        return response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class)
    def update(self, request, pk=None):
        """Update the logged in user's note searched by pk and update cached memory"""
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
        """Delete the logged in user's note if exists and update cached memory"""
        queryset = Note.objects.filter(user=request.user)
        query = queryset.get(pk=pk)
        if query:
            query.delete()

        if len(cache.get(request.user.id)) != len(queryset):
            self.update_cache(queryset, request.user.id)

        return response(data={}, status=status.HTTP_204_NO_CONTENT)


class LabelViewSet(viewsets.ViewSet):
    """Label APIs class"""
    authentication_classes = (CustomAuthentication,)
    permission_classes = (CustomIsAuthenticated,)
    serializer_class = LabelSerializer
    model = Label

    def list(self, request):
        """Return list of lebels from database"""
        queryset = Label.objects.all().order_by("pk")
        serializer = self.serializer_class(queryset, many=True)
        return response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class)
    def create(self, request):
        """Save new lebel in the database"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Return lebel searched by pk"""
        queryset = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(queryset)
        return response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class)
    def update(self, request, pk=None):
        """update lebel searched by pk"""
        qs = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(qs, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        """delete lebel"""
        qs = get_object_or_404(self.model, pk=pk)
        qs.delete()
        return response(status=status.HTTP_204_NO_CONTENT)
