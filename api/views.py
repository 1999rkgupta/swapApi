from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import User
from .serializers import UserSerializer
import logging
from knox.views import LoginView as KnoxLoginView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView  
from knox.auth import TokenAuthentication
from rest_framework.serializers import Serializer



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
    

class LoginView1(KnoxLoginView):
   permission_classes = [AllowAny]

   def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        _, token = self.create_knox_token(None, user, request)

        return Response({
            'token': token,
            'user_id': user.id,
            'email': user.email,
            # Include other desired user details as needed
        }, status=status.HTTP_200_OK)