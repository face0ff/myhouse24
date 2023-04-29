import datetime

from django.db import models
from django.utils import timezone

from services_app.models import Tariff, Services, Item
from site_app.models import Service
from user_app.models import UserProfile, Role


class House(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    image_1 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 1')
    image_2 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 2')
    image_3 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 3')
    image_4 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 4')
    image_5 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 5')
    users = models.ManyToManyField(UserProfile, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return f"{self.name}"


class Floor(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return f"{self.name}"


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='apartment',
                              verbose_name='Владелец')
    house = models.ForeignKey(House, null=True, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тариф')
    number = models.IntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь (кв.м.)')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['section', 'floor', 'number']

    def __str__(self):
        return f"{self.number}"

class Request(models.Model):
    CHOICES = (('new', 'Новое'),
               ('in_work', 'В работе'),
               ('done', 'Выполнено'))

    status = models.CharField(max_length=7, choices=CHOICES, default='new', verbose_name='Статус')
    TYPES = (('any', 'Любой специалист'),
             ('electric', 'Электрик'),
             ('plumber', 'Сантехник'))
    type_master = models.CharField(max_length=16, choices=TYPES, default='any', verbose_name='Тип мастера')
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.time)
    description = models.TextField()
    comment = models.TextField(blank=True)
    master = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=32)
    text = models.TextField()
    is_dept = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='owner_messages')
    apartment = models.ForeignKey(Apartment, blank=True, null=True, on_delete=models.CASCADE)
    house = models.ForeignKey(House, blank=True, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, blank=True, null=True, on_delete=models.SET_NULL)
    floor = models.ForeignKey(Floor, blank=True, null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='sender')


def account_number():
    last = Account.objects.all().order_by('number').last()
    if not last:
        return '1'.zfill(10)
    number = int(last.number) + 1
    return str(number).zfill(10)

class Account(models.Model):
    number = models.BigIntegerField(default=account_number, unique=True,
                                             verbose_name='Номер лицевого счета')
    CHOICES = (('active', 'Активный'),
               ('inactive', 'Неактивный'))
    status = models.CharField(choices=CHOICES, max_length=16, default='active', verbose_name='Статус')
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, null=True, related_name='account',
                                     blank=True, verbose_name='Номером Квартиры')
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Остаток (грн.)')

    class Meta:
        verbose_name = 'Лицевой счет'
        verbose_name_plural = 'Лицевые счета'

    def __str__(self):
        return str(self.number).zfill(10)


class InvoiceService(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Квитанция')
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Услуга')
    cost_for_unit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена за ед., грн.')
    expense = models.IntegerField(verbose_name='Расход')
    full_cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость, грн.')

    class Meta:
        verbose_name = 'Услуга для квитанции'
        verbose_name_plural = 'Услуги для квитанций'
        unique_together = ['invoice', 'service']

def invoice_number():
    largest = Invoice.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)

class Invoice(models.Model):
    number = models.BigIntegerField(default=invoice_number, unique=True, verbose_name='Номер квитанции')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT, verbose_name='Квартира')
    done = models.BooleanField(default=True, verbose_name='Проведена')
    CHOICES = (('paid', 'Оплачена'),
               ('piece', 'Частично оплачена'),
               ('unpaid', 'Неоплачена'))
    status = models.CharField(max_length=16, choices=CHOICES, default='unpaid', verbose_name='Статус')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Тариф')
    date_from = models.DateField(default=timezone.now, verbose_name='Период с')
    date_before = models.DateField(default=timezone.now, verbose_name='Период до')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, verbose_name='Сумма')
    services = models.ManyToManyField(Services, through=InvoiceService, through_fields=('invoice', 'service'),
                                      verbose_name='Услуги')

    class Meta:
        verbose_name = 'Квитанция'
        verbose_name_plural = 'Квитанции'

    def __str__(self):
        return str(self.number).zfill(10)

def transfer_number():
    largest = Transfers.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)

class Transfers(models.Model):
    number = models.BigIntegerField(default=transfer_number, unique=True, verbose_name='Номер ведомости')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True,
                              related_name='owner', verbose_name='Владелец квартиры')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True,
                                         verbose_name='Лицевой счет')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Статья')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма')
    completed = models.BooleanField(default=True, verbose_name='Проведен')
    manager = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='manager',
                                verbose_name='Менеджер')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    income = models.BooleanField(default=True, verbose_name='Приходная ведомость')

    class Meta:
        verbose_name = 'Приход/Расход'
        verbose_name_plural = 'Приходные/Расходные ведомости'

    def __str__(self):
        return str(self.number).zfill(10)

class Template(models.Model):
    name = models.CharField(max_length=16, default='template', verbose_name='Шаблон')
    type = models.BooleanField(default=False, verbose_name='Назначить шаблоном по умоланию')
    file = models.FileField("Шаблонь", upload_to="files")