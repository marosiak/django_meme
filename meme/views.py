from django.shortcuts import render, redirect
from .models import Meme
from django.contrib.auth.decorators import login_required


# Create your views here.
def meme_list(request):
    memes = Meme.objects.all().order_by('-publish_date')
    return render(request, 'meme/meme_list.html', {'memes': memes})


@login_required
def add_meme(request):
    if request.POST:
        img = request.FILES.get('image', False)
        title = request.POST.get('title', False)
        if title:
            if img:
                Meme.objects.create(file=img, title=title, author=request.user)
                return redirect('meme_list')
            else:
                return render(request, 'meme/meme_add.html', {'error': 'Please select file'})
        else:
            return render(request, 'meme/meme_add.html', {'error': 'Please enter title'})

    return render(request, 'meme/meme_add.html')
