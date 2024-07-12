from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from InnerFlow.forms import AchievementForm, PraiseForm
from InnerFlow.models import User, Achievement, Praise


# .env 파일에서 환경 변수를 불러오기


def daily_log(request):
    kakao_id = request.session.get('kakao_id')
    praises = Praise.objects.filter(user__kakao_id=kakao_id).order_by('-created_at')  # 최신순으로
    achievements = Achievement.objects.filter(user__kakao_id=kakao_id)
    praise_form = PraiseForm()

    if request.method == 'POST':
        praise_form = PraiseForm(request.POST)
        if praise_form.is_valid():
            praise = praise_form.save(commit=False)
            praise.user = User.objects.get(kakao_id=kakao_id)
            praise.save()
            return redirect('daily_log')

    return render(request, 'journal/daily_log.html', {
        'praise_form': praise_form,
        'praises': praises,
        'achievements': achievements
    })


def delete_praise(request, praise_id):
    kakao_id = request.session.get('kakao_id')
    praise = get_object_or_404(Praise, id=praise_id, user__kakao_id=kakao_id)
    if request.method == 'POST':
        praise.delete()
        return redirect('daily_log')


def achievement_form(request, date):
    kakao_id = request.session.get('kakao_id')
    achievement = Achievement.objects.filter(user__kakao_id=kakao_id, date=date).first()
    if request.method == 'POST':
        form = AchievementForm(request.POST, instance=achievement)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = User.objects.get(kakao_id=kakao_id)
            achievement.save()
            return redirect('daily_log')
    else:
        form = AchievementForm(instance=achievement, initial={'date': date})  # 초기값으로 date를 설정

    return render(request, 'journal/achievement_form.html', {'form': form, 'date': date})


def achievement_detail(request, achievement_id):
    kakao_id = request.session.get('kakao_id')
    achievement = get_object_or_404(Achievement, id=achievement_id, user__kakao_id=kakao_id)
    return render(request, 'journal/achievement_detail.html', {'achievement': achievement})


def events(request):
    kakao_id = request.session.get('kakao_id')
    achievements = Achievement.objects.filter(user__kakao_id=kakao_id)
    events = []
    for achievement in achievements:
        events.append({
            'id': achievement.id,
            'title': achievement.title,
            'start': achievement.date.isoformat(),
            'end': achievement.date.isoformat(),
        })
    return JsonResponse(events, safe=False)
