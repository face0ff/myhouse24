from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import get_image_dimensions
from django.db.models import Q
from django.forms import ModelForm, modelformset_factory, Textarea, Select, NumberInput, CharField, TextInput, \
    inlineformset_factory, formset_factory, TimeInput, DateInput

from django import forms

from services_app.models import Unit
from user_app.models import Role
from .models import *


class UserHouseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']
        exclude = ['role']

    user = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'onchange': "selectUser(this)"}),
        queryset=UserProfile.objects.all(),
        empty_label="Выберите...")

    role = forms.CharField(required=False, initial='Выберите...',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    # def clean_role(self):
    #     print(self.cleaned_data)
    #     data = self.cleaned_data['role']
    #     try:
    #         return Role.objects.get(roles=data)
    #     except ObjectDoesNotExist:
    #         raise forms.ValidationError("Роль не найдена")
    #     return data


UserFormSet = formset_factory(form=UserHouseForm, extra=0, can_delete=True)


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ('house',)


SectionFormSet = modelformset_factory(Section, form=SectionForm, extra=0, can_delete=True)


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        exclude = ('house',)


FloorFormSet = modelformset_factory(Floor, form=FloorForm, extra=0, can_delete=True)


class ApartmentForm(forms.ModelForm):
    account_number = forms.IntegerField(required=False, label='Номер лицевого счета',
                                        widget=NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Apartment
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'tariff': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].empty_label = 'Выберите дом'
        self.fields['tariff'].empty_label = 'Выберите...'
        self.fields['owner'].empty_label = 'Выберите...'
        self.fields['section'].empty_label = 'Выберите...'
        if self.instance:
            try:
                self.fields['account_number'].initial = Account.objects.get(apartment=self.instance.id)
                self.fields['section'].queryset = Section.objects.filter(house_id=self.instance.house.id)
                self.fields['floor'].queryset = Floor.objects.filter(house_id=self.instance.house.id)
                self.fields['owner'].queryset = UserProfile.objects.filter(role_id__isnull=True)
            except:
                self.fields['section'].queryset = Section.objects.all()
                self.fields['floor'].queryset = Floor.objects.all()
                self.fields['owner'].queryset = UserProfile.objects.filter(role_id__isnull=True)
        self.fields['floor'].empty_label = 'Выберите...'

    def save(self, commit=True):
        apartment = super().save(commit=False)
        prev_acc = Account.objects.filter(apartment=apartment)
        # if prev_acc:
        #     prev_acc.update(apartment_id='')
        print('111111111111111111111111111')
        print(self.cleaned_data['account_number'])
        if self.cleaned_data['account_number']:
            try:
                prev_acc.update(apartment_id='')
                account = Account.objects.get(number=self.cleaned_data['account_number'])
                print(account)
                account.apartment_id = apartment
                account.save()
                if commit:

                    apartment.save()

            except:
                account = Account.objects.create(number=self.cleaned_data['account_number'])
                if commit:
                    apartment.save()
                    account.apartment_id = apartment
                    account.save()

        else:
            if commit:
                apartment.save()
                return apartment
        return apartment


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = '__all__'
        exclude = ('users',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'image_1': forms.FileInput(attrs={'type': 'file'}),
            'image_2': forms.FileInput(attrs={'type': 'file'}),
            'image_3': forms.FileInput(attrs={'type': 'file'}),
            'image_4': forms.FileInput(attrs={'type': 'file'}),
            'image_5': forms.FileInput(attrs={'type': 'file'}),
        }

    def clean(self):
        images = ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']
        for image in images:
            if self.cleaned_data[image]:
                width, height = get_image_dimensions(self.cleaned_data[image])
                if image == 'image_1':
                    if width != 522 or height != 350:
                        raise forms.ValidationError("Размеры изображения не валидны (522x350)")
                else:
                    if width != 248 or height != 160:
                        raise forms.ValidationError("Размеры изображения не валидны (248x160)")
        return self.cleaned_data


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 7, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type_master': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'apartment': forms.Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control',
                                     'type': 'text'}),
            'time': TimeInput(attrs={'class': 'form-control',
                                     'type': 'text'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.datetime.today().strftime('%d.%m.%Y')
        self.fields['time'].initial = datetime.datetime.today().strftime('%H:%M')
        self.fields['master'].empty_label = 'Выберите...'
        self.fields['master'].queryset = UserProfile.objects.filter(is_staff=False, role__isnull=False)
        self.fields['apartment'].empty_label = 'Выберите...'

    owner = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'onchange': "selectUser(this)"}),
        queryset=UserProfile.objects.filter(role_id__isnull=True),
        empty_label="Выберите..."
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения:'}),
            'text': forms.Textarea(attrs={'rows': 7, 'class': 'form-control', 'placeholder': 'Текст сообщения:'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'apartment': forms.Select(attrs={'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control',
                                     'type': 'text'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].empty_label = 'Всем...'
        self.fields['house'].queryset = House.objects.all()
        self.fields['section'].choices = [('', 'Всем...')]
        self.fields['apartment'].choices = [('', 'Всем...')]
        self.fields['floor'].choices = [('', 'Всем...')]
        self.fields['owner'].empty_label = 'Выберите...'
        self.fields['owner'].queryset = UserProfile.objects.filter(role_id__isnull=True)

    def save(self, commit=True):
        message = super().save(commit=False)
        print(self.cleaned_data)
        if self.cleaned_data['apartment']:
            owner = UserProfile.objects.get(apartment=self.cleaned_data['apartment'])
            message.owner = owner
            message.sender = self.cleaned_data['sender']
            if commit:
                message.save()
            return message
        else:
            if commit:
                message.save()
            return message


class AccountForm(forms.ModelForm):
    owners = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'onchange': "selectUser(this)"}),
        queryset=UserProfile.objects.filter(role_id__isnull=True),
        empty_label="Выберите...")

    houses = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        queryset=House.objects.all(),
        empty_label="Выберите...")

    section = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        queryset=Section.objects.all(),
        empty_label="Выберите...")

    class Meta:
        model = Account
        fields = ['number', 'status', 'apartment', 'owners', 'houses', 'section']

        widgets = {
            'number': NumberInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'apartment': Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.instance.id)
        try:
            if self.instance.id:
                house = House.objects.get(apartment__account=self.instance.id)
                self.fields['houses'].initial = house
                self.fields['section'].queryset = Section.objects.filter(house_id=house.id)
                self.fields['section'].initial = Section.objects.get(apartment__account=self.instance.id)
                self.fields['apartment'].empty_label = 'Выберите...'
                self.fields['apartment'].queryset = Apartment.objects.filter(Q(account=self.instance.id)
                                                                             | Q(account__isnull=True))
                # self.fields['apartment'].initial = Apartment.objects.get(account=self.instance.id)
                # self.fields['apartment'].queryset = Apartment.objects.filter(account__isnull=True)

        except:

            pass


class InvoiceForm(forms.ModelForm):
    houses = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        queryset=House.objects.all(),
        empty_label="Выберите...")

    section = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        queryset=Section.objects.all(),
        empty_label="Выберите...")

    account = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    class Meta:
        model = Invoice
        fields = ['number', 'date', 'apartment', 'done', 'status', 'date_from', 'date_before', 'amount', 'tariff']

        widgets = {
            'number': NumberInput(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control id_date',
                                     'type': 'text'}),
            'date_before': DateInput(attrs={'class': 'form-control id_date',
                                            'type': 'text'}),
            'date_from': DateInput(attrs={'class': 'form-control id_date',
                                          'type': 'text'}),
            'tariff': Select(attrs={'class': 'form-control'}),
            'apartment': Select(attrs={'class': 'form-control'}),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance.id:
                houses = House.objects.get(apartment__invoice=self.instance.id)
                self.fields['houses'].initial = houses
                self.fields['apartment'].empty_label = 'Выберите...'
                self.fields['section'].initial = Section.objects.get(apartment__invoice=self.instance.id)
                self.fields['tariff'].initial = Tariff.objects.filter(apartment__invoice=self.instance.id)
                self.fields['account'].initial = Account.objects.get(apartment__invoice=self.instance.id)
        except:
            pass
        self.fields['tariff'].empty_label = 'Выберите...'
        self.fields['apartment'].empty_label = 'Выберите...'
        self.fields['section'].empty_label = 'Выберите...'


class InvoiceServiceForm(ModelForm):
    unit = forms.CharField(required=False,
                                  widget=TextInput(attrs={'class': 'form-control',
                                                       'disabled': 'true'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            print(self.instance.id)
            self.fields['unit'].initial = Unit.objects.get(services__invoiceservice=self.instance.id)
        self.fields['service'].empty_label = 'Выберите...'
        self.fields['unit'].empty_label = 'Выберите услугу'


    class Meta:
        model = InvoiceService
        fields = ['service', 'invoice', 'cost_for_unit', 'expense', 'full_cost']

        widgets = {'service': Select(attrs={'class': 'form-control',
                                            'onchange': 'select_service(this.id)'}),
                   'expense': NumberInput(attrs={'class': 'form-control',
                                                 'onblur': 'select_expense(this.id)'}),
                   'cost_for_unit': NumberInput(attrs={'class': 'form-control',
                                                       'onblur': 'select_cost(this.id)'}),
                   'full_cost': NumberInput(attrs={'class': 'form-control full-cost',
                                                   'readonly': 'true'})}


InvoiceServiceFormSet = modelformset_factory(InvoiceService, form=InvoiceServiceForm, extra=0, can_delete=True)


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = '__all__'

        widgets = {
            'number': NumberInput(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control',
                                     'type': 'text'}),
            'owner': Select(attrs={'class': 'form-control'}),
            'account': Select(attrs={'class': 'form-control'}),
            'item': Select(attrs={'class': 'form-control'}),
            'amount': NumberInput(attrs={'class': 'form-control'}),
            'manager': Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 7, 'class': 'form-control', 'placeholder': 'Текст сообщения:'}),

        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance.id:
        #     print(self.instance.id)
        #     self.fields['unit'].initial = Unit.objects.get(services__invoiceservice=self.instance.id)
        # self.fields['service'].empty_label = 'Выберите...'
        # self.fields['unit'].empty_label = 'Выберите услугу'


        self.fields['owner'].empty_label = 'Выберите...'
        self.fields['owner'].queryset = UserProfile.objects.filter(role_id__isnull=True)
        self.fields['account'].empty_label = 'Выберите...'
        self.fields['item'].empty_label = 'Выберите...'
        self.fields['manager'].initial = user
        self.fields['manager'].queryset = UserProfile.objects.filter(is_staff=True)
        self.fields['manager'].empty_label = 'Выберите...'

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'type': 'file'}),
        }