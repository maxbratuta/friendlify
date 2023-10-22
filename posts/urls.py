from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.index, name="posts.index"),
    path('posts/', views.store, name="posts.store"),
    path('posts/<int:id>/delete', views.destroy, name="posts.destroy"),
]
