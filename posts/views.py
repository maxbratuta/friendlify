from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User, Friendship
from posts.models import Post


@login_required(login_url="login")
def index(request):
    view_filter = request.GET.get("view")
    username_filter = request.GET.get("username")
    user = None

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
    conversations = []  # TODO : get all conversations with friendships

    accepted_friendships = Friendship.get_friendships(friend_1=request.user, status=Friendship.ACCEPTED)

    if username_filter:
        user = User.objects.get(username=username_filter)

        if not user:
            redirect("posts.index", view=view_filter)

        if user == request.user:
            posts = Post.objects.filter(user=request.user)
        else:
            specific_filter_friendship = Friendship.get_friendships(
                friend_1=request.user,
                friend_2=user,
                status=Friendship.ACCEPTED
            )

            posts = Post.objects.filter(
                Q(user=user, updated_at__gte=specific_filter_friendship.get_dates()[user])
            )
    else:
        posts = Post.get_posts(friendship_dates=accepted_friendships.get_dates(), user=request.user)

    return render(request, "posts/feed.html", {
        "pending_requests_count": Friendship.get_pending_friends_count_as_receiver(user=request.user),
        "friends": accepted_friendships.get_friends(user=request.user),
        "posts": posts,
        "conversations": conversations,
        "filter": {
            "view": view_filter,
            "username": username_filter,
            "user_full_name": user.get_full_name() if user else None
        }
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

        friends = User.objects.all()  # TODO : get friendships list from POST

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
