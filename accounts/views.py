from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request):
    email = request.POST.get('login_email')
    password = request.POST.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            print('user is active')
            login(request, user)
            return redirect('application.views.new')
        else:
            pass
    else:
        print('user is none')
        pass


def logout_view(request):
    logout(request)
    return redirect('application.views.new')
