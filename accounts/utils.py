# accounts/utils.py
import africastalking
import random
import string


def generate_otp(length=4):
    """Generates a random OTP of specified length."""
    characters = string.digits
    otp = ''.join(random.choice(characters) for i in range(length))
    return otp


class SMSService:
    def __init__(self):
        self.username = 'YOUR_USERNAME'
        self.api_key = 'YOUR_API_KEY'
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_otp(self, phone_number, otp):
        message = f"Your OTP code is {otp}"
        try:
            response = self.sms.send(message, [phone_number])
            print(response)
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False
