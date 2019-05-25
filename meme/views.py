from django.shortcuts import render, redirect
from .models import Meme
from django.contrib.auth.decorators import login_required

# Create your views here.
def meme_list(request):
    memes = Meme.objects.all().order_by('-publish_date')
    if request.user.is_staff:
        return render(request, 'meme/meme_list.html', {'memes': memes, 'is_stuff': True})
    else:
        return render(request, 'meme/meme_list.html', {'memes': memes})


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
            if len(title) >= 15:
                return render(request, 'meme/meme_add.html', {'error': 'The title is too long'})
            if img:
                Meme.objects.create(file=img, title=title, author=request.user)
                return redirect('meme_list')
            else:
                return render(request, 'meme/meme_add.html', {'error': 'Please select file'})
        else:
            return render(request, 'meme/meme_add.html', {'error': 'Please enter title'})

    return render(request, 'meme/meme_add.html')
