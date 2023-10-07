from django.contrib.auth.models import AbstractUser
from django.db import models

from friendlify.models import TimestampModel


class User(AbstractUser, TimestampModel):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

# class Friendship(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
