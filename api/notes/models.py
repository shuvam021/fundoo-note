from django.db import models


# Create your models here.
class Note(models.Model):
    """ORM for all Notes"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)


class Label(models.Model):
    """ORM for Label table"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    note = models.ManyToManyField('notes.Note')
    color = models.CharField(max_length=50)
