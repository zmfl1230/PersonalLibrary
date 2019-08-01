# forms.py
from django import forms
from .models import *


class AuthorimageForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'image']
