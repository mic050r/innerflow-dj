from django.db import models
from .goal import Goal


class Todo(models.Model):
    todo_id = models.AutoField(primary_key=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    todo = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)