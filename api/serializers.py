from rest_framework import serializers
from .models import CustomUser
from django.db import models  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_or_mobile = data.get('email_or_mobile')
        password = data.get('password')

        user = CustomUser.objects.filter(
            models.Q(email=email_or_mobile) | models.Q(mobile=email_or_mobile)
        ).first()

        if user and user.check_password(password):
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid credentials")

        return data
