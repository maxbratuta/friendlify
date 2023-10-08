from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from posts.models import Post


@login_required(login_url='login')
def feed(request):
    posts = Post.objects.all()
    return render(request, "posts/index.html", {"posts": posts})
