
from django.urls import path
from .views import SignUpView, LoginView, UpdateUserView, DeleteUserView, DefaultAPIView

urlpatterns = [
    path('', DefaultAPIView.as_view(), name='default-api'),
    path('api/v1/signup/', SignUpView.as_view(), name='signup'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/update_user', UpdateUserView.as_view(), name='update-user'),
    path('api/v1/delete_user', DeleteUserView.as_view(), name='delete-user'),
    # Add other URLs as needed
]
