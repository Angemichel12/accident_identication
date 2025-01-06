from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


User = get_user_model()


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('dashboard')
        else:
            messages.error('Wrong Credentials!')
            return render(request, 'users/login.html')
    messages.error(request, "Wrong Credentials")
    return render(request, "users/login.html")
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("home")
@login_required
def register_user_view(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        print("firstname", firstname)
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print("username",username)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Password and confirm password must match.')
            return redirect('users_dashboard')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('users_dashboard')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('users_dashboard')

        try:
            user = User.objects.create(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=username,
                password=make_password(password))
            messages.success(request, f'{user.first_name} has been successfully created!')
            return redirect('users_dashboard')
        except Exception as e:
            
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('users_dashboard')

    return redirect('users_dashboard')
@login_required
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        
        user.first_name = request.POST.get("firstname")
        user.last_name = request.POST.get("lastname")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        password = request.POST.get("password")
        
        
        if password:
            user.set_password(make_password(password))
            
        try:
            user.save()
            messages.success(request,"User updated Successfully!")
        except Exception as e:
            messages.error(request, f"Something went wrong {e}")
            return redirect('users_dashboard')
        return redirect("users_dashboard")

@login_required   
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        user.delete()
        messages.success(request, "Delete user Successfully!")
    except Exception as e:
        messages.error(request, "Error: ", e)
        return redirect('users_dashboard')
    return redirect('users_dashboard')
