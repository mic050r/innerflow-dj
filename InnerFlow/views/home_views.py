import json

from django.shortcuts import render

from InnerFlow.models import Achievement, Goal, Todo


def index(request):
    return render(request, 'index.html')


def home(request):
    kakao_id = request.session.get('kakao_id')
    kakao_nickname = request.session.get('kakao_nickname')

    with open('./InnerFlow/static/data/info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(data)

    # 업적 데이터 가져오기
    achievements = Achievement.objects.filter(user__kakao_id=kakao_id)
    keywords = []
    for achievement in achievements:
        keywords.extend(achievement.keyword.split('/'))

    # 목표 데이터 가져오기 (최신순으로 3개)
    goals = Goal.objects.filter(user__kakao_id=kakao_id).order_by('-created_at')[:3]
    goal_stats = []
    for goal in goals:
        todos = Todo.objects.filter(goal=goal)
        total_todos = todos.count()
        completed_todos = todos.filter(checked=True).count()
        completion_rate = (completed_todos / total_todos) * 100 if total_todos > 0 else 0
        goal_stats.append({
            'goal': goal,
            'total_todos': total_todos,
            'completed_todos': completed_todos,
            'completion_rate': completion_rate,
        })

    return render(request, 'home.html', {
        'data': json.dumps(data),  # 기존의 data 추가
        'keywords': keywords,
        'goal_stats': goal_stats,
        'nickname': kakao_nickname
    })
