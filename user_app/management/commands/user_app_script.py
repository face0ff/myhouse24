import datetime

from django.core.management.base import BaseCommand

from user_app.models import *


class Command(BaseCommand):
    help = 'site_app'

    def handle(self, *args, **kwargs):
        if Role.objects.count() == 0:
            CHOICES = (('director', 'Директор'),
                       ('manager', 'Менеджер'),
                       ('accountant', 'Бухгалтер'),
                       ('electric', 'Электрик'),
                       ('plumber', 'Сантехник'))
            for index in CHOICES:
                Role.objects.create(roles=index[0], statistics=True, cashbox=True, invoice=True,
                                    personal_account=True, apartment=True, owner=True, house=True, message=True,
                                    application=True, meter=True, site_management=True, service=True, tariff=True,
                                    rol=True, users=True, requisites=True)
            print('user create successful')

    if UserProfile.objects.count() == 0:
        for index in range(5):
            UserProfile.objects.create(id=(index + 1), email='123@gmail.com', is_staff=False, is_active=True,
                                       date_joined=datetime.datetime.now(), user_id=(index + 1), first_name=index,
                                       last_name=index, password='12345678Qw',
                                       patronymic=index, avatar='index', telephone=index, viber=index,
                                       telegram='index',
                                       notes=index, status='is_active', role=Role.objects.get(pk=(index + 1)))
        print('user create successful')
