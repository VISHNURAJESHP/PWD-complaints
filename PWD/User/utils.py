import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode


def generate_otp(length=6):
    """Generate a random OTP code of specified length."""
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp


def send_otp_email(to_email, otp_code, user_name):

    verification_link = generate_verification_link(to_email, otp_code)
    subject = "Verify Your Email"
    message = f"Hi {user_name},\n\nPlease verify your email by clicking the following link:\n{verification_link}"
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [to_email])
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def generate_verification_link(to_email, otp_code):
    base_url = settings.BACKEND_URL  
    verification_path = reverse('otp_verification_view')
    query_string = urlencode({'otp': otp_code, 'email': to_email})
    return f"{base_url}{verification_path}?{query_string}"