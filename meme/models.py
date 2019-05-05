from django.db import models


# Create your models here.


class Meme(models.Model):
    # Fields
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now=True)

    # Relationship Fields
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE, related_name="memes",
    )
    file = models.ImageField()

    def __str__(self):
        return self.name
