from django.urls import path
from .views import OfficialRegistrationView , UserRegistrationView, OTPVerificationView, LoginView

urlpatterns = [
    path('officialregister', OfficialRegistrationView.as_view(), name='official-register'),
    path('userregister', UserRegistrationView.as_view({'post': 'user_registration'}), name='official-register'),
    path('login', LoginView.as_view(), name='login-view'),
    path('verify-email', OTPVerificationView.as_view(), name='otp_verification_view'),
]