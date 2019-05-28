from django.urls import path
from . import views

urlpatterns = [
    path('favorite/add/<int:pk>', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:pk>', views.remove_favorite, name='remove_favorite'),
]
