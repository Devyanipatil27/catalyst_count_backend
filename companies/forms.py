# companies/forms.py
from django import forms


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')
