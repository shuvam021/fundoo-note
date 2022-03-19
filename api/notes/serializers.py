from rest_framework import serializers

from .models import Label, Note


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for NoteModel"""
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'user')


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for LabelModel"""
    class Meta:
        model = Label
        fields = ('id', 'title', 'author', 'color', 'note')
