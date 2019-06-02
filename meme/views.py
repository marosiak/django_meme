from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import ListView

from favorite.models import FavoriteCollection
from .models import Meme


class MemeListView(ListView):
    template_name = 'meme/meme_list.html'
    model = Meme
    context_object_name = 'memes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_stuff'] = self.request.user.is_staff
        return context


class AllMemesListView(MemeListView):
    def get_queryset(self):
        memes = Meme.objects.all()
        if self.request.user.is_authenticated:
            for meme in memes:
                user = get_user_model().objects.get(pk=self.request.user.pk)
                if not user.favorite:
                    user.favorite = FavoriteCollection.objects.create()
                    user.save()
                user_faviorites = user.favorite.memes.all()
                for fav in user_faviorites:
                    if fav == meme:
                        meme.is_favorite = True
        return memes


class FavoriteMemesView(MemeListView):
    def get_queryset(self):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        if not user.favorite:
            user.favorite = FavoriteCollection.objects.create()
            user.save()
        return user.favorite.memes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_view'] = True
        return context


def remove_meme(request, pk):
    if request.user.is_staff:
        meme = Meme.objects.filter(pk=pk)
        meme.delete()
    return redirect('meme_list')


def add_meme(request):
    allowed_content_types = ['image/jpeg', 'image/png']
    if request.POST:
        img = request.FILES.get('image', False)
        title = request.POST.get('title', False)
        if title:
            if len(title) >= 30:
                return render(request, 'meme/meme_add.html', {'error': 'The title is too long'})
            if img:
                if img.content_type in allowed_content_types:
                    Meme.objects.create(file=img, title=title, author=request.user)
                    return redirect('meme_list')
                else:
                    return render(request, 'meme/meme_add.html', {'error': 'Wrong file format, please upload png/jpeg'})
            else:
                return render(request, 'meme/meme_add.html', {'error': 'Please select file'})
        else:
            return render(request, 'meme/meme_add.html', {'error': 'Please enter title'})

    return render(request, 'meme/meme_add.html')
