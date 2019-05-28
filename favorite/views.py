from django.contrib.auth import get_user_model
from django.http import HttpResponse

from favorite.models import FavoriteCollection
from meme.models import Meme

# Create your views here.


def add_favorite(request, pk):
    meme = Meme.objects.all().get(pk=pk)
    user = get_user_model().objects.get(pk=request.user.pk)
    if not user.favorite:
        user.favorite = FavoriteCollection.objects.create()
    user.favorite.memes.add(meme)
    user.save()
    return HttpResponse(200)


def remove_favorite(request, pk):
    user = get_user_model().objects.get(pk=request.user.pk)
    user.favorite.memes.remove(user.favorite.memes.get(pk=pk))
    return HttpResponse(200)
