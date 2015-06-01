from django.forms import ModelForm
from django import forms
from core.models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'description', 'interval', 'interval_options', 'arguments', 'active']

    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        INTERVAL_CHOICES = (
            ('Y', 'Yearly'),
            ('M', 'Monthly'),
            ('W', 'Weekly'),
            ('D', 'Daily'),
            ('H', 'Hourly'),
            ('m', 'Minutely'),
        )

        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['description'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['interval'].widget = forms.Select(attrs={'id': 'interval-select', 'class': 'select2-container form-control input-xlarge'})
        self.fields['interval'].choices = INTERVAL_CHOICES
        self.fields['interval_options'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['arguments'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['arguments'].required = False
        self.fields['file'].widget = forms.FileInput(attrs={'class': 'input', 'id': 'fileinput', 'name': 'fileinput'})
