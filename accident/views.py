from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Accident
from cars.models import Car
from .send_sms import send_sms
from django.core.exceptions import ObjectDoesNotExist

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
            print(f"Location: Latitude--={latitude}, Longitude--={longitude}")
            print(f"Plate Number: {plate_number}")
            if latitude is not None and longitude is not None:
                print(f"Location: Latitude={latitude}, Longitude={longitude}")
            else:
                print("Location: GPS data not available")

            try:
                # Fetch the car object
                car = Car.objects.get(plate_number=plate_number)
            except ObjectDoesNotExist:
                print(f"Car with plate number {plate_number} not found")
                return JsonResponse({"error": f"Car with plate number {plate_number} not found."}, status=404)
            except Exception as e:
                print(f"Error: {str(e)}")
                return JsonResponse({"error": "Internal server error while fetching car details."}, status=500)

            try:
                # Create an accident record
                accident = Accident.objects.create(
                    impact=impact,
                    tilt_x=tilt_x,
                    tilt_y=tilt_y,
                    tilt_z=tilt_z,
                    latitude=latitude,
                    longitude=longitude,
                    car=car
                )
                print(f"Accident recorded: {accident}")

                # Send SMS notification only if data is saved successfully
                if latitude and longitude:
                    send_sms(
                        f"Accident detected! Car with plate number: {plate_number}. "
                        f"Location: https://maps.google.com/?q={latitude},{longitude}"
                    )
                else:
                    send_sms(
                        f"Accident detected! Car with plate number: {plate_number}. "
                        "Location data not available."
                    )

                return JsonResponse({"message": "Data received and saved successfully!"})
            except Exception as e:
                print(f"Error: {str(e)}")
                return JsonResponse({"error": "Internal server error while saving accident data."}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    
    # Return error for unsupported methods
    return JsonResponse({"error": "Invalid request method"}, status=405)
