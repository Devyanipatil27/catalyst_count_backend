# companies/forms.py
from django import forms
from .models import CompanyData

# class UploadCSVForm(forms.Form):
#     csv_file = forms.FileField(label='csv_file')


class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = ['name', 'csv_file']
