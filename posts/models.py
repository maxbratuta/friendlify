from datetime import datetime
from django.db import models

from friendlify.models import TimestampModel
from accounts.models import User


def image_directory_path(instance, filename):
    return f"posts/{instance.user.username}/{datetime.now().timestamp()}.jpg"


class Post(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)

    image = models.ImageField(upload_to=image_directory_path)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def formatted_created_at(self):
        return self.created_at.strftime('%b %d')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super().delete(*args, **kwargs)
        storage.delete(path)
