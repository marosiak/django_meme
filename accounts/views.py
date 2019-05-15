from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def sign_up(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if username and password and password_confirm:
            if password == password_confirm:
                if len(password) < 6:
                    return render(request, 'registration/sign_up.html', {'error': 'Password must be atleast 6 characters length'})
                if len(username) < 4:
                    return render(request, 'registration/sign_up.html', {'error': 'Username must be atleast 4 characters length'})
                if User.objects.filter(username=username).exists():
                    return render(request, 'registration/sign_up.html', {'error': 'This user already exists'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect("meme_list")
                    else:
                        return render(request, 'registration/sign_up.html', {'error': 'There was weird problem :/'})
            else:
                return render(request, 'registration/sign_up.html', {'error': 'Passwords doesn\'t match'})
        return render(request, 'registration/sign_up.html', {'error': 'Please enter correct values'})
    return render(request, 'registration/sign_up.html')
