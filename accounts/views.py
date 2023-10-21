from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.generics import get_object_or_404

from .models import User
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
def show(request, username):
    user = request.user if username == request.user.username else get_object_or_404(User, username=username)

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

    return render(request, "accounts/users/show.html", {
        "user": user,
        "posts": user.post_set.all(),
        "conversations": conversations,
        "user_friends_count": 0,
        "max_user_friends": 20,
    })


@login_required(login_url="login")
def edit(request, username):
    if username != request.user.username:
        return redirect("posts.index")

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
def destroy(request):
    request.user.delete()
    return redirect("home")