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

    def formatted_created_at(self):
        return self.created_at.strftime('%b %d')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super().delete(*args, **kwargs)
        storage.delete(path)
