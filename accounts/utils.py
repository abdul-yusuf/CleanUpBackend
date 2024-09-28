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
        self.username = 'sandbox'
        self.api_key = 'atsk_4396aff20f77073773d344d96f7b9feba2fa6bfcdf8f6270535dd81718a883b9420335cf'
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_otp(self, phone_number, otp):
        message = f"Your OTP code is {otp}"
        print(phone_number, message)
        try:
            response = self.sms.send(message, [phone_number], '3235')
            print(response)
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False
