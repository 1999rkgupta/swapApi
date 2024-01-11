# api/urls.py
from django.urls import path
from .views import SignupView, LoginView, ApiInfo

urlpatterns = [
    path('v1/signup/', SignupView.as_view(), name='signup'),
    path('v1/login/', LoginView.as_view(), name='login'),
    path('', ApiInfo.as_view(), name='api_info'),  # Include the info endpoint
    # Add other endpoints as needed
]
