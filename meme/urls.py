from django.urls import path
from . import views

urlpatterns = [
    path('', views.meme_list, name='meme_list'),
    path('meme/add', views.add_meme, name='add_meme'),
    path('meme/remove/<int:pk>', views.remove_meme, name='remove_meme'), 
]
