from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, Q, BooleanField
from django.shortcuts import render, redirect

from favorite.models import FavoriteCollection
from .models import Meme


# Create your views here.
def meme_list(request):
    memes = Meme.objects.all()
    memes.order_by('-publish_date')
    if request.user.is_authenticated:
        user = get_user_model().objects.get(pk=request.user.pk)
        if not user.favorite:
            user.favorite = FavoriteCollection.objects.create()
            user.save()
        user_faviorites = user.favorite.memes.all()
        memes = (Meme.objects.all().
            annotate(
            is_favorite=Case(
                When(condition=Q(pk__in=user_faviorites), then=Value(True)), default=Value(False),
                output_field=BooleanField())
        ))

    return render(request, 'meme/meme_list.html', {'memes': memes, 'is_stuff': request.user.is_staff})


# yes, I'm copying this shit from above, I'll make ListView class in future, but rn I got no time..
@login_required
def favorite_list(request):
    user = get_user_model().objects.get(pk=request.user.pk)

    user_faviorites = user.favorite.memes.all()
    user_faviorites.order_by('-publish_date')

    return render(request, 'meme/meme_list.html',
                  {'memes': user_faviorites, 'is_stuff': request.user.is_staff, 'favorite_view': True})


def remove_meme(request, pk):
    if request.user.is_staff:
        meme = Meme.objects.filter(pk=pk)
        meme.delete()
    return redirect('meme_list')


@login_required
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
