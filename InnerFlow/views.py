from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # 회원가입 성공 시 홈페이지로 리다이렉트
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # 로그인 성공 시 홈페이지로 리다이렉트
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')  # 로그아웃 후 홈페이지로 리다이렉트