from django.urls import path    
from . import views

urlpatterns = [
    path('save-location/', views.save_location, name='save_location'),
    path('api/record_data/', views.record_data, name='record_data'),
]