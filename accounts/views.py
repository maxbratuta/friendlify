from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import User
from .forms import MyUserCreationForm


def login_page(request):
    if request.user.is_authenticated:
        return redirect("feed")

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
            return redirect("feed")
        else:
            messages.error(request, "Invalid password")
            return redirect("login")

    return render(request, "accounts/login.html")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("feed")
        else:
            error_messages = []

            for field_errors in form.errors.as_data().values():
                for error in field_errors:
                    error_messages.extend(error)

            messages.error(request, ". ".join(error_messages))

    else:
        form = MyUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")
