from django.db import models
from django.db.models import ManyToManyField, OneToOneField
from django.contrib.auth.models import AbstractUser
from meme.models import Meme


class FavoriteCollection(models.Model):
    memes = ManyToManyField(Meme)


class UserExtension(AbstractUser):
    favorite = OneToOneField(FavoriteCollection, on_delete=models.CASCADE, null=True)
