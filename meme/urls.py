from django.contrib.auth.decorators import login_required
from django.urls import path

from meme.views import AllMemesListView, FavoriteMemesView
from . import views

urlpatterns = [
    # path('', views.meme_list, name='meme_list'),
    # path('favorite/', views.favorite_list, name='favorite_list'),
    path('', AllMemesListView.as_view(), name='meme_list'),
    path('favorite/', login_required(FavoriteMemesView.as_view()), name='favorite_list'),
    path('meme/add', login_required(views.add_meme), name='add_meme'),
    path('meme/remove/<int:pk>', views.remove_meme, name='remove_meme'),
]
