# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, mobile, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)  # Store hashed password
    city = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = User.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        # Use Django's check_password method
        return check_password(raw_password, self.password)
