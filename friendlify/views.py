from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect("feed")

    return render(request, "friendlify/index.html")
