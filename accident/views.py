from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Accident
from cars.models import Car
from .send_sms import send_sms

# Global variable to store the last known location
last_known_location = {"latitude": None, "longitude": None}

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # Save the last known location
            global last_known_location
            last_known_location["latitude"] = latitude
            last_known_location["longitude"] = longitude

            print(f"Saved location: Latitude={latitude}, Longitude={longitude}")
            return JsonResponse({'status': 'Location saved successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def record_data(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            
            # Extract fields from the JSON payload
            impact = data.get("impact")
            tilt_x = data.get("tilt_x")
            tilt_y = data.get("tilt_y")
            tilt_z = data.get("tilt_z")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            plate_number = data.get("plate_number")

            # Use last known location if GPS data is not available
            global last_known_location
            if latitude is None or longitude is None:
                latitude = last_known_location["latitude"]
                longitude = last_known_location["longitude"]

            # Log or process the received data
            print(f"Impact: {impact} m/s²")
            print(f"Tilt: X={tilt_x}° Y={tilt_y}° Z={tilt_z}°")
            print(f"Location: Latitude={latitude}, Longitude={longitude}")
            print(f"Plate Number: {plate_number}")

            # Check if the car exists
            try:
                car = Car.objects.get(plate_number=plate_number)
            except Car.DoesNotExist:
                print(f"Car with plate number {plate_number} not found")
                send_sms(f"Accident detected! Unknown car with plate number: {plate_number}. Location: https://maps.google.com/?q={latitude},{longitude}")
                return JsonResponse({"error": "Car not found"}, status=404)

            # Get driver information
            driver = car.driver if hasattr(car, 'driver') else "Unknown driver"

            # Record the accident
            accident = Accident.objects.create(
                impact=impact,
                tilt_x=tilt_x,
                tilt_y=tilt_y,
                tilt_z=tilt_z,
                latitude=latitude,
                longitude=longitude,
                car=car
            )
            
            # Send SMS notification
            message = (
                f"Accident detected! Plate: {plate_number}, Driver: {driver}. "
                f"Location: https://maps.google.com/?q={latitude},{longitude}"
            )
            send_sms(message)

            print(f"Accident recorded: {accident}")
            return JsonResponse({"message": "Accident recorded successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    
    # Return error for unsupported methods
    return JsonResponse({"error": "Invalid request method"}, status=405)
