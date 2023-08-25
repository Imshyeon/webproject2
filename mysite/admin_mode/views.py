from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Comment


def admin_mode(request):
    users = User.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()

    context = {
        'users': users,
        'posts': posts,
        'comments': comments,
    }

    return render(request, 'admin_mode.html', context)
