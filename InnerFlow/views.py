import os
import json
from venv import logger
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden
import requests
from django.http import HttpResponse
from urllib.parse import urlencode
from django.shortcuts import render, get_object_or_404, redirect

# .env 파일에서 환경 변수를 불러오기
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken

from InnerFlow.forms import BoardForm, CommentForm
from InnerFlow.models import User, Board, Comment

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)

load_dotenv()

def index(request):
    return render(request, 'index.html')

def home(request):
    with open('./InnerFlow/static/data/info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(data)
    return render(request, 'home.html', {'data': json.dumps(data)})


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

        kakao_id = profile["id"]
        kakao_nickname = profile["properties"]["nickname"]

        user, created = User.objects.get_or_create(kakao_id=kakao_id, defaults={"profile": kakao_profile_url,
                                                                                      "nickname": kakao_nickname})
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # 세션에 저장
        request.session['access_token'] = str(access)
        request.session['refresh_token'] = str(refresh)
        request.session['kakao_id'] = str(kakao_id)
        print(request.session.get('kakao_id'))

        return redirect('/home/')  # 로그인 성공 후 /home으로 리다이렉트

    except KeyError as e:
        return HttpResponse(f"Error: {str(e)}")  # 예외 발생 시 에러 메시지 반환

def check_session(request):
    access_token = request.session.get('access_token', 'No access token in session')
    refresh_token = request.session.get('refresh_token', 'No refresh token in session')
    return JsonResponse({
        'access_token': access_token,
        'refresh_token': refresh_token
    })

   
def board_list(request):
    boards = Board.objects.all()
    return render(request, 'board_list.html', {'boards': boards})

   
def board_detail(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    comments = Comment.objects.filter(board=board)
    return render(request, 'board_detail.html', {'board': board, 'comments': comments})

   
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            kakao_id = request.session.get('kakao_id')
            if not kakao_id:
                return HttpResponse("Error: Kakao ID not found in session")

            try:
                user = User.objects.get(kakao_id=kakao_id)
                board.user = user
                board.save()
                return redirect('board_list')
            except User.DoesNotExist:
                return HttpResponse("Error: User not found")
    else:
        form = BoardForm()
    return render(request, 'board_form.html', {'form': form})

   
def board_update(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    kakao_id = request.session.get('kakao_id')
    print("board", board.user.kakao_id)
    print("login", kakao_id)
    if board.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to edit this board.")

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.board_id)
    else:
        form = BoardForm(instance=board)
    return render(request, 'board_form.html', {'form': form})

   
def board_delete(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    kakao_id = request.session.get('kakao_id')
    if board.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to delete this board.")

    if request.method == 'POST':
        board.delete()
        return redirect('board_list')
    return render(request, 'board_confirm_delete.html', {'board': board})

   
def comment_create(request, board_id):
    board = get_object_or_404(Board, pk=board_id, user__kakao_id=request.session.get('kakao_id'))
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            kakao_id = request.session.get('kakao_id')
            if not kakao_id:
                return HttpResponse("Error: Kakao ID not found in session")

            try:
                user = User.objects.get(kakao_id=kakao_id)
                comment.user = user
                comment.board = board
                comment.save()
                return redirect('board_detail', board_id=board_id)
            except User.DoesNotExist:
                return HttpResponse("Error: User not found")
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})

   
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    kakao_id = request.session.get('kakao_id')
    if comment.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=comment.board.board_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_form.html', {'form': form})

   
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    kakao_id = request.session.get('kakao_id')
    if comment.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('board_detail', board_id=comment.board.board_id)
    return render(request, 'comment_confirm_delete.html', {'comment': comment})