from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request):
    email = request.POST.get('login_email')
    password = request.POST.get('password')
    print(email, password)
    user = authenticate(username=email, password=password)
    if user:
        if user.is_active:
            login(request, user)
            if user.is_staff:
                return redirect('admin:index')
            else:
                return redirect('application.views.show')
        else:
            pass
    else:
        return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('application.views.new')
