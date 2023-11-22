from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="почта", unique=True)
    phone = models.CharField(max_length=30, verbose_name="телефон", **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="страна", **NULLABLE)
    verification_code = models.CharField(max_length=50, verbose_name="код активации", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

