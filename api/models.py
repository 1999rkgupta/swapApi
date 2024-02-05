from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Email(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='user_email')
    email = models.EmailField(unique=True)

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.OneToOneField(Email, on_delete=models.CASCADE, related_name='user_profile')
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(default="avatar.png", blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-created_at"]

class Mobile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_mobile')
    mobile = models.CharField(max_length=15, unique=True)

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_token')
    token = models.CharField(max_length=255, blank=True, null=True)

class IPAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_ip_address')
    ip_address = models.GenericIPAddressField()

class LoginTime(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_login_time')
    login_time = models.DateTimeField(default=timezone.now)

class Name(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_name')
    name = models.CharField(max_length=100)

class City(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_city')
    city = models.CharField(max_length=100)
