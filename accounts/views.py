from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from posts.models import Post
from .forms import UserForm, UserStoreForm
from .models import User, Friendship


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

    return render(request, "accounts/auth/login.html")


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

    return render(request, "accounts/auth/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def user_show(request, username):
    conversations = []  # TODO : get all conversations with friendships

    is_friendship_received = False
    is_friendship_sent = False
    is_friends = False

    posts = []
    friends_count = 0

    if username == request.user.username:
        user = request.user
        posts = user.post_set.all()

        friends_count = len(Friendship.get_friends(user=request.user))  # TODO : reuse with conversations
    else:
        user = get_object_or_404(User, username=username)

        is_friends, \
            is_friendship_received, \
            is_friendship_sent, \
            friendship = get_friendship_statuses(friend_1=user, friend_2=request.user)

        if is_friends:
            posts = Post.get_posts(friendship_dates=friendship.get_dates(), exclude_for_user=request.user)

    return render(request, "accounts/users/show.html", {
        "pending_requests_count": Friendship.get_pending_friends_count_as_receiver(user=request.user),
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

    return render(request, "accounts/users/edit.html", {
        "pending_requests_count": Friendship.get_pending_friends_count_as_receiver(user=request.user),
        "form": form
    })


@login_required(login_url="login")
def user_destroy(request):
    request.user.delete()
    return redirect("home")


@login_required(login_url="login")
def send_friend_request(request, username):
    if request.method == "POST":
        user = get_object_or_404(User, username=username)

        friendship = Friendship.get_friendships(friend_1=request.user, friend_2=user).first()

        if friendship:
            messages.info(request, "The friendship is already created.")
            return redirect("users.show", username)

        friendships_count = Friendship.get_friendships(friend_1=request.user).count()

        if friendships_count < Friendship.USER_FRIENDS_LIMIT:
            Friendship.objects.create(sender=request.user, receiver=user)
        else:
            messages.error(request, "Allowed number of friendships exceeded."
                                    f"You can have up to { Friendship.USER_FRIENDS_LIMIT } friendships at a time.")

        # TODO : send notification to receiver
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def accept_friend_request(request, username):
    if request.method == "POST":
        pending_friendship = Friendship.get_specific_friendship(
            sender=get_object_or_404(User, username=username),
            receiver=request.user,
            status=Friendship.PENDING
        ).first()

        # TODO : add verification to: receiver have friends limit, than sender send request and receiver accept it

        if pending_friendship:
            pending_friendship.accept()
            # TODO : send notification to receiver
        else:
            messages.error(request, "The friendship you are referring to does not exist!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def friendship_destroy(request, username):
    if request.method == "POST":
        friendship = Friendship.get_friendships(
            friend_1=request.user,
            friend_2=get_object_or_404(User, username=username),
        ).first()

        if friendship:
            friendship.destroy()
            # TODO : send notification to receiver
        else:
            messages.error(request, "The friendship you are referring to does not exist!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def friendship_index(request):
    conversations = []  # TODO : get all conversations with friendships

    friends = Friendship.get_friends(user=request.user)

    return render(request, "accounts/friendships/index.html", {
        "pending_requests_count": Friendship.get_pending_friends_count_as_receiver(user=request.user),
        "friendship": {
            'friends_count': len(friends),
            "user_friends_limit": Friendship.USER_FRIENDS_LIMIT,
            "friends": friends,
            "pending_friends": {
                "as_sender": Friendship.get_pending_friends_as_sender(user=request.user),
                "as_receiver": Friendship.get_pending_friends_as_receiver(user=request.user),
            }
        },
        "conversations": conversations,
    })


def user_search(request):
    query = request.GET.get("q")

    filtered_users = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )[:5] if query else []

    data = []

    for user in filtered_users:
        is_friends, \
            is_friendship_received, \
            is_friendship_sent, \
            friendship = get_friendship_statuses(friend_1=user, friend_2=request.user)

        if user == request.user:
            status = {"value": "You", "style": "dark"}
        elif is_friends:
            status = {"value": "Friend", "style": "success"}
        elif is_friendship_received:
            status = {"value": "Incoming request", "style": "primary"}
        elif is_friendship_sent:
            status = {"value": "Outcoming request", "style": "secondary"}
        else:
            status = None

        data.append({
            "ref_link": reverse("users.show", args=[user.username]),
            "username": user.username,
            "avatar": user.avatar.url if user.avatar else None,
            "initials": user.initials,
            "full_name": user.get_full_name(),
            "friendship_status": status,
        })

    return JsonResponse({"data": data})


def get_friendship_statuses(friend_1: User, friend_2: User):
    is_friends = False
    is_friendship_received = False
    is_friendship_sent = False

    friendship = Friendship.get_friendships(friend_1=friend_2, friend_2=friend_1)

    if friendship:
        if friendship.first().is_accepted():
            is_friends = True
        else:
            is_friendship_received = Friendship.is_pending_friendship_exists(sender=friend_1, receiver=friend_2)
            is_friendship_sent = not is_friendship_received

    return is_friends, is_friendship_received, is_friendship_sent, friendship
