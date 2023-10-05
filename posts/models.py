from django.db import models

from friendlify.models import TimestampModel
from accounts.models import User


class Post(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="posts/")
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
