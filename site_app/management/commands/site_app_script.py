from django.core.management.base import BaseCommand

from site_app.models import *


class Command(BaseCommand):
    help = 'site_app'

    def handle(self, *args, **kwargs):

        if AditGallery.objects.count() == 0:
            AditGallery.objects.create(adit_image='1')
            print('AditImage create successful')

        if Gallery.objects.count() == 0:
            Gallery.objects.create(image='1')
            print('Image create successful')

        if Service.objects.count() == 0:
            for index in range(2):
                seo = Seo.objects.create(titles=index, descriptions=index, keywords=index)
                Service.objects.create(seo=seo)
                print('Service create successful')

        if Main.objects.count() == 0:
            Seo.objects.create(titles='main', descriptions='main', keywords='main')
            Main.objects.create(header='index', description='index', show_url=True, slider_1='1', slider_2='1',
                                slider_3='1', seo_id=1)
            print('Main create successful')

        if Block.objects.count() == 0:
            for index in range(6):
                Block.objects.create(header=index, description=index, service_id=1, image='1')
            print('Block create successful')
        if Block.objects.count() == 6:
            for index in range(2):
                Block.objects.create(header=index, description=index, service_id=2, image='1')
            print('Block create successful')

        if Info.objects.count() == 0:
            seo = Seo.objects.create(titles='info', descriptions='info', keywords='info')
            Info.objects.create(header='index', text='index', photo='1', adit_header=1, adit_text=1,
                                seo=seo)
            print('Main create successful')

        if Contacts.objects.count() == 0:
            seo = Seo.objects.create(titles='contact', descriptions='contact', keywords='contact')
            Contacts.objects.create(header='index', text='index', url=1, map=1, fio=1, address='index', location=1,
                                    phone=1, email=1, seo=seo)
            print('Main create successful')

        if Files.objects.count() == 0:
            Files.objects.create(name=1, files='1')
            print('AditImage create successful')
