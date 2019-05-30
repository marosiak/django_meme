from django.conf import settings
from django.db import models


# Create your models here.


class Meme(models.Model):
    # Fields
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now=True)

    # Relationship Fields
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memes",
    )
    file = models.ImageField(upload_to='memes/%Y%m%d')


    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
