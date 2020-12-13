from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to = 'users_avatar', blank = True),
    age = models.PositiveIntegerField(blank = True, null = True)

    def __str__(self):
        return self.username
