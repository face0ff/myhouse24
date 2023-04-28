import re
from django.contrib.auth import logout, authenticate, login
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, DateInput, TextInput, EmailInput

from house_app.models import House
from user_app.models import Role, UserProfile


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)

class UserForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'status', 'role', 'telephone', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.status = 'new'
        if commit:
            user.save()
        return user



class UserUpdateForm(UserChangeForm):
    password1 = forms.CharField(required=False, label='Пароль')
    password2 = forms.CharField(required=False, label='Повторить пароль')
    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'telephone', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 and not password2:
            pass
        else:
            if password1 and password2 and password1 != password2:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
            return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.cleaned_data['password1']:
            if commit:
                user.save(update_fields = ['email', 'first_name', 'last_name', 'telephone'])
            return user
        else:
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()

            print('celery')
            return user


class OwnerForm(UserCreationForm):


    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'patronymic', 'birth_date', 'telephone', 'viber', 'telegram', 'email', 'status', 'user_id', 'notes', 'password1', 'password2']

        widgets = {
            'user_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 7, 'class': 'form-control', 'placeholder': 'Текст сообщения:'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),


        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.status = 'new'
        if commit:
            user.save()
        return user


class OwnerUpdateForm(UserCreationForm):
    password1 = forms.CharField(required=False, label='Пароль')
    password2 = forms.CharField(required=False, label='Повторить пароль')

    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'patronymic', 'birth_date', 'telephone', 'viber', 'telegram',
                  'email', 'status', 'user_id', 'notes', 'password1', 'password2']

        widgets = {
            'user_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 7, 'class': 'form-control', 'placeholder': 'Текст сообщения:'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),

        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):

        user = super().save(commit=False)
        if not self.cleaned_data['password1']:
            if commit:
                user.save(update_fields=['avatar', 'first_name', 'last_name', 'patronymic', 'birth_date', 'telephone', 'viber', 'telegram',
                  'email', 'status', 'user_id', 'notes'])
            return user
        else:
            user.set_password(self.cleaned_data['password1'])
            user.is_active = True
            user.status = 'new'
            if commit:
                user.save()
            return user


class InviteForm(forms.Form):
    telephone = forms.CharField(required=False, label='Телефон',
                                widget=TextInput(attrs={'class': 'form-control',
                                                        'placeholder': '+380(099) 999-99-99'}))
    email = forms.CharField(label='E-mail', widget=EmailInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'email@example.com'}))