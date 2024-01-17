from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.utils import timezone  # Add this import line
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView


class DefaultAPIView(APIView):
    def get(self, request):
        return Response({"message": "API is running!"}, status=status.HTTP_200_OK)

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Use the correct user model for AuthToken creation
        token, _ = AuthToken.objects.create(CustomUser.objects.get(email=user.email))

        return Response({'user': UserSerializer(user).data, 'token': token})
    
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