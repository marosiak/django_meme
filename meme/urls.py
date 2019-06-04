from django.contrib.auth.decorators import login_required
from django.urls import path

from meme.views import AllMemesListView, FavoriteMemesView, RemoveMeme
from . import views

urlpatterns = [
    path('', AllMemesListView.as_view(), name='meme_list'),
    path('favorite/', login_required(FavoriteMemesView.as_view()), name='favorite_list'),
    path('meme/add', login_required(views.add_meme), name='add_meme'),
    path('meme/remove/<int:pk>', login_required(RemoveMeme.as_view()), name='remove_meme'),
]
