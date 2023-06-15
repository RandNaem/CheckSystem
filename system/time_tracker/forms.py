from django import forms
from .models import Checks

class ChecksForm(forms.ModelForm):
    class Meta:
        model = Checks
        fields = ('qr_code',)
