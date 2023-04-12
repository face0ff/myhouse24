import datetime

from django.contrib.auth.models import User
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
                Role.objects.create(roles=index[0], statistics=False, cashbox=True, invoice=False,
                                    personal_account=True,apartment=False, owner=True, house=False, message=True,
                                    application=False, meter=True, site_management=False, service=True, tariff=False,
                                    rol=True, users=False, requisites=True)
            print('user create successful')


        if User.objects.count() == 0:
            username = 'admin'
            email = 'admin@mail.com'
            password = '1542'
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
        else:
            print('Админа в студию')
        if UserProfile.objects.count() == 0:
            for index in range(5):
                UserProfile.objects.create(id=(index+1), email=index, is_staff=False, is_active=True,
                                           date_joined=datetime.datetime.now(), user_id=(index+1), first_name=index, last_name=index,
                                           patronymic=index, avatar='index', telephone=index, viber=index, telegram='index',
                                           notes=index, status='is_active', role=Role.objects.get(pk=(index+1)))
            print('user create successful')