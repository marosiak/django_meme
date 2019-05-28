from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, Q, BooleanField
from django.shortcuts import render, redirect

from .models import Meme


# Create your views here.
def meme_list(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    memes = Meme.objects.all()
    memes.order_by('-publish_date')

    user_faviorites = user.favorite.memes.all()
    memes = (Meme.objects.all().
        annotate(
        is_favorite=Case(
            When(condition=Q(pk__in=user_faviorites), then=Value(True)), default=Value(False),
            output_field=BooleanField())
    ))

    return render(request, 'meme/meme_list.html', {'memes': memes, 'is_stuff': request.user.is_staff})


def remove_meme(request, pk):
    if request.user.is_staff:
        meme = Meme.objects.filter(pk=pk)
        meme.delete()
    return redirect('meme_list')


@login_required
def add_meme(request):
    if request.POST:
        img = request.FILES.get('image', False)
        title = request.POST.get('title', False)
        if title:
            if len(title) >= 30:
                return render(request, 'meme/meme_add.html', {'error': 'The title is too long'})
            if img:
                Meme.objects.create(file=img, title=title, author=request.user)
                return redirect('meme_list')
            else:
                return render(request, 'meme/meme_add.html', {'error': 'Please select file'})
        else:
            return render(request, 'meme/meme_add.html', {'error': 'Please enter title'})

    return render(request, 'meme/meme_add.html')
