from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from friendlify.models import TimestampModel


class User(AbstractUser, TimestampModel):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def delete(self, *args, **kwargs):
        if self.avatar and hasattr(self.avatar, "path") and self.avatar.storage.exists(self.avatar.name):
            storage, path = self.avatar.storage, self.avatar.path
            super().delete(*args, **kwargs)
            storage.delete(path)
        else:
            super().delete(*args, **kwargs)

    @property
    def initials(self):
        return "".join([name[0].upper() for name in [self.first_name, self.last_name] if name])


class FriendshipQuerySet(models.QuerySet):
    def get_friends(self, user: User) -> list[User]:
        return [
            friendship.sender if friendship.receiver == user else friendship.receiver
            for friendship in self
        ]

    def get_dates(self) -> dict[User, datetime]:
        friendship_dates: dict[User, datetime] = {}

        if len(self) > 1:
            for friendship in self:
                if friendship.sender not in friendship_dates:
                    friendship_dates[friendship.sender] = friendship.updated_at

                if friendship.receiver not in friendship_dates:
                    friendship_dates[friendship.receiver] = friendship.updated_at
        else:
            friendship = self.first()

            if friendship:
                friendship_dates[friendship.sender] = friendship.updated_at
                friendship_dates[friendship.receiver] = friendship.updated_at

        return friendship_dates


class Friendship(TimestampModel):
    objects = FriendshipQuerySet.as_manager()

    USER_FRIENDS_LIMIT = 20

    PENDING = 0
    ACCEPTED = 1

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
    ]

    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def accept(self):
        self.status = self.ACCEPTED
        self.save()

    def destroy(self):
        self.delete()

    def is_pending(self) -> bool:
        return self.status == self.PENDING

    def is_accepted(self) -> bool:
        return self.status == self.ACCEPTED

    @classmethod
    def get_friends(cls, user: User) -> list[User]:
        return cls.get_friendships(friend_1=user, status=cls.ACCEPTED).get_friends(user=user)

    @classmethod
    def get_friendships(cls, friend_1: User, friend_2: User = None, status: STATUS_CHOICES = None):
        if friend_2 is None:
            users_query = Q(sender=friend_1) | Q(receiver=friend_1)
        else:
            users_query = Q(sender=friend_1, receiver=friend_2) | Q(sender=friend_2, receiver=friend_1)

        status_query = Q(status=cls.ACCEPTED) | Q(status=cls.PENDING) if status is None else Q(status=status)

        return cls.objects.filter(users_query, status_query)

    @classmethod
    def get_specific_friendship(cls, sender: User, receiver: User, status: STATUS_CHOICES):
        return cls.objects.filter(sender=sender, receiver=receiver, status=status)

    @classmethod
    def is_pending_friendship_exists(cls, sender: User, receiver: User) -> bool:
        return cls.get_specific_friendship(sender=sender, receiver=receiver, status=cls.PENDING).first() is not None

    @classmethod
    def get_pending_friends_as_sender(cls, user: User) -> list[User]:
        return cls.objects.filter(sender=user, status=cls.PENDING).get_friends(user=user)

    @classmethod
    def get_pending_friends_as_receiver(cls, user: User) -> list[User]:
        return cls.objects.filter(receiver=user, status=cls.PENDING).get_friends(user=user)

    @classmethod
    def get_pending_friends_count_as_receiver(cls, user: User) -> int:
        return len(cls.objects.filter(receiver=user, status=cls.PENDING).get_friends(user=user))
