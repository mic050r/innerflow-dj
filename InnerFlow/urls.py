from django.contrib import admin
from django.urls import path, include

from InnerFlow.views import home_views, auth_views, board_views, goal_views, journal_views

urlpatterns = [
    # 어드민
    path('admin/', admin.site.urls),

    # 인덱스, 홈
    path('home/', home_views.home, name='home'),
    path('', home_views.index, name='index'),

    # 카카오 로그인
    path('kakao/login/', auth_views.kakao_login, name='kakao_login'),
    path('kakao/login/callback/', auth_views.kakao_callback, name='kakao_callback'),
    path('check-session/', auth_views.check_session, name='check_session'),  # 세션 확인

    # 익명게시판
    path('boards/', board_views.board_list, name='board_list'),
    path('boards/<int:board_id>/', board_views.board_detail, name='board_detail'),
    path('boards/create/', board_views.board_create, name='board_create'),
    path('boards/<int:board_id>/update/', board_views.board_update, name='board_update'),
    path('boards/<int:board_id>/delete/', board_views.board_delete, name='board_delete'),
    path('boards/filter/<str:filter_type>/', board_views.board_filter, name='board_filter'),
    path('boards/<int:board_id>/comments/create/', board_views.comment_create, name='comment_create'),
    path('comments/<int:comment_id>/update/', board_views.comment_update, name='comment_update'),
    path('comments/<int:comment_id>/delete/', board_views.comment_delete, name='comment_delete'),

    # 목표 설정
    path('goal/', goal_views.goal_list, name='goal_list'),
    path('goal/create/', goal_views.goal_create, name='goal_create'),
    path('goal/<int:goal_id>/update/', goal_views.goal_update, name='goal_update'),
    path('goal/<int:goal_id>/delete/', goal_views.goal_delete, name='goal_delete'),
    path('goal/<int:goal_id>/todos/', goal_views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/update/', goal_views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', goal_views.todo_delete, name='todo_delete'),
    path('todo/<int:todo_id>/update_checked/', goal_views.update_checked, name='update_checked'),

    # 성취일지 & 칭찬일지
    path('daily-log/', journal_views.daily_log, name='daily_log'),
    path('delete-praise/<int:praise_id>/', journal_views.delete_praise, name='delete_praise'),
    path('achievement/<str:date>/', journal_views.achievement_form, name='achievement_form'),
    path('achievement/<int:achievement_id>/', journal_views.achievement_detail, name='achievement_detail'),
    path('events/', journal_views.events, name='events'),
]
