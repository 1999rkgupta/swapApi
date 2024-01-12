from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import User
from .serializers import UserSerializer, EmailPasswordSerializer
import logging
from knox.views import LoginView as KnoxLoginView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView  
from knox.auth import TokenAuthentication
from rest_framework.serializers import Serializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token





logger = logging.getLogger(__name__)

class SignupView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'name': user.name,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)
    
    #         hashed_password = make_password(password)


class LoginView1(KnoxLoginView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Hash the provided password using SHA-256
        hashed_password = make_password(password)

        print(hashed_password)

        # Use Django's authenticate function
        user = authenticate(request, email=email, password=hashed_password)

        if user:
            # If authentication is successful, generate or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'email': user.email, 'mobile': user.mobile, 'city': user.city})
        else:
            # If authentication fails, return an error response
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)