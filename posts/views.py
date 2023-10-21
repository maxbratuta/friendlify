from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from posts.models import Post


@login_required(login_url="login")
def feed(request):
    # posts = Post.objects.all()


    # names = value.split()
    # initials = [name[0].upper() for name in names]
    # return ''.join(initials)

    friends_list = [
        User.objects.filter(username="ola_hombre").get(),
        User.objects.filter(username="paulina_sombrero").get(),
        User.objects.filter(username="hose_horse").get(),
    ]

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

    posts = [
        Post.objects.get(user__username="paulina_sombrero"),
        Post.objects.get(user__username="ola_hombre"),
    ]

    posts = Post.objects.all()

    # topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    # room_messages = Message.objects.filter(
    #     Q(room__topic__name__icontains=q))[0:3]

    # context = {'rooms': rooms, 'topics': topics,
    #            'room_count': room_count, 'room_messages': room_messages}

    return render(request, "posts/feed.html", {
        "posts": posts,
        "conversations": conversations,
        "friends": friends_list,
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
        post = get_object_or_404(Post, id=id)

        if request.user != post.user:
            return HttpResponse("You do not have permission to perform this action.", status=403)

        post.delete()

        messages.success(request, "Post has been deleted!")

    return redirect("posts.index")
