from django.urls import path
from .views import (home, 
                dashboard_page,
                cars_page, 
                users_page,
                accidents_page
                )

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard_page, name="dashboard"),
    path('accidents/', accidents_page, name="accidents_dashboard"),
    path('cars/', cars_page, name="cars_dashboard"),
    path('users/', users_page, name="users_dashboard"),
]