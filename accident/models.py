from django.db import models
from cars.models import Car

class Accident(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    impact = models.DecimalField(max_digits=5, decimal_places=2)
    tilt_x = models.CharField(max_length=10)
    tilt_y = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Accident at {self.latitude}, {self.longitude}"
    
class Location(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Location: {self.latitude}, {self.longitude}"
