from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User, Friendship
from posts.models import Post


@login_required(login_url="login")
def index(request):
    conversations = [
        {
            'id': 200001,
            'friend': User.objects.filter(username="ola_hombre").get(),
            'last_message': 'Gorgeous!',
        },
        {
            'id': 200002,
            'friend': User.objects.filter(username="paulina_sombrero").get(),
            'last_message': 'Hola!',
        },
        {
            'id': 200003,
            'friend': User.objects.filter(username="hose_horse").get(),
            'last_message': 'Muy bien :)',
        },
    ]
    conversations = []  # TODO : get all conversations with friends

    friendships = Friendship.get_accepted_friendships(user=request.user)

    return render(request, "posts/feed.html", {
        "friends": Friendship.get_friends(friendships=friendships, user=request.user),
        "posts": Post.get_posts(friendships=friendships, user=request.user),
        "conversations": conversations,
    })


def store(request):
    if request.method == "POST":
        image = request.FILES.get("capturedPhoto", None)

        if not image:
            messages.error(request, "Image is required")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

        post = Post.objects.create(
            user=request.user,
            image=image,
            description=request.POST.get("post_message", None),
        )

        friends = User.objects.all()  # TODO : get friends list from POST

        post.participants.set(friends)

    return redirect("posts.index")


@login_required(login_url="login")
def destroy(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=id)

        if request.user != post.user:
            return HttpResponse("You do not have permission to perform this action.", status=403)

        post.delete()

        messages.success(request, "Post has been deleted!")

    return redirect("posts.index")
