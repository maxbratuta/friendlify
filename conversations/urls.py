from django.urls import path
from . import views

urlpatterns = [
    path("conversations/<int:id>/", views.conversation_page, name="conversation"),
]
