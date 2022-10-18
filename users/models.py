import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    language = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


def number_of_days_left():
    return timezone.now() + timezone.timedelta(days=1)


class ResetPassword(models.Model):
    user = models.ForeignKey(CustomUser, models.DO_NOTHING)
    url_id = models.CharField(
        max_length=50, unique=True, default=uuid.uuid4, editable=False
    )
    created_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=False, default=number_of_days_left)

    def __str__(self) -> str:
        return f"{self.user} - {self.url_id}"
