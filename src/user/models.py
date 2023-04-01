from django_countries.fields import CountryField
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class UserModel(AbstractUser):
    username = models.CharField(null=True, blank=True, max_length=64)
    guid = models.UUIDField(default=uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True)
    country = CountryField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

