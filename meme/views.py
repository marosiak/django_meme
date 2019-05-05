from django.shortcuts import render, redirect
from .models import Meme


# Create your views here.
def meme_list(request):
    memes = Meme.objects.all()
    return render(request, 'meme/meme_list.html', {'memes': memes})


def add_meme(request):
    if request.user.is_authenticated:
        if request.POST:
            img = request.FILES.get('image', False)
            if img:
                Meme.objects.create(file=img, title=request.POST.get("title", ""), author=request.user)
                return redirect('meme_list')
        return render(request, 'meme/meme_add.html')
    else:
        return redirect('login')
