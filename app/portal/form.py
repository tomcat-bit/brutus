from django import forms


class CSVForm(forms.Form):
    docfile = forms.FileField(label='Select a file')