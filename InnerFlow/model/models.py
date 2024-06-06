from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    profile = models.CharField(max_length=500, blank=True)