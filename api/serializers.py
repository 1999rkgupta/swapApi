from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    included_fields = ['id', 'name', 'city', 'email', 'mobile', 'password', 'last_login', 'created_at', 'updated_at', 'role']
    
    class Meta:
        model = User
        fields = ['id', 'name', 'city', 'email', 'mobile', 'password', 'last_login', 'created_at', 'updated_at', 'role']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_included_fields(self):
        return self.included_fields
    
    def to_representation(self, instance):
        included_fields = self.get_included_fields()
        data = super().to_representation(instance)
        return {field_name: data[field_name] for field_name in included_fields}