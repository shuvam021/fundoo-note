import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save

from api.authentication.tasks import send_email_to_verify_user_task
from api.utils.views import generate_tokens_for_user

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
            send_email_to_verify_user_task.delay(token, instance.email)
        except Exception as e:
            logger.exception(e)


def hash_password_pre_save(sender, instance, *args, **kwargs):
    instance.password = make_password(instance.password)
    return instance


pre_save.connect(hash_password_pre_save, sender=User)
post_save.connect(user_post_save, sender=User)
