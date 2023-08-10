from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser
from django.db import models


# class Student(models.Model):
#     index_number = models.CharField(max_length=20, default=None, unique=True)
#     email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
#     first_name = models.CharField(max_length=200)
#     middle_name = models.CharField(max_length=200)
#     surname = models.CharField(max_length=200)
#     box_no = models.CharField(max_length=10)
#     box_code = models.CharField(max_length=10)
#     town = models.CharField(max_length=200)
#     email_address = models.CharField(max_length=200)
#     fee_boarder = models.CharField(max_length=200)
#     fee_day = models.CharField(max_length=200)
#     country = models.CharField(max_length=200)
#     course = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=10)
#     phone_number2 = models.CharField(max_length=10)
#
#     REGULAR = 'REGULAR'
#     EVENING = 'EVENING'
#     MODE_CHOICES = [
#         (REGULAR, 'REGULAR'),
#         (EVENING, 'EVENING'),
#     ]
#     mode = models.CharField(max_length=50, choices=MODE_CHOICES)
#
#     def __str__(self):
#         full_name = self.first_name + " " + self.middle_name + " " + self.surname
#         return full_name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Student(AbstractUser, PermissionsMixin):
    index_number = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    box_no = models.CharField(max_length=10)
    box_code = models.CharField(max_length=10)
    town = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    fee_boarder = models.CharField(max_length=200)
    fee_day = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15)
    REGULAR = 'REGULAR'
    EVENING = 'EVENING'
    MODE_CHOICES = [
        (REGULAR, 'REGULAR'),
        (EVENING, 'EVENING'),
    ]
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        full_name = self.first_name + " " + self.middle_name + " " + self.surname
        return full_name
