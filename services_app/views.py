import json

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from django.http import HttpResponseRedirect, request, JsonResponse, HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib import messages
from copy import deepcopy

from house_app.models import House, Section, Apartment
from services_app.forms import ServicesForm, ServicesFormSet, UnitFormSet, TariffForm, PriceTariffServicesFormset, \
    PriceTariffServicesForm, RequisiteForm, ItemForm, MeterForm
from services_app.models import Services, Unit, Tariff, PriceTariffServices, Requisite, Item, MeterReading
from datetime import datetime



class ServicesAdmin(CreateView):
    model = Services
    template_name = 'services.html'
    form_class = ServicesForm
    qs = Services.objects.all()
    success_url = reverse_lazy('services')



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services_formset'] = ServicesFormSet(queryset=self.qs, prefix='services')
        context['unit_formset'] = UnitFormSet(queryset=Unit.objects.all(), prefix='unit')
        context['use_unit_id'] = [x.unit.id for x in Services.objects.select_related('unit').all()]
        return context

    def post(self, *args, **kwargs):
        self.object = None
        services_formset = ServicesFormSet(self.request.POST, self.request.FILES, prefix='services')
        unit_formset = UnitFormSet(self.request.POST, self.request.FILES, prefix='unit')


        if all([unit_formset.is_valid(), services_formset.is_valid()]):
            return self.form_valid(unit_formset, services_formset)
        else:
            return self.form_invalid(unit_formset, services_formset)

    def form_valid(self, unit_formset, services_formset):
        print(self.request.POST)
        items = unit_formset.save(commit=False)
        for item in unit_formset.deleted_objects:
            item.delete()
        for item in items:
            item.save()
        items = services_formset.save(commit=False)
        for item in services_formset.deleted_objects:
            item.delete()
        for item in items:
            item.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, unit_formset, services_formset, **kwargs):
        print(unit_formset.errors)
        print(services_formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(unit_formset=unit_formset, services_formset=services_formset))


class TariffsList(ListView):
    model = Tariff
    template_name = 'tariffs_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Tariff.objects.all()
        print(self.request.GET.get('filter'))
        if self.request.GET.get('filter') == '1':
            object_list = object_list.order_by('-title')
        if self.request.GET.get('filter') == '0':
            object_list = object_list.order_by('title')
        context['object_list'] = object_list
        return context

class TariffDetail(DetailView):
    model = Tariff
    template_name = 'tariff.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        inst = get_object_or_404(Tariff, id=self.get_object().pk)
        context['all_in'] = PriceTariffServices.objects.select_related('services', 'services__unit').filter(tariff_id=inst.pk)
        return context


class TariffCreate(CreateView):
    model = Tariff
    template_name = 'tariff_create.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariffs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk') != None:
            inst = get_object_or_404(Tariff, id=self.kwargs.get('pk'))

            context['tariff'] = TariffForm(instance=inst)
            context['price_formset'] = PriceTariffServicesFormset(
                queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                prefix='price')
        else:

            context['tariff'] = TariffForm()
            context['unit'] = Unit.objects.all()
            context['price_formset'] = PriceTariffServicesFormset(queryset=PriceTariffServices.objects.none(), prefix='price')
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        self.object = None
        qs_tariff = PriceTariffServices.objects.filter(tariff_id=self.request.GET.get('id'))
        tariff_form = TariffForm(self.request.POST)
        price_formset = PriceTariffServicesFormset(self.request.POST or None, queryset=PriceTariffServices.objects.none(),
                                                   prefix='price', initial=[{'services': tar.services, 'price': tar.price,
                                                    'unit': tar.services.unit} for tar in qs_tariff])

        if all([tariff_form.is_valid(), price_formset.is_valid()]):
            return self.form_valid(tariff_form, price_formset)
        else:
            return self.form_invalid(tariff_form, price_formset)

    def form_valid(self, tariff_form, price_formset):
        print(self.request.POST)
        tariff_form.save()
        price_formset.save(commit=False)

        for form in price_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.tariff = tariff_form.instance
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(tariff_form, price_formset)
        for form in price_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, tariff_form, price_formset, **kwargs):
        print(tariff_form.errors)
        print(price_formset.errors)

        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(tariff_form=tariff_form, price_formset=price_formset))



class TariffUpdate(UpdateView):
    model = Tariff
    template_name = 'tariff_update.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariffs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tariff'] = TariffForm(instance=get_object_or_404(Tariff, id=self.get_object().pk))
        context['price_formset'] = PriceTariffServicesFormset(queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                                                              prefix='price')
        return context

    def post(self, *args, **kwargs):
        self.object = None
        tariff_form = TariffForm(self.request.POST, self.request.FILES, instance=get_object_or_404(Tariff, id=self.get_object().pk))
        price_formset = PriceTariffServicesFormset(self.request.POST or None,
                                                   queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                                                   prefix='price')

        if all([tariff_form.is_valid(), price_formset.is_valid()]):
            return self.form_valid(tariff_form, price_formset)
        else:
            return self.form_invalid(tariff_form, price_formset)

    def form_valid(self, tariff_form, price_formset):
        print(self.request.POST)
        tariff_form.save()
        price_formset.save(commit=False)
        for form in price_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.tariff = tariff_form.instance
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(tariff_form, price_formset)
        for form in price_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, tariff_form, price_formset, **kwargs):
        print(tariff_form.errors)
        print(price_formset.errors)

        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(tariff_form=tariff_form, price_formset=price_formset))



class Requisite(CreateView):
    model = Requisite
    template_name = 'requisite.html'
    form_class = RequisiteForm
    success_url = reverse_lazy('requisite')
    inst = get_object_or_404(Requisite, id=1)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RequisiteForm(instance=self.inst)
        return context

    def post(self, *args, **kwargs):
        self.object = None
        form = RequisiteForm(self.request.POST or None, instance=self.inst)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        print(form.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(form=form))


class ItemList(ListView):
    model = Item
    template_name = 'items_list.html'


class ItemCreate(CreateView):
    model = Item
    template_name = 'item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('items')


class ItemUpdate(UpdateView):
    model = Item
    template_name = 'item_update.html'
    form_class = ItemForm
    success_url = reverse_lazy('items')


class MeterList(ListView):
    model = MeterReading
    template_name = 'meter_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        meter_readings = MeterReading.objects.all()
        meters = Services.objects.filter(show=True)

        houses = House.objects.all()
        if self.request.GET.get('filter-number') == '1':
            meter_readings = meter_readings.order_by('-apartment__number')
        if self.request.GET.get('filter-number') == '0':
            meter_readings = meter_readings.order_by('apartment__number')
        if self.request.GET.get('house'):
            meter_readings = meter_readings.filter(apartment__section__house=self.request.GET.get('house'))
            sections = Section.objects.filter(house=self.request.GET.get('house'))
            context['sections'] = sections
        if self.request.GET.get('section'):
            meter_readings = meter_readings.filter(apartment__section=self.request.GET.get('section'))
        if self.request.GET.get('input_number'):
            meter_readings = meter_readings.filter(apartment__number=self.request.GET.get('input_number'))
        if self.request.GET.get('meter'):
            meter_readings = meter_readings.filter(meter_id=self.request.GET.get('meter'))

        paginator = Paginator(meter_readings, 10)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            meter_readings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            meter_readings = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            meter_readings = paginator.page(paginator.num_pages)

        context['meters'] = meters
        context['houses'] = houses
        context['meter_readings'] = meter_readings
        context['page'] = page
        return context

class MeterApartmentList(ListView):
    model = MeterReading
    template_name = 'meter_apartment_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('apartment_id') and self.request.GET.get('service_id'):
            meter_readings = MeterReading.objects.filter(apartment_id=self.request.GET.get('apartment_id'),
                                                         meter_id=self.request.GET.get('service_id'))
            meters = Services.objects.filter(show=True, id=self.request.GET.get('service_id'))
            houses = House.objects.get(apartment=self.request.GET.get('apartment_id'))
        elif self.request.GET.get('apartment_id'):
            meter_readings = MeterReading.objects.filter(apartment_id=self.request.GET.get('apartment_id'))
            meters = Services.objects.filter(show=True)
        else:
            meter_readings = MeterReading.objects.all()
            meters = Services.objects.filter(show=True)
        sections = Section.objects.all()
        houses = House.objects.all()
        print(self.request.GET)
        if self.request.GET.get('number'):
            meter_readings = meter_readings.filter(number=self.request.GET.get('number'))
        if self.request.GET.get('status'):
            meter_readings = meter_readings.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('section'):
            meter_readings = meter_readings.filter(apartment__section=self.request.GET.get('section'))
        if self.request.GET.get('input_date'):
            date = self.request.GET.get('input_date')
            meter_readings = meter_readings.filter(date__range=[date.split(' ')[0], date.split(' ')[1]])
        if self.request.GET.get('meter'):
            meter_readings = meter_readings.filter(meter_id=self.request.GET.get('meter'))
        if self.request.GET.get('filter-date') == '0':
            meter_readings = meter_readings.order_by('date')
        if self.request.GET.get('filter-date') == '1':
            meter_readings = meter_readings.order_by('-date')

        paginator = Paginator(meter_readings, 10)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            meter_readings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            meter_readings = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            meter_readings = paginator.page(paginator.num_pages)

        context['meters'] = meters
        context['houses'] = houses
        context['section'] = sections
        context['meter_readings'] = meter_readings
        context['page'] = page
        return context




class MeterCreate(CreateView):
    model = MeterReading
    template_name = 'meter_create.html'
    form_class = MeterForm
    success_url = reverse_lazy('meter_list')




class MeterDetail(DetailView):
    model = MeterReading
    template_name = 'meter_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        houses = House.objects.all()
        context['houses'] = houses
        return context



class MeterUpdate(UpdateView):
    model = MeterReading
    template_name = 'meter_update.html'
    form_class = MeterForm
    success_url = reverse_lazy('meter_list')


def item_delete(request, pk):
    item = get_object_or_404(Item, id=pk)
    item.delete()
    return redirect('items')


def tariff_delete(request, pk):
    tariff = get_object_or_404(Tariff, id=pk)
    try:
        tariff.delete()
    except:
        messages.error(request, "Вы не можете удалить этот тариф, он используеться")

    return redirect('tariffs')

def meter_delete(request, pk):
    meter = get_object_or_404(MeterReading, id=pk)
    meter.delete()
    return redirect('meter_list')

def show_unit_service(request):
    # if request.is_ajax():
    service_id = request.GET.get('service_id')

    unit_name = Services.objects.filter(id=service_id).values('unit__name')
    print(unit_name)
    response = {
        'services_price': list(unit_name)
    }
    return JsonResponse(response, status=200)


def select_field(request):
    response = {}
    if request.GET.get('house_field'):
        house = House.objects.get(pk=request.GET.get('house_field'))
        section_house = house.section_set.all().values('id', 'name')
        apart_house = Apartment.objects.filter(section__house=house).values('id', 'number')
        print(section_house)
        print(apart_house)
        response = {
            'section_data': list(section_house),
            'apart_data': list(apart_house)
        }
        return JsonResponse(response, status=200)
    elif request.GET.get('section_field'):
        print(request.GET.get('section_field'))
        apart_house = Apartment.objects.filter(section__id=request.GET.get('section_field')).values('id', 'number')
        response = {
            'apartament_data': list(apart_house)
        }
        return JsonResponse(response, status=200)
    elif request.GET.get('index_apart'):
        # print(request.GET.get('section_field'))
        house_data = House.objects.filter(sections__apartment=request.GET.get('index_apart')).values('id', 'name')
        apart_data = Apartment.objects.filter(id=request.GET.get('index_apart')).values('id', 'number', 'section')
        meter_data = Services.objects.filter(id=request.GET.get('index_meter')).values('id', 'main')
        number = MeterReading.objects.filter(apartment_id=request.GET.get('index_apart')).values('id', 'number')
        all_apart = Apartment.objects.all().values('id', 'number', 'section')

        response = {
            'all_apart': list(all_apart),
            'number': list(number),
            'apartment_data': list(apart_data),
            'house_data': list(house_data),
            'meter_data': list(meter_data)
        }
        return JsonResponse(response, status=200)
    elif request.GET.get('update_id'):
        print(request.GET.get('update_id'))
        house_data = House.objects.filter(sections__apartment__meterreading=request.GET.get('update_id')).values('id', 'name')
        apart_house = Apartment.objects.filter(section__apartment__meterreading=request.GET.get('update_id')).values('id', 'number')
        all_apart = Apartment.objects.all().values('id', 'number', 'section')
        print(apart_house)
        response = {
            'house_data': list(house_data),
            'all_apart': list(all_apart),
            'apartment_data': list(apart_house)
        }
        return JsonResponse(response, status=200)
    else:
        return JsonResponse(response, status=200)



