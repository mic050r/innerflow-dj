from django.db import models
from .user import User
from django.db import models

from .user import User


class Praise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)