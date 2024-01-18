from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class LoginHistory(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    login_timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField()

    # Add other fields as needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def user_exists(self, email_or_mobile):
        return (
            self.objects.filter(email=email_or_mobile).exists() or
            self.objects.filter(mobile=email_or_mobile).exists()
        )

    def log_login_history(self, access_token, ip_address):
        # Get the 5 most recent login history records
        recent_logins = self.loginhistory_set.order_by('-login_timestamp')[:4]

        # Create a new login history entry
        login_history = LoginHistory.objects.create(
            user=self,
            access_token=access_token,
            ip_address=ip_address
        )

        # Link the new entry to the user
        recent_logins = [login_history] + list(recent_logins)
        self.loginhistory_set.set(recent_logins)