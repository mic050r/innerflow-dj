"""
URL configuration for InnerFlow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from InnerFlow import views

urlpatterns = [
    # 어드민
    path('admin/', admin.site.urls),

    # 인덱스, 홈
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),

    # 카카오 로그인
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/login/callback/', views.kakao_callback, name='kakao_callback'),
    path('check-session/', views.check_session, name='check_session'),  # 세션 확인

    # 익명게시판
    path('boards/', views.board_list, name='board_list'),
    path('boards/<int:board_id>/', views.board_detail, name='board_detail'),
    path('boards/create/', views.board_create, name='board_create'),
    path('boards/<int:board_id>/update/', views.board_update, name='board_update'),
    path('boards/<int:board_id>/delete/', views.board_delete, name='board_delete'),
    path('boards/filter/<str:filter_type>/', views.board_filter, name='board_filter'),
    path('boards/<int:board_id>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # 목표 설정
    path('goal/', views.goal_list, name='goal_list'),
    path('goal/create/', views.goal_create, name='goal_create'),
    path('goal/<int:goal_id>/update/', views.goal_update, name='goal_update'),
    path('goal/<int:goal_id>/delete/', views.goal_delete, name='goal_delete'),
    path('goal/<int:goal_id>/todos/', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
    path('todo/<int:todo_id>/update_checked/', views.update_checked, name='update_checked'),

    # 성취일지 & 칭찬일지
    path('daily-log/', views.daily_log, name='daily_log'),
    path('delete-praise/<int:praise_id>/', views.delete_praise, name='delete_praise'),
    path('achievement/<str:date>/', views.achievement_form, name='achievement_form'),
    path('achievement/<int:achievement_id>/', views.achievement_detail, name='achievement_detail'),
    path('events/', views.events, name='events'),
]
