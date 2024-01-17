from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password, role, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            mobile=mobile,
            role=role,
            creationDate=timezone.now(),  # Automatically set creation date
            **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    # ... other methods for creating superuser, etc.

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    creationDate = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)
    city = models.CharField(max_length=100)  # Add the city field

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'role']

    # ... other methods for checking password, __str__, etc.
