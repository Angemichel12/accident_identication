# utils.py
from twilio.rest import Client
from django.conf import settings

def send_sms(message):
    """
    Sends an SMS using Twilio.

    :param to_phone: Recipient's phone number in international format (e.g., +250xxxxxxxxx).
    :param message: Message content to send.
    :return: Response from Twilio API.
    """
    try:
        # Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Send the SMS
        response = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to="+250790005804"
        )
        print("responste", response)
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None
