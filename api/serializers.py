from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "id", "avatar"]

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims to the token
        user = self.user
        data['email'] = user.email
        data['avatar'] = user.avatar.url
        data['is_staff'] = user.is_staff
        data['name'] = user.name

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate_email_or_mobile(self, email_or_mobile, password):
        user = None

        # Check if the input is an email
        if '@' in email_or_mobile:
            user = User.objects.filter(email=email_or_mobile).first()
        else:
            # Assuming it's a mobile number, adjust this logic based on your actual implementation
            user = User.objects.filter(mobile=email_or_mobile).first()

        if user and user.check_password(password):
            return user
        return None

    def validate(self, attrs):
        email_or_mobile = attrs.get('email_or_mobile', None)
        password = attrs.get('password', None)

        if email_or_mobile and password:
            user = self.validate_email_or_mobile(email_or_mobile, password)

            if user:
                attrs['user'] = user
                return super().validate(attrs)

        raise serializers.ValidationError("Unable to log in with provided credentials.")
