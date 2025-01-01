from django.shortcuts import render
from cars.models import Car

def home (request):
    return render(request, 'index.html')

def dashboard_page (request):
    return render(request, 'dashboard/dashboard.html')
def accidents_page(request):
    return render(request, 'dashboard/accidents_dashboard.html')

def cars_page (request):
    cars = Car.objects.all()
    context = {
        'cars':cars,
    }
    return render(request, 'dashboard/cars_dashboard.html', context)

def users_page(request):
    return render(request, 'dashboard/users_dashboard.html')