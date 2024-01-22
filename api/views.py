from datetime import datetime
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .models import User
from .serializers import UserSerializer
from django.db import models
from django.db.models import Q
from rest_framework.authtoken.models import Token



class DefaultAPIView(generics.GenericAPIView):
    def get(self, request):
        return Response({"message": "API is running!"}, status=status.HTTP_200_OK)

class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(models.Q(email=username) | models.Q(mobile=username)).first()

        if user is not None and user.check_password(password):
            _, token = AuthToken.objects.create(user)
            user.last_login = datetime.now()
            user.save()
            return Response({
                'user': UserSerializer(user).data,
                'token': token
            })
        elif user is None:
            return Response({'error': 'User not found with the provided email/mobile.'})
        else:
            return Response({'error': 'Invalid password.'})

class SignupAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        included_fields = ('name', 'email', 'password', 'mobile', 'city', 'role', 'created_at', 'updated_at', 'last_login')
        serializer = UserSerializer(data=request.data, fields=included_fields)
        
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateAPI(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DeleteAPI(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GetUserAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # or 'pk' depending on your implementation

    def get_object(self):
        return self.request.user