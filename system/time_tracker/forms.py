from django import forms
from .models import Check, InOut

class ChecksForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('qr_code',)