from django import forms
from .models import Board, Comment, Goal, Todo, Achievement, Praise


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'date', 'keyword', 'temperature', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PraiseForm(forms.ModelForm):
    class Meta:
        model = Praise
        fields = ['content']