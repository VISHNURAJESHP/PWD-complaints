from django.urls import path
from .views import RegistrationView

urlpatterns = [
    #path('login', LoginView.as_view(), name='login-view'),
    path('register', RegistrationView.as_view(), name='vendor-register'),
]