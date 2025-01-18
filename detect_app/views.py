from django.shortcuts import render
from cars.models import Car
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accident.models import Accident

User = get_user_model()

def home (request):
    return render(request, 'index.html')
@login_required
def dashboard_page (request):
 
    return render(request, 'dashboard/dashboard.html',)
@login_required
def accidents_page(request):
    accidents = Accident.objects.all()
    context = {
        'accidents':accidents,}
    return render(request, 'dashboard/accidents_dashboard.html', context)
@login_required
def cars_page (request):
    cars = Car.objects.all()
    context = {
        'cars':cars,
    }
    return render(request, 'dashboard/cars_dashboard.html', context)
@login_required
def users_page(request):
    users = User.objects.filter(is_staff=False)
    context = {
        'users':users,
    }
    return render(request, 'dashboard/users_dashboard.html', context)