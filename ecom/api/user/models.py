from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=250, unique=True)

    username = None                # we don't want username field as username
    USERNAME_FIELD = 'email'        # now in django/admin it will ask for email to login
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
   
    session_token = models.CharField(max_length=10, default=0)
    #as django doesn't work on these tokens so we will be using this to generator a lot of token and stuff

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)