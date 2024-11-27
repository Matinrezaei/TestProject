from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")
        extra_fields.setdefault('is_active', True)

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=False,
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Phone number'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    deleted_at = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Deleted at'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is staff'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Is superuser'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return str(self.phone_number)
    
