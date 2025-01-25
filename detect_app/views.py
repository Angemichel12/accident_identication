from django.shortcuts import render
from cars.models import Car
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accident.models import Accident
from django.db.models.functions import TruncMonth
from django.db.models import Count

User = get_user_model()

def home (request):
    return render(request, 'index.html')
@login_required
def dashboard_page (request):
       # Accidents by month
    accidents_by_month = (
        Accident.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    accident_data = {
        "labels": [a["month"].strftime("%b %Y") for a in accidents_by_month],
        "data": [a["count"] for a in accidents_by_month],
    }

    # Cars registered by month
    cars_by_month = (
        Car.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    car_data = {
        "labels": [c["month"].strftime("%b %Y") for c in cars_by_month],
        "data": [c["count"] for c in cars_by_month],
    }
    total_accidents = Accident.objects.count()
    total_cars = Car.objects.count()
    total_users = User.objects.filter(is_staff=False).count()

    context = {
        "accident_data": accident_data,
        "car_data": car_data,
        "total_accidents": total_accidents,
        "total_cars": total_cars,
        "total_users": total_users,
    }
 
    return render(request, 'dashboard/dashboard.html', context)
@login_required
def accidents_page(request):
    accidents = Accident.objects.all()
    total_accidents = Accident.objects.count()
    total_cars = Car.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    context = {
        'accidents':accidents,
        'total_accidents':total_accidents,
        'total_cars':total_cars,
        'total_users':total_users,}
    return render(request, 'dashboard/accidents_dashboard.html', context)
@login_required
def cars_page (request):
    cars = Car.objects.all()
    total_accidents = Accident.objects.count()
    total_cars = Car.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    context = {
        'cars':cars,
        'total_accidents':total_accidents,
        'total_cars':total_cars,
        'total_users':total_users,
    }
    return render(request, 'dashboard/cars_dashboard.html', context)
@login_required
def users_page(request):
    users = User.objects.filter(is_staff=False)
    total_accidents = Accident.objects.count()
    total_cars = Car.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    context = {
        'users':users,
        'total_accidents':total_accidents,
        'total_cars':total_cars,
        'total_users':total_users,

    }
    return render(request, 'dashboard/users_dashboard.html', context)