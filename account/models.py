from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('поле email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', **extra_fields)
        extra_fields.setdefault('is_active', **extra_fields)
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email