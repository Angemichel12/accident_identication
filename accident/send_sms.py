import africastalking

username = "sandbox"  # Your Africa's Talking username
api_key = "atsk_708328d111f0e8fcc9153fd82bc9f25094dbaa111570fcceba2b9bd54a136fc2e9dfa80a"    # Your Africa's Talking API key
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms():
    response = sms.send(
        message="Hello, this is a test SMS!",
        recipients=["+250783327944"],  # Any phone number
    )
    print(response)