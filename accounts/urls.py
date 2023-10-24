from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),

    path("users/search/", views.user_search, name="users.search"),

    path("users/<str:username>/", views.user_show, name="users.show"),
    path("users/<str:username>/edit/", views.user_edit, name="users.edit"),
    path("users/destroy/", views.user_destroy, name="users.destroy"),

    path("friendships/", views.friendship_index, name="friendships.index"),
    path("friendships/<str:username>/send/", views.send_friend_request, name="friendships.send_request"),
    path("friendships/<str:username>/accept/", views.accept_friend_request, name="friendships.accept_request"),
    path("friendships/<str:username>/destroy/", views.friendship_destroy, name="friendships.destroy"),
]
