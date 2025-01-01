from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html')

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")