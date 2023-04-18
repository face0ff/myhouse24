
from django.contrib.auth.models import User
from django.forms import ModelForm, modelformset_factory, Textarea, FileInput, CheckboxInput, CharField, TextInput
from django import forms

from house_app.models import House, Apartment, Section
from .models import *


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


ServicesFormSet = modelformset_factory(model=Services, form=ServicesForm, extra=0, can_delete=True)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'


UnitFormSet = modelformset_factory(model=Unit, form=UnitForm, extra=0, can_delete=True)


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'

class PriceTariffServicesForm(forms.ModelForm):

    currency = forms.CharField(required=False, initial='грн',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    unit = forms.CharField(required=False, initial='Выберите...',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    def __init__(self, *args, **kwargs):
        super(PriceTariffServicesForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['unit'].initial = kwargs.get('instance').services.unit.name

    class Meta:
        model = PriceTariffServices
        exclude = ['tariff']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'services': forms.Select(attrs={'class': 'form-control',
                                            'onchange': "selectServices(this)"})
        }


PriceTariffServicesFormset = modelformset_factory(model=PriceTariffServices, form=PriceTariffServicesForm, extra=0, can_delete=True)


class RequisiteForm(forms.ModelForm):
    class Meta:
        model = Requisite
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class MeterForm(forms.ModelForm):
    house = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'house_field'})
    )
    section = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'section_field'}),
        queryset=Section.objects.all()
    )
    apartment = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'apartment_field'}),
        queryset=Apartment.objects.all()
    )
    class Meta:
        model = MeterReading
        fields = ('number', 'date', 'apartment', 'meter', 'status', 'expense')
        exclude = ['house', 'section']

    def __init__(self, *args, **kwargs):
        super(MeterForm, self).__init__(*args, **kwargs)
        self.fields['house'].choices = [('', 'Выберите значение...')] + [(item.id, item.name) for item in House.objects.all()]
        self.fields['section'].choices = [('', 'Выберите значение...')]
        self.fields['apartment'].choices = [('', 'Выберите значение...')]
        self.fields['meter'].empty_label = 'Выберите значение...'
        self.fields['meter'].queryset = Services.objects.filter(show=True)
        self.fields['number'].error_messages = {'unique': 'Такой номер уже существует'}

    def clean_apartment(self):
        return Apartment.objects.get(pk=self.cleaned_data['apartment'].id)

    # def save(self, commit=True):
    #     meter = super().save(commit=False)
    #     apartment = self.cleaned_data['apartment']
    #     meter.apartment = apartment
    #     if commit:
    #         meter.save()
    #     return meter

