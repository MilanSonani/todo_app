from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=datetime.now())
    update_at = models.DateTimeField(auto_now=datetime.now())


class User(AbstractUser):
    ROLE = (
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member')
    )

    role = models.CharField(max_length=15, choices=ROLE)#, default='MEMBER')
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Book(BaseModel):
    CHOICES = (
        ('BORROWED', 'Borrowed'),
        ('AVAILABLE', 'Available')
    )
    status = models.CharField(max_length=15, choices=CHOICES, default='AVAILABLE')
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()

