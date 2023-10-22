from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.generics import get_object_or_404

from posts.models import Post
from .models import User, Friendship
from .forms import UserStoreForm, UserForm


def login_page(request):
    if request.user.is_authenticated:
        return redirect("posts.index")

    if request.method == "POST":
        email = request.POST.get("email", "").lower()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember_me", False)

        if not User.objects.filter(email=email).exists():
            messages.error(request, "The given email does not exist")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user:
            if remember_me:
                request.session.set_expiry(86400 * 30)  # 30 days

            login(request, user)
            return redirect("posts.index")
        else:
            messages.error(request, "Invalid password")
            return redirect("login")

    return render(request, "accounts/login.html")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("posts.index")

    if request.method == "POST":
        form = UserStoreForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("posts.index")
        else:
            error_messages = []

            for field_errors in form.errors.as_data().values():
                for error in field_errors:
                    error_messages.extend(error)

            messages.error(request, ". ".join(error_messages))
    else:
        form = UserStoreForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def user_show(request, username):
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

    is_friendship_received = False
    is_friendship_sent = False
    is_friends = False

    posts = []
    friends_count = 0

    friendships = Friendship.get_accepted_friendships(user=request.user)

    if username == request.user.username:
        user = request.user
        posts = user.post_set.all()
        friends_count = friendships.count()
    else:
        user = get_object_or_404(User, username=username)

        is_friendship_received = Friendship.objects.filter(
            sender=user,
            receiver=request.user,
            status=Friendship.PENDING
        ).exists()

        is_friendship_sent = Friendship.objects.filter(
            sender=request.user,
            receiver=user,
            status=Friendship.PENDING
        ).exists()

        if not is_friendship_received and not is_friendship_sent:
            specific_friendship = Friendship.objects.filter(
                Q(sender=request.user, receiver=user) |
                Q(sender=user, receiver=request.user),
                status=Friendship.ACCEPTED
            )

            is_friends = specific_friendship.exists()

            if is_friends:
                posts = Post.get_posts(friendships=specific_friendship, exclude_for_user=request.user)

    return render(request, "accounts/users/show.html", {
        "user": user,
        "posts": posts,
        "conversations": conversations,  # TODO : CONVERSATIONS

        "friendship": {
            'friends_count': friends_count,
            "user_friends_limit": Friendship.USER_FRIENDS_LIMIT,

            "is_pending_received_friendship": is_friendship_received,
            "is_pending_sent_friendship": is_friendship_sent,
            "is_friend": is_friends,
        }
    })


@login_required(login_url="login")
def user_edit(request, username):
    if username != request.user.username:
        return redirect("users.show", username)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False, request=request)

            if "delete_avatar" in request.POST and user.avatar:
                user.avatar.delete(save=False)

            user.save()

            messages.success(request, "The profile has been updated!")
        else:
            messages.error(request, "The profile has not been updated!")
    else:
        form = UserForm(instance=request.user)

    return render(request, "accounts/users/edit.html", {"form": form})


@login_required(login_url="login")
def user_destroy(request):
    request.user.delete()
    return redirect("home")


@login_required(login_url="login")
def send_friend_request(request, username):
    if request.method == "POST":
        friendships = Friendship.get_accepted_friendships(user=request.user)

        if friendships.count() < Friendship.USER_FRIENDS_LIMIT:
            Friendship.objects.get_or_create(
                sender=request.user,
                receiver=get_object_or_404(User, username=username)
            )
        else:
            messages.error(request, "Allowed number of friends exceeded. You can have up to 20 friends at a time")

        # TODO : send notification to receiver
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def accept_friend_request(request, username):
    if request.method == "POST":
        friendship = get_object_or_404(
            Friendship,
            sender=get_object_or_404(User, username=username),
            receiver=request.user
        )

        friendship.accept()
        # TODO : send notification to receiver

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def friendship_destroy(request, username):
    if request.method == "POST":
        user = get_object_or_404(User, username=username)

        friendship = get_object_or_404(
            Friendship,
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        )

        friendship.destroy()
        # TODO : send notification to receiver

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
