import logging

from api.utils.views import CustomEMailer, generate_tokens_for_user
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)


# Create your models here.
class User(AbstractUser):
    """Extend class Default User model with custom fields"""
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']


def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        try:
            token = generate_tokens_for_user(instance)
            CustomEMailer.verification_mail(token, instance.email)
        except Exception as e:
            logger.exception(e)


post_save.connect(user_post_save, sender=User)
