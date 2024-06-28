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
]