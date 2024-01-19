from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone  # Add this import line
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class DefaultAPIView(APIView):
    def get(self, request):
        return Response({"message": "API is running!"}, status=status.HTTP_200_OK)

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # Customize the response message
        response_data = {
            'message': 'User {user.name} created successfully!',
            'name': user.name,
            'email': user.email,
            # Include any other relevant information
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Update last_login
        user.last_login = timezone.now()
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Store login history (you may need to adapt this based on your model)
        user.log_login_history(access_token, request.META.get('REMOTE_ADDR'))

        return Response({'user': UserSerializer(user).data, 'access_token': access_token})
    
class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_id = request.data.get('userid')

        if not user_id:
            return Response({'detail': 'User ID is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user making the request matches the provided user ID
        if self.request.user.id != int(user_id):
            return Response({'detail': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the update
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())

    def get_object(self):
        return self.request.user

class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user_id = request.data.get('userid')

        if not user_id:
            return Response({'detail': 'User ID is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user making the request matches the provided user ID
        if self.request.user.id != int(user_id):
            return Response({'detail': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
    

class GetUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)