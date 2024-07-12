from django.db import models
from .user import User
from django.db import models

from .user import User


class Goal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
