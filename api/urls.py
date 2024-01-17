# api/urls.py
from django.urls import path
from .views import SignupView, LoginView1

urlpatterns = [
    path('api/v1/signup/', SignupView.as_view(), name='signup'),
   path('api/v1/login/', LoginView1.as_view(), name='login'),
    # path('', ApiInfo.as_view(), name='api_info'),  # Include the info endpoint
]

