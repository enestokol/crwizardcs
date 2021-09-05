from uuid import uuid1
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_active, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('You must be enter a valid email address')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, is_active=is_active, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, is_active=True, is_staff=False, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, is_active=True, is_staff=True, is_superuser=True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=60, null=False, blank=False)
    last_name = models.CharField(max_length=60, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def unique_username(self):
        username = slugify(self.first_name.replace('ı', 'i').lower() + self.first_name.replace('ı', 'i').lower())
        while CustomUser.objects.filter(username=username).exists():
            unique = uuid1().hex[:1]
            # username = slugify(self.username.replace('ı', 'i')) + "-" + str(unique)
            username = username + str(unique)
        return username
