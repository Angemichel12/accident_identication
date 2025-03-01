import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Accident, Location
from cars.models import Car
from .send_sms import send_sms  # Assuming send_sms is defined in send_sms.py

# Configure logging
logger = logging.getLogger(__name__)

@csrf_exempt
def save_location(request):
    """
    Save the last known location of the car.
    If there are already 10 entries in the Location model, delete all entries before saving the new one.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

    try:
        # Parse JSON data from the request
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Validate latitude and longitude
        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Latitude and longitude are required.'}, status=400)

        # Check if there are already 10 entries in the Location model
        if Location.objects.count() >= 10:
            # Delete all existing entries
            Location.objects.all().delete()
            logger.info("Deleted all existing location entries.")

        # Create a new Location instance and save it to the database
        location = Location(latitude=latitude, longitude=longitude)
        location.save()

        logger.info(f"Saved location: Latitude={latitude}, Longitude={longitude}")
        return JsonResponse({'status': 'Location saved successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Error saving location: {str(e)}")
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    

@csrf_exempt
def record_data(request):
    """
    Record accident data and send an SMS notification.
    If GPS data is missing, use the latest entry from the Location table.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

    try:
        # Parse JSON data from the request
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    # Extract fields from the JSON payload
    impact = data.get("impact")
    tilt_x = data.get("tilt_x")
    tilt_y = data.get("tilt_y")
    tilt_z = data.get("tilt_z")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    plate_number = data.get("plate_number")

    # Validate required fields
    required_fields = ["impact", "tilt_x", "tilt_y", "tilt_z", "plate_number"]
    for field in required_fields:
        if field not in data:
            return JsonResponse({"error": f"Missing required field: {field}"}, status=400)

    # Use the latest entry from the Location table if GPS data is not available
    if latitude is None or longitude is None:
        try:
            # Get the latest Location entry
            latest_location = Location.objects.latest('created_at')
            latitude = latest_location.latitude
            longitude = latest_location.longitude
            logger.info(f"Using latest location from database: Latitude={latitude}, Longitude={longitude}")
        except ObjectDoesNotExist:
            logger.warning("No GPS data available, and no location entries found in the database.")
            return JsonResponse({"error": "No GPS data available, and no location entries found."}, status=400)

    # Log the received data
    logger.info(f"Impact: {impact} m/s²")
    logger.info(f"Tilt: X={tilt_x}° Y={tilt_y}° Z={tilt_z}°")
    logger.info(f"Plate Number: {plate_number}")
    if latitude is not None and longitude is not None:
        logger.info(f"Location: Latitude={latitude}, Longitude={longitude}")
    else:
        logger.warning("Location: GPS data not available")

    try:
        # Fetch the car object
        car = Car.objects.get(plate_number=plate_number)
    except ObjectDoesNotExist:
        logger.error(f"Car with plate number {plate_number} not found")
        return JsonResponse({"error": f"Car with plate number {plate_number} not found."}, status=404)
    except Exception as e:
        logger.error(f"Error fetching car: {str(e)}")
        return JsonResponse({"error": "Internal server error while fetching car details."}, status=500)

    try:
        # Create an accident record
        accident = Accident.objects.create(
            impact=impact,
            tilt_x=tilt_x,
            tilt_y=tilt_y,
            latitude=latitude,
            longitude=longitude,
            car=car
        )
        logger.info(f"Accident recorded: {accident}")

        # Send SMS notification
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
        logger.error(f"Error creating accident record: {str(e)}")
        return JsonResponse({"error": "Internal server error while saving accident data."}, status=500)