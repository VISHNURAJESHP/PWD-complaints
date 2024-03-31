from django.urls import path
from .views import OfficialRegistrationView , UserRegistrationView

urlpatterns = [
    #path('login', LoginView.as_view(), name='login-view'),
    path('officialregister', OfficialRegistrationView.as_view(), name='official-register'),
    path('userregister', UserRegistrationView.as_view(), name='official-register'),
]