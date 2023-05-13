from random import randint

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.utils import timezone


# class CustomUserManager(BaseUserManager):
#
#     def create_user(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         if not email:
#             raise ValueError('The Email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    email = models.EmailField('E-mail', unique=True)

    # username = None
    # objects = CustomUserManager()
    username = models.CharField(max_length=32, default='user')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    user_id = models.CharField(max_length=5, unique=True, null=True, blank=True, verbose_name='ID')
    first_name = models.CharField(max_length=32, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=32, blank=True, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=32, blank=True, verbose_name='Отчество')
    avatar = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Аватар')
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    viber = models.CharField(max_length=20, null=True, blank=True, verbose_name='Viber')
    telegram = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telegram')
    notes = models.TextField(null=True, blank=True, verbose_name='О владельце (заметки)')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    CHOICES = (('is_active', 'Активен'),
               ('new', 'Новый'),
               ('disable', 'Отключен'))
    status = models.CharField(max_length=16, choices=CHOICES, default='new', verbose_name='Статус')
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Роль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Role(models.Model):
    CHOICES = (('director', 'Директор'),
               ('manager', 'Менеджер'),
               ('accountant', 'Бухгалтер'),
               ('electric', 'Электрик'),
               ('plumber', 'Сантехник'))
    roles = models.CharField(max_length=16, choices=CHOICES, default='director', blank=True, verbose_name='Роль')
    statistics = models.BooleanField(default=False, verbose_name='Доступ к статистике')
    cashbox = models.BooleanField(default=False, verbose_name='Доступ к кассе')
    invoice = models.BooleanField(default=False, verbose_name='Доступ к квитанциям')
    personal_account = models.BooleanField(default=False, verbose_name='Доступ к лицевым счетам')
    apartment = models.BooleanField(default=False, verbose_name='Доступ к квартирам')
    owner = models.BooleanField(default=False, verbose_name='Доступ к владельцам квартир')
    house = models.BooleanField(default=False, verbose_name='Доступ к домам')
    message = models.BooleanField(default=False, verbose_name='Доступ к сообщениям')
    application = models.BooleanField(default=False, verbose_name='Доступ к заявкам вызова мастера')
    meter = models.BooleanField(default=False, verbose_name='Доступ к показаниям счетчиков')
    site_management = models.BooleanField(default=False, verbose_name='Доступ к управлению сайтом')
    service = models.BooleanField(default=False, verbose_name='Доступ к услугам')
    tariff = models.BooleanField(default=False, verbose_name='Доступ к тарифам')
    rol = models.BooleanField(default=False, verbose_name='Доступ к ролям')
    users = models.BooleanField(default=False, verbose_name='Доступ к пользователям')
    requisites = models.BooleanField(default=False, verbose_name='Доступ к реквизитам')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
