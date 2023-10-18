from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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

    # topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    # room_messages = Message.objects.filter(
    #     Q(room__topic__name__icontains=q))[0:3]

    # context = {'rooms': rooms, 'topics': topics,
    #            'room_count': room_count, 'room_messages': room_messages}

    return render(request, "posts/feed.html", {
        "posts": posts,
        "conversations": conversations,
        "friends_list": friends_list,
    })


@login_required(login_url="login")
def gallery(request):
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

    # topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    # room_messages = Message.objects.filter(
    #     Q(room__topic__name__icontains=q))[0:3]

    # context = {'rooms': rooms, 'topics': topics,
    #            'room_count': room_count, 'room_messages': room_messages}

    return render(request, "posts/gallery.html", {
        "posts": posts,
        "conversations": conversations,
        "friends_list": friends_list
    })
