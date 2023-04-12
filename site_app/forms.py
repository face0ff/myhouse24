from django.forms import ModelForm, modelformset_factory, Textarea, FileInput, CheckboxInput, CharField, TextInput
from django import forms
from .models import *


class SeoForm(ModelForm):
    titles = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    keywords = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'form-control'}))
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Seo
        fields = '__all__'


class MainForm(ModelForm):
    seo = SeoForm()
    class Meta:
        model = Main
        fields = ['header', 'description', 'slider_1', 'slider_2', 'slider_3', 'show_url']

        widgets = {
             "header": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Заголовок"
            }),
            "description": Textarea(attrs={
                'class': 'form-control description',
                'placeholder': "Красткий текст",
                'id': 'id_description'
            }),
            "slider_1": FileInput(attrs={
                'class': 'form-control',
                'onchange': 'download(this)',
                "title": "Добавьте картинку"

            }),
            "slider_2": FileInput(attrs={
                'class': 'form-control',
                'onchange': 'download(this)',
                "title": "Добавьте картинку"

            }),
            "slider_3": FileInput(attrs={
                'class': 'form-control',
                'onchange': 'download(this)',
                "title": "Добавьте картинку"

            }),
            "show_url": CheckboxInput(attrs={

                'type': 'checkbox'
            })
        }

class BlockForm(ModelForm):

    class Meta:
        model = Block
        fields = ['header', 'description', 'image']

        widgets = {
             "header": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Заголовок"
            }),
            "description": Textarea(attrs={
                'class': 'form-control description',
                'placeholder': "Краткий текст",


            }),
            "image": FileInput(attrs={
                'class': 'form-control',
                'onchange': 'download(this)',
                "title": "Добавьте картинку"
            }),
        }


BlockFormSet = modelformset_factory(model=Block, form=BlockForm, extra=0, can_delete=True)


class ContactsForm(ModelForm):
    class Meta:
        model = Contacts
        exclude = ['seo']
        widgets = {
            "phone": TextInput(attrs={
                'class': 'form-control',
                'data-mask': '(000)-000-00-00',
                'placeholder': '(000)-000-00-00'
            })
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = '__all__'
        widgets = {
            "text": TextInput(attrs={
                'class': 'form-control',
            }),

            "files": FileInput(attrs={
                'class': 'form-control',
                'onchange': 'download(this)',
                "title": "Добавить фаил"
            }),
        }


FilesFormSet = modelformset_factory(model=Files, form=FilesForm, extra=0, can_delete=True)


class AditGalleryForm(forms.ModelForm):
    class Meta:
        model = AditGallery
        fields = '__all__'

class InfoForm(ModelForm):
    class Meta:
        model = Info
        exclude = ['seo']
        widgets = {
            "photo": FileInput(attrs={
                'class': 'form-control',

            })
        }
