from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from authentication.models import User


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Wrong email')
        user = authenticate(username=email, password=password)
        if user is not None:
            messages.success(request, 'Logged in as ' + user.email)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')
    return render(request, 'login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('auth:login')
    return redirect('home')