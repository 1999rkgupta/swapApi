
from django.urls import path
from .views import LoginAPI, SignupAPI, UpdateAPI, DeleteAPI, GetUserAPI, DefaultAPIView

urlpatterns = [
    path('', DefaultAPIView.as_view(), name='default-api'),
    path('api/v1/signup', SignupAPI.as_view(), name='signup'),
    path('api/v1/login', LoginAPI.as_view(), name='login'),
    path('api/v1/update_user', UpdateAPI.as_view(), name='update-user'),
    path('api/v1/delete_user', DeleteAPI.as_view(), name='delete-user'),
    path('api/v1/get_user', GetUserAPI.as_view(), name='get-user'),
]
