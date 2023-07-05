from django import forms
from .models import Check, InOut

class ChecksForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = '__all__'