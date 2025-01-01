from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Car

@login_required
def create_car_view(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        driver_name = request.POST.get('driver_name')
        driver_phone_number = request.POST.get('driver_phone_number')
        chassis_number = request.POST.get('chassis_number')

        if not plate_number or not driver_name or not driver_phone_number:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'dashboard/cars_dashboard.html')

        Car.objects.create(
            plate_number=plate_number,
            driver_name=driver_name,
            driver_phone_number=driver_phone_number,
            chassis_number=chassis_number
        )
        messages.success(request, "Car registered successfully.")
        return redirect('cars_dashboard')

    return render(request, 'dashboard/cars_dashboard.html')

@login_required
def edit_car(request):
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        car = get_object_or_404(Car, id=car_id)
        
        car.plate_number = request.POST.get("plate_number")
        car.driver_name = request.POST.get("driver_name")
        car.chassis_number = request.POST.get("chassis_number")
        car.driver_phone_number = request.POST.get("driver_phone_number")
        car.save()
        
        return redirect("cars_dashboard")
    
@login_required   
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, "Car deleted successfully.")
    return redirect("cars_dashboard")