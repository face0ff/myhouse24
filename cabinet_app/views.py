import datetime

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView

from house_app.forms import RequestForm
from house_app.models import *
from services_app.models import Tariff, Services, PriceTariffServices
from user_app.forms import OwnerUpdateForm


# Create your views here.
# class cabinet_stat(TemplateView):
#     template_name = 'cabinet_statistic.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         first = Apartment.objects.filter(owner=self.request.user).first()
#         try:
#             context['account'] = Account.objects.get(apartment=first)
#         except:
#             pass
#         dateList = []
#         for i in Invoice.objects.all().values('date'):
#             dateList.append(str(i['date']).split('-')[1])
#         length = len(set(dateList))
#
#         amount = Invoice.objects.filter(amount__gt=0).aggregate(total_amount=Sum('amount'))[
#             'total_amount']
#         if amount:
#             average = amount / length
#             context['avarage'] = average
#         else:
#             context['avarage'] = '0'
#
#         today = datetime.date.today()  # Get the current date
#         month_number = today.month
#
#         services1 = Invoice.objects.filter(apartment_id=14, date__month=month_number).values(
#             'services__unit__name').annotate(total_cost=Sum('amount'))
#         print([int(d['total_cost']) for d in services1])
#
#         context['list_name'] = [d['services__unit__name'] for d in services1]
#         context['list_cost '] = [int(d['total_cost']) for d in services1]
#         return context
#

class OwnerApartmentDetail(DetailView):
    model = Apartment
    template_name = 'cabinet_statistic.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['account'] = Account.objects.get(apartment=self.object.id)
        except:
            pass
        dateList = []
        for i in Invoice.objects.all().values('date'):
            dateList.append(str(i['date']).split('-')[1])
        length = len(set(dateList))

        amount = Invoice.objects.filter(apartment=self.object.id, amount__gt=0).aggregate(total_amount=Sum('amount'))[
            'total_amount']
        if amount:
            average = amount / length
            context['avarage'] = round(average, 2)
        else:
            context['avarage'] = '0'

        today = datetime.date.today()  # Get the current date
        month_number = today.month
        list_debts_by_month = []
        for i in range(1, 13):
            debt_by_month = Invoice.objects.all().aggregate(sum=Sum('amount', filter=(Q(apartment_id=self.object.id) & Q(date__month=i) & Q(done=True) &
                                                                                      (Q(status='unpaid') | Q(
                                                                                          status='piece')))))
            list_debts_by_month.append(int(debt_by_month['sum']) if debt_by_month['sum'] else 0)
        if sum(list_debts_by_month) > 0:
            context['list_debts_by_month'] = list_debts_by_month
        services1 = Invoice.objects.filter(apartment_id=self.object.id, date__month=month_number).values(
            'services__unit__name').annotate(total_cost=Sum('invoiceservice__full_cost'))
        print([d['total_cost'] for d in services1])
        context['list_name'] = [d['services__unit__name'] for d in services1]
        context['list_cost'] = [d['total_cost'] for d in services1]
        return context


class OwnerInvoiceList(ListView):
    model = Invoice
    template_name = 'cabinet_invoice.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.id)
        owner_invoice = Invoice.objects.filter(apartment__owner=self.request.user)
        if self.request.GET.get('apartment'):
            context['object_list'] = owner_invoice.filter(apartment=self.request.GET.get('apartment'))
        else:
            context['object_list'] = owner_invoice
        return context


def select_owner_invoice(request):
    print(request.GET.get('apartment'))
    draw = request.GET['draw']
    owner_invoice = Invoice.objects.filter(apartment__owner=request.user)
    if request.GET.get('filterApart'):
        owner_invoice = owner_invoice.filter(apartment=request.GET.get('filterApart'))

    owner_invoice_list = []
    filters = Q()

    if request.GET['filterDate']:
        filters &= Q(date=request.GET.get('filterDate'))
    if request.GET['filterStatus']:
        filters &= Q(status=request.GET['filterStatus'])

    owner_invoice = owner_invoice.filter(filters)

    for invoice in owner_invoice:
        # print(invoice.number)
        invoice_dict = {
            'number': invoice.number,
            'date': invoice.date.strftime('%d.%m.%Y'),
            'status': invoice.get_status_display(),
            'amount': invoice.amount,
            'id': invoice.id
        }
        owner_invoice_list.append(invoice_dict)

    page_number = request.GET.get('page')
    paginator = Paginator(owner_invoice_list, 10)
    page_obj = paginator.get_page(page_number)

    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': list(page_obj.object_list),
    }
    return JsonResponse(response, status=200)


class OwnerInvoiceDetail(DetailView):
    model = Invoice
    template_name = 'cabinet_invoice_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_service = InvoiceService.objects.filter(invoice=self.object.id)
        context['invoice_service'] = invoice_service
        context['template_default'] = Template.objects.get(type=True)
        return context

class OwnerTariffList(ListView):
    model = Services
    template_name = 'cabinet_tariff.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('apartment'):
            context['servises_list'] = PriceTariffServices.objects.filter(tariff__apartment=self.request.GET.get('apartment')),
            context['apartment'] = Apartment.objects.get(id=self.request.GET.get('apartment'))
        return context

class OwnerMessageList(ListView):
    model = Message
    template_name = 'cabinet_message.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['message_list'] = Message.objects.filter(owner=self.request.user)
        return context


class OwnerMessageDetail(DetailView):
    model = Message
    template_name = 'cabinet_message_detail.html'

class OwnerRequestList(ListView):
    model = Request
    template_name = 'cabinet_request_list.html'

class OwnerRequestCreate(CreateView):
    model = Request
    template_name = 'cabinet_request_create.html'
    form_class = RequestForm
    success_url = reverse_lazy('owner_request_list')

    # def form_valid(self, form):
    #     print('lol')
    #
    # def form_invalid(self, form):
    #     print(form.errors)

class OwnerDetail(DetailView):
    model = UserProfile
    template_name = 'cabinet_owner_detail.html'


class OwnerProfileUpdate(UpdateView):
    model = UserProfile
    template_name = 'cabinet_owner_update.html'
    form_class = OwnerUpdateForm

    def form_valid(self, form):
        try:
            body_text = f"Ваш новый пароль - {form.cleaned_data['password1']}"
            send_mail('Админ молодец', body_text, None, [form.cleaned_data['email']], fail_silently=False)
            return super().form_valid(form)
        except:
            return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy('owner_profile_detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('logout_page')

