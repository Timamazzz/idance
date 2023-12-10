# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from phonenumbers import is_valid_number, parse as parse_phone


class PhoneNumberValidator(RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = 'Enter a valid phone number.'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone_number, password, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be set')

        if phone_number:
            phone_number = parse_phone(phone_number, "RU")
            if not is_valid_number(phone_number):
                raise ValueError('Invalid phone number')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email")
    phone_number = models.CharField(
        validators=[PhoneNumberValidator()],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.phone_number or self.email
