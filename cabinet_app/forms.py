
from django.forms import TimeInput, DateInput
from house_app.models import *
from django import forms


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
    # def save(self, commit=True):
    #     request = super().save(commit=False)
    #     if commit:
    #         request.status = 'new'
    #     return request