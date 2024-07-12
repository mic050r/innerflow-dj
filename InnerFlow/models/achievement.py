from django.db import models
from .user import User
from django.db import models

from .user import User


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    keyword = keyword = models.TextField()
    temperature = models.IntegerField()
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
