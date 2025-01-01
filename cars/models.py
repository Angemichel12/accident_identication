from django.db import models

class Car(models.Model):
    plate_number = models.CharField(max_length=8)
    driver_name = models.CharField(max_length=50)
    driver_phone_number = models.CharField(max_length=15, null=True, blank=True)
    chassis_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.plate_number} {self.driver_name}"
