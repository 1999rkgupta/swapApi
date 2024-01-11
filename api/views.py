# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

      # Original plaintext password
        plain_password = "1234"

        hashed_password_django = make_password(plain_password, hasher='pbkdf2_sha256')

# Manually provided hashed password
        hashed_password_provided = "pbkdf2_sha256$260000$KwXrv63XakQVAouiQfCu92$UoRAALfo6z6STL0b6GfNiPH4Ptyz6uRlFl8cfjSEQGc="

# Check if the two hashed passwords match
        password_matches = check_password(hashed_password_django, plain_password)

        if password_matches:
          print("Password is correct!")
        else:
          print("Password is incorrect.")

        # Use Django's authenticate function
        user = authenticate(request, email=email, password=password)

        if user:
            # If authentication is successful, generate or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'email': user.email, 'mobile': user.mobile, 'city': user.city})
        else:
            # If authentication fails, return an error response
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ApiInfo(APIView):
    def get(self, request):
        info = {
            "version": "v1",
            "endpoints": {
                "signup": "/api/v1/signup/",
                "login": "/api/v1/login/",
                # Add other endpoints as needed
            }
        }
        return Response(info)
