from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with the given phone number and password.
        """
        User = get_user_model()
        if not phone_number:
            raise ValueError('The phone number must be set')

        # Normalize the phone number by removing spaces and hyphens
        phone_number = self.normalize_phone_number(phone_number)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Set the password for the user
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser with the given phone number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing spaces, hyphens, and other special characters.
        """
        # Implement your normalization logic here based on your requirements
        normalized_number = phone_number.replace(" ", "").replace("-", "")
        return normalized_number
