from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from .backends import EmailOrMobileBackend
from django.db import IntegrityError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
            return user
        except IntegrityError as e:
            print("e",e)
            if 'unique constraint' in str(e).lower():
                raise serializers.ValidationError({'error': 'user with this email or mobile already exists.'})
            else:
                raise serializers.ValidationError({'error': 'Unable to create user.'})

class LoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_or_mobile = data.get('email_or_mobile')
        password = data.get('password')

        # Use the custom authentication backend
        user = EmailOrMobileBackend().authenticate(request=self.context.get('request'), email_or_mobile=email_or_mobile, password=password)

        if not user:
            # Check whether the email or mobile is wrong
            if not EmailOrMobileBackend().user_exists(email_or_mobile):
                raise serializers.ValidationError({'error': 'Wrong email or mobile'})

            # Check whether the password is wrong
            raise serializers.ValidationError({'error': 'Invalid credentials'})

        data['user'] = user
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Exclude the password field from the response
        data.pop('password', None)
        return data
