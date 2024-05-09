import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class TemporaryUser(models.Model):
    phone_number = models.CharField(unique=True, max_length=11)

    otp_code = models.CharField(max_length=4)
    otp_code_expiration = models.DateTimeField(blank=True)

    def __str__(self):
        return self.phone_number

    def is_otp_valid(self):
        """
        Check if the OTP code is still valid based on the expiration time.
        """
        return self.otp_code_expiration > timezone.now()


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=80, blank=True, default='کاربر')
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=11)
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    job_title = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_user_permissions'
    )

    profile_image = models.ImageField(upload_to='static/accounts/profile_pics/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
