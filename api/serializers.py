from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'email', 'password', 'role', 'creationDate', 'city']  # Include id and city
        extra_kwargs = {'password': {'write_only': True}}

    # ... other methods (unchanged)


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # Optional validation examples (adjust as needed)
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        elif not value.endswith("@gmail.com"):  # Replace with your domain
            raise serializers.ValidationError("Email must be a valid gmail.com address.")
        return value

    # Add validation for other fields as needed

class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()