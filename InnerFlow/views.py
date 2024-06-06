import os

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
import requests
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlencode

# .env 파일에서 환경 변수를 불러오기
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


# 카카오 로그인 페이지로 리다이렉트하는 함수
def kakao_login(request):
    kakao_redirect_uri = 'http://localhost:8000/kakao/login/callback/'
    KAKAO_APP_KEY = os.getenv('KAKAO_APP_KEY')  # 환경 변수에서 애플리케이션 키를 불러오기

    # 카카오 인증 페이지로 리다이렉트
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_APP_KEY}&redirect_uri={kakao_redirect_uri}&response_type=code'
    )


# 카카오 로그인 콜백을 처리하는 함수
def kakao_callback(request):
    code = request.GET.get('code')  # 카카오에서 반환한 인증 코드를 가져오기

    if not code:
        return HttpResponse("Error: Authorization code not provided.")  # 인증 코드가 없을 경우 에러 반환

    kakao_token_url = 'https://kauth.kakao.com/oauth/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('KAKAO_APP_KEY'),  # 환경 변수에서 클라이언트 ID를 불러오기
        'client_secret': os.getenv('KAKAO_CLIENT_SECRET'),  # 환경 변수에서 클라이언트 시크릿을 불러오기
        'redirect_uri': 'http://localhost:8000/kakao/login/callback/',
        'code': code,
    }

    # 데이터를 URL-encoded 형식으로 변환
    encoded_data = urlencode(data)
    response = requests.post(kakao_token_url, headers=headers, data=encoded_data)

    # TODO : accesssToken session에 담기
    try:
        response_data = response.json()

        if response.status_code != 200:
            return HttpResponse(f"Error: {response_data.get('error_description')}")  # 응답 상태가 200이 아니면 에러 반환

        access_token = response_data.get('access_token')

        if not access_token:
            raise KeyError('access_token not found')  # 액세스 토큰이 없을 경우 예외 발생

        # 액세스 토큰을 사용하여 사용자 정보를 가져오는 요청
        kakao_profile_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(kakao_profile_url, headers=headers)
        profile = profile_response.json()
        print(profile)  # 사용자 정보를 출력

        return HttpResponseRedirect('/home/')

    except KeyError as e:
        return HttpResponse(f"Error: {str(e)}")  # 예외 발생 시 에러 메시지 반환