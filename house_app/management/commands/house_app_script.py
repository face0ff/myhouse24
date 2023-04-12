import datetime

from django.core.management.base import BaseCommand


from house_app.models import *


class Command(BaseCommand):
    help = 'site_app'

    def handle(self, *args, **kwargs):
        if Section.objects.count() == 0:
            Section.objects.create(name='Vtoraja'),

            print('Section create successful')

        if Floor.objects.count() == 0:
            Floor.objects.create(name=1),
            print('Floor create successful')


        if House.objects.count() == 0:
            house = House.objects.create(name='111', address='111', image_1='111', image_2='111', image_3='111', image_4='111',
                                 image_5='111',)
            house.sections.set(Section.objects.all())
            house.floors.set(Floor.objects.all())
            house.users.set(UserProfile.objects.all())
            house.save()

        if Apartment.objects.count() == 0:
            Apartment.objects.create(number=111, area='111', section=Section.objects.get(pk=1), floor=Floor.objects.get(pk=1),
                                 owner=UserProfile.objects.get(pk=1), tariff=Tariff.objects.get(pk=1))
            print('House create successful')

