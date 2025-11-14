from enum import Enum
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from enumfields import EnumField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Admin users must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)
    

class UserRole(Enum):
    CONSUMER = "consumer"
    FARMER = "farmer"
    RETAILER = "retailer"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=150, unique=True)
    phone = PhoneNumberField(unique=True, region='KE', null=True, blank=True)
    location = models.CharField(max_length=255)
    role = EnumField(UserRole, default=UserRole.CONSUMER, max_length=64)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # attach the user manager for queries.
    objects = UserManager()

    # the primary credential that uniquely identifies all users is the email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-is_active", "created_at"]
