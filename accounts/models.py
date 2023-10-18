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

    def delete(self, *args, **kwargs):
        if self.avatar and hasattr(self.avatar, 'path') and self.avatar.storage.exists(self.avatar.name):
            storage, path = self.avatar.storage, self.avatar.path
            super().delete(*args, **kwargs)
            storage.delete(path)
        else:
            super().delete(*args, **kwargs)

    @property
    def initials(self):
        return ''.join([name[0].upper() for name in [self.first_name, self.last_name] if name])

# class Friendship(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
