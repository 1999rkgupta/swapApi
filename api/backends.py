from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, email_or_mobile=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email_or_mobile)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(mobile=email_or_mobile)
            except CustomUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def user_exists(self, email_or_mobile):
        return (
            CustomUser.objects.filter(email=email_or_mobile).exists() or
            CustomUser.objects.filter(mobile=email_or_mobile).exists()
        )