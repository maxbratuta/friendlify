from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.templatetags.static import static

from posts.models import Post


@login_required(login_url='login')
def feed(request):
    # posts = Post.objects.all()


    # names = value.split()
    # initials = [name[0].upper() for name in names]
    # return ''.join(initials)

    friends_list = [
        {
            'id': 1,
            'full_name': 'Ola Hombre',
            'initials': 'OH',
            'avatar': None,
        },
        {
            'id': 2,
            'full_name': 'Paulina Sombrero',
            'initials': 'PS',
            'avatar': None
        },
        {
            'id': 3,
            'full_name': 'Hose Horse',
            'initials': 'HH',
            'avatar': None
        }
    ]

    conversations = [
        {
            'id': 200001,
            'friend': {
                'id': 1,
                'full_name': 'Ola Hombre',
                'initials': 'OH',
                'avatar': None
            },
            'last_message': 'Gorgeous!',
        },
        {
            'id': 200002,
            'friend': {
                'id': 2,
                'full_name': 'Paulina Sombrero',
                'initials': 'PS',
                'avatar': None
            },
            'last_message': 'Hola!',
        },
        {
            'id': 200003,
            'friend': {
                'id': 3,
                'full_name': 'Hose Horse',
                'initials': 'HH',
                'avatar': None
            },
            'last_message': 'Muy bien :)',
        },
    ]

    posts = [
        {
            'id': 100002,
            'user': {
                'id': 2,
                'full_name': 'Paulina Sombrero',
                'initials': 'PS',
                'avatar': None
            },
            'image_url': static('images/posts/post-image-1.jpg'),
            'description': 'El Camino de mi Almo',
            'created_at': '2 Oct',
        },
        {
            'id': 100001,
            'user': {
                'id': 1,
                'full_name': 'Ola Hombre',
                'initials': 'OH',
                'avatar': None,
            },
            'image_url': static('images/posts/post-image-2.jpg'),
            'description': 'Windy Day!',
            'created_at': '1 Oct',
        }
    ]

    # topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    # room_messages = Message.objects.filter(
    #     Q(room__topic__name__icontains=q))[0:3]

    # context = {'rooms': rooms, 'topics': topics,
    #            'room_count': room_count, 'room_messages': room_messages}

    return render(request, "posts/index.html", {
        "posts": posts,
        "conversations": conversations,
        "friends_list": friends_list,
        "auth": {
            "user": {
                "id": request.user.id,
                "full_name": request.user.get_full_name(),
                "initials": "AD",
                "avatar": request.user.avatar,
            }
        }
    })
