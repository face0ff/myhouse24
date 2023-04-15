from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from house_app.models import House, Request, Account, Apartment, Transfers
from user_app.models import UserProfile


# Create your views here.


class Stat(TemplateView):
    template_name = 'admin/statistic.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.all()
        context['owners'] = UserProfile.objects.filter(status='active', role__isnull=True)
        context['requests'] = Request.objects.all()
        context['requests_new'] = Request.objects.filter(status='new')
        context['accounts'] = Account.objects.all()
        context['apartments'] = Apartment.objects.all()
        context['balance'] = \
            Account.objects.filter(status='active', balance__gt=0).aggregate(total_balance=Sum('balance'))[
                'total_balance']
        context['debt'] = \
            Account.objects.filter(status='active', balance__lt=0).aggregate(total_debt=Sum('balance'))[
                'total_debt']
        context['cashbox'] = \
            Transfers.objects.filter(completed=True).aggregate(total_cash=Sum('amount'))[
                'total_cash']

        return context






