
from django.urls import path
from .views import register, LoginView, edit_profile, delete_user, DefaultAPIView, get_solo_user,search

urlpatterns = [
    path('', DefaultAPIView.as_view(), name='default-api'),
    path('api/v1/search/', search, name='search'),
    path('api/v1/signup', register, name='signup'),
    path('api/v1/login', LoginView, name='login'),
    path('api/v1/get_user', get_solo_user, name='get-authenticated-user'),
    # path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view()),
    path('api/v1/update_user', edit_profile, name='update-user'),
    path('api/v1/delete_user', delete_user, name='delete-user'),
    # path('api/v1/get_user', GetUserView.as_view(), name='get-user'),
]
