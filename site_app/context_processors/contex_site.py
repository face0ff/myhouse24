from site_app.models import Contacts


def welcome(request):
    url = Contacts.objects.all().first()

    return {
        'url': url,
        }