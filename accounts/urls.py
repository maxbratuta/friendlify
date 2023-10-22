from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),


    path("users/<str:username>/", views.show, name="users.show"),
    path('users/<str:username>/edit', views.edit, name="users.edit"),
    path('users/destroy', views.destroy, name="users.destroy"),

    path('friendship/send/<int:receiver_id>/', views.send_friend_request, name="friendship.send_request"),
    path('friendship/accept/<int:request_id>/', views.accept_friend_request, name="friendship.accept_request"),
    path('friendship/decline/<int:request_id>/', views.decline_friend_request, name="friendship.decline_request"),
]
