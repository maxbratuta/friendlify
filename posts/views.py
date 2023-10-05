from django.shortcuts import render

from posts.models import Post


def feed(request):
    posts = Post.objects.all()

    return render(request, "posts/index.html", {
        "posts": posts
    })
