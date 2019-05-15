from django.shortcuts import render, redirect
from .models import Meme
from django.contrib.auth.decorators import login_required


# Create your views here.
def meme_list(request):
    memes = Meme.objects.all()
    return render(request, 'meme/meme_list.html', {'memes': memes})


@login_required
def add_meme(request):
    if request.POST:
        img = request.FILES.get('image', False)
        if img:
            Meme.objects.create(file=img, title=request.POST.get("title", ""), author=request.user)
            return redirect('meme_list')
    return render(request, 'meme/meme_add.html')
