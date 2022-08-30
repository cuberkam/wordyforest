from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(unique=False, max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
