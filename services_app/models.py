from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models import ForeignKey


# Create your models here.





class Unit(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"{self.name}"


class Tariff(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField()
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class PriceTariffServices(models.Model):

    price = models.DecimalField(max_digits=10, decimal_places=2)
    tariff = models.ForeignKey('Tariff', on_delete=models.CASCADE, blank=True)
    services = models.ForeignKey('Services', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tariff', 'services')


class Services(models.Model):
    main = models.CharField("Услуга", max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Ед. изм.')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.main


class MeterReading(models.Model):
    number = models.BigIntegerField(unique=True, verbose_name='Номер показания')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    apartment = ForeignKey('house_app.Apartment', on_delete=models.CASCADE, verbose_name='Квартира')
    meter = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Счетчик')
    CHOICES = (('new', 'Новое'),
               ('accounted', 'Учтено'),
               ('paid', 'Учтено и оплачено'),
               ('zero', 'Нулевое'))
    status = models.CharField(max_length=16, choices=CHOICES, default='new', verbose_name='Статус')
    expense = models.IntegerField(verbose_name='Показания счетчика')

    class Meta:
        verbose_name = 'Показание счетчика'
        verbose_name_plural = 'Показания счетчика'

    def __str__(self):
        return str(self.number).zfill(10)


class Requisite(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название компании')
    information = models.TextField(verbose_name='Информация')

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    CHOICES = (('income', 'Приход'),
               ('expense', 'Расход'))
    income_invoice = models.CharField(max_length=16, choices=CHOICES, default='income', verbose_name='Приход/Расход')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.name