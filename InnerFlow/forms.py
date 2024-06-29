from django import forms
from .models import Board, Comment, Goal, Todo, Achievement, Praise

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목 입력', 'class': 'title-input'}),
            'content': forms.Textarea(attrs={'placeholder': '글을 작성해주세요'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '답변하기'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal']
        widgets = {
            'goal': forms.TextInput(attrs={'placeholder': '목표를 입력해주세요'}),
        }

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo']
        widgets = {
            'todo': forms.TextInput(attrs={'placeholder': '할 일을 입력해주세요'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'date', 'keyword', 'temperature', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '제목 입력',
                'class': 'borderless-title'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'borderless-date'
            }),
            'keyword': forms.TextInput(attrs={
                'placeholder': '키워드를 입력해주세요',
                'class': 'borderless-keyword'
            }),
            'temperature': forms.NumberInput(attrs={
                'placeholder': '온도를 체크해주세요',
                'type': 'range',
                'min': '0',
                'max': '100',
                'step': '1',
                'class': 'borderless-slider',
                'oninput': 'updateTemperatureValue(this.value)'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': '글을 작성해주세요',
                'class': 'borderless-content'
            }),
        }

class PraiseForm(forms.ModelForm):
    class Meta:
        model = Praise
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '칭찬 내용을 입력해주세요'}),
        }
