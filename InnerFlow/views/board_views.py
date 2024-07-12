from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from InnerFlow.forms import BoardForm, CommentForm
from InnerFlow.models import Board, Comment, User


def board_list(request):
    query = request.GET.get('q')
    if query:
        boards = Board.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        boards = Board.objects.all().order_by('-created_at')
    return render(request, 'board/board_list.html', {'boards': boards})


def board_detail(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    comments = Comment.objects.filter(board=board)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = CommentForm()

    return render(request, 'board/board_detail.html', {
        'board': board,
        'comments': comments,
        'form': form
    })


def board_filter(request, filter_type):
    kakao_id = request.session.get('kakao_id')
    if filter_type == 'all':
        boards = Board.objects.all().order_by('-created_at')
    elif filter_type == 'waiting':
        boards = Board.objects.filter(comments__isnull=True).order_by('-created_at')
    elif filter_type == 'my_posts':
        boards = Board.objects.filter(user__kakao_id=kakao_id).order_by('-created_at')
    else:
        boards = Board.objects.all().order_by('-created_at')

    return render(request, 'board/board_list.html', {'boards': boards})


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
    return render(request, 'board/board_form.html', {'form': form})


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
    return render(request, 'board/board_form.html', {'form': form})


def board_delete(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    kakao_id = request.session.get('kakao_id')
    if board.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to delete this board.")

    if request.method == 'POST':
        board.delete()
        return redirect('board_list')
    return render(request, 'board/board_confirm_delete.html', {'board': board})


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
    return render(request, 'board/comment_form.html', {'form': form})


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
    return render(request, 'board/comment_form.html', {'form': form})


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    kakao_id = request.session.get('kakao_id')
    if comment.user.kakao_id != kakao_id:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('board_detail', board_id=comment.board.board_id)
    return render(request, 'board/comment_confirm_delete.html', {'comment': comment})
