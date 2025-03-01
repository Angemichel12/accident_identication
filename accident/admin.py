from django.contrib import admin
from .models import Accident, Location

admin.site.register([Accident, Location])
