from django.urls import path
from .views import create_car_view,edit_car, delete_car

urlpatterns = [
    path("add/",create_car_view, name='register_car'),
    path('edit/', edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', delete_car, name='delete_car'),
]