# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    preferred_language = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        app_label = 'users'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
