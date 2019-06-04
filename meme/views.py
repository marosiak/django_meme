from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, RedirectView

from favorite.models import FavoriteCollection
from .models import Meme


class MemeListView(ListView):
    template_name = 'meme/meme_list.html'
    model = Meme
    context_object_name = 'memes'

    def _get_memes(self):
        memes = Meme.objects.all()
        user = self.request.user
        if user.is_authenticated:
            if not user.favorite:
                user.favorite = FavoriteCollection.objects.create()
                user.save()
        memes.order_by('-publish_date')
        return memes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_stuff'] = self.request.user.is_staff
        return context


class AllMemesListView(MemeListView):
    def get_queryset(self):
        user = self.request.user
        memes = self._get_memes()
        if user.is_authenticated:
            for meme in memes:
                user_faviorites = user.favorite.memes.all()
                for fav in user_faviorites:
                    if fav == meme:
                        meme.is_favorite = True
        return memes


class FavoriteMemesView(MemeListView):
    def get_queryset(self):
        user = self.request.user
        if not user.favorite:
            user.favorite = FavoriteCollection.objects.create()
            user.save()
        fav = user.favorite.memes.all()
        fav.order_by('-publish_date')
        return fav

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_view'] = True
        return context


class RemoveMeme(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'meme_list'

    def get_redirect_url(self, *args, **kwargs):
        meme = get_object_or_404(Meme, pk=kwargs.pop('pk'))
        meme.delete()
        return super().get_redirect_url(*args, **kwargs)


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
