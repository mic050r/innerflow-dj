import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from InnerFlow.forms import TodoForm, GoalForm
from InnerFlow.models import User, Todo, Goal


def goal_list(request):
    kakao_id = request.session.get('kakao_id')
    goals = Goal.objects.filter(user__kakao_id=kakao_id)
    goal_stats = []
    for goal in goals:
        todos = Todo.objects.filter(goal=goal)
        total_todos = todos.count()
        completed_todos = todos.filter(checked=True).count()
        if total_todos > 0:
            completion_rate = (completed_todos / total_todos) * 100
        else:
            completion_rate = 0
        goal_stats.append({
            'goal': goal,
            'total_todos': total_todos,
            'completed_todos': completed_todos,
            'completion_rate': completion_rate,
        })
    return render(request, 'goal/goal_list.html', {'goal_stats': goal_stats})


def goal_create(request):
    kakao_id = request.session.get('kakao_id')
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            user = User.objects.get(kakao_id=kakao_id)
            goal.user = user
            goal.save()
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'goal/goal_form.html', {'form': form})


def goal_update(request, goal_id):
    kakao_id = request.session.get('kakao_id')
    goal = get_object_or_404(Goal, pk=goal_id, user__kakao_id=kakao_id)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goal/goal_form.html', {'form': form})


def goal_delete(request, goal_id):
    kakao_id = request.session.get('kakao_id')
    goal = get_object_or_404(Goal, pk=goal_id, user__kakao_id=kakao_id)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'goal/goal_confirm_delete.html', {'goal': goal})


def todo_list(request, goal_id):
    kakao_id = request.session.get('kakao_id')
    goal = get_object_or_404(Goal, pk=goal_id, user__kakao_id=kakao_id)
    todos = Todo.objects.filter(goal=goal)

    # 목표 진행 상황 계산
    total_todos = todos.count()
    completed_todos = todos.filter(checked=True).count()
    completion_rate = (completed_todos / total_todos) * 100 if total_todos > 0 else 0

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.goal = goal
            todo.save()
            return redirect('todo_list', goal_id=goal_id)
    else:
        form = TodoForm()

    return render(request, 'goal/todo_list.html', {
        'goal': goal,
        'todos': todos,
        'form': form,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'completion_rate': round(completion_rate),
    })


def todo_update(request, todo_id):
    kakao_id = request.session.get('kakao_id')
    todo = get_object_or_404(Todo, pk=todo_id, goal__user__kakao_id=kakao_id)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list', goal_id=todo.goal.goal_id)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'goal/todo_form.html', {'form': form})


@require_POST
def update_checked(request, todo_id):
    kakao_id = request.session.get('kakao_id')
    todo = get_object_or_404(Todo, pk=todo_id, goal__user__kakao_id=kakao_id)
    data = json.loads(request.body)
    todo.checked = data.get('checked', False)
    todo.save()
    return JsonResponse({'status': 'success'})


def todo_delete(request, todo_id):
    kakao_id = request.session.get('kakao_id')
    todo = get_object_or_404(Todo, pk=todo_id, goal__user__kakao_id=kakao_id)
    goal_id = todo.goal.goal_id
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list', goal_id=goal_id)
    return render(request, 'goal/todo_confirm_delete.html', {'todo': todo})
