import datetime

from django.core.management.base import BaseCommand


from house_app.models import *


class Command(BaseCommand):
    help = 'site_app'

    def handle(self, *args, **kwargs):

        if House.objects.count() == 0:
            house = House.objects.create(name='111', address='111', image_1='111', image_2='111', image_3='111', image_4='111',
                                 image_5='111',)

        if Apartment.objects.count() == 0:
            Apartment.objects.create(number=111, area='111', section=Section.objects.create(house_id=house.id), floor=Floor.objects.create(house_id=house.id),
                                 owner=UserProfile.objects.get(pk=1), tariff=Tariff.objects.create())
            print('House create successful')




