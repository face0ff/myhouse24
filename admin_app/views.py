from django.db.models import Sum, Q
from django.shortcuts import render
from django.views.generic import TemplateView

from house_app.models import House, Request, Account, Apartment, Transfers, Invoice
from user_app.models import UserProfile


# Create your views here.


class Stat(TemplateView):
    template_name = 'admin/statistic.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.all()
        context['owners'] = UserProfile.objects.filter(is_active=True, role__isnull=True)
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
        list_debts_by_month = []
        list_incomes_by_month = []
        for i in range(1, 13):
            debt_by_month = Invoice.objects.all().aggregate(sum=Sum('amount', filter=(Q(date__month=i) & Q(done=True) &
                                                                         (Q(status='unpaid') | Q(status='piece')))))
            income_by_month = Transfers.objects.all().aggregate(sum=Sum('amount', filter=Q(date__month=i, income=True,
                                                                                completed=True)))
            list_debts_by_month.append(int(debt_by_month['sum']) if debt_by_month['sum'] else 0)
            list_incomes_by_month.append(int(income_by_month['sum']) if income_by_month['sum'] else 0)
        print(list_incomes_by_month)
        print(list_debts_by_month)
        context['list_debts_by_month'] = list_debts_by_month
        context['list_incomes_by_month'] = list_incomes_by_month

        return context






