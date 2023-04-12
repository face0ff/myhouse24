import datetime

from django.core.management.base import BaseCommand

from house_app.models import Apartment
from services_app.models import *


class Command(BaseCommand):
    help = 'site_app'

    def handle(self, *args, **kwargs):
        if Unit.objects.count() == 0:
            Unit.objects.create(name='electro'),

            print('unit create successful')

        if Tariff.objects.count() == 0:
            Tariff.objects.create(title='electro', description='electro', date_edit=datetime.datetime.now()),
            print('Tariff create successful')

        if Services.objects.count() == 0:
            Services.objects.create(main='111', unit=Unit.objects.get(pk=1), show=True)
            print('Service create successful')

        if PriceTariffServices.objects.count() == 0:
            PriceTariffServices.objects.create(price=111, tariff=Tariff.objects.get(pk=1),
                                               services=Services.objects.get(pk=1)),
            print('PriceITD create successful')

        if MeterReading.objects.count() == 0:

            MeterReading.objects.create(number=11, expense=11, status='new',
                                        date=datetime.datetime.now(), meter=Services.objects.get(pk=1),
                                        apartment=Apartment.objects.get(pk=1))
            print('Meter create successful')

        if Requisite.objects.count() == 0:
            Requisite.objects.create(name='111', information='information')
            print('Requisite create successful')

        if Item.objects.count() == 0:
            Item.objects.create(name='111', income_invoice='income')
            print('Requisite create successful')