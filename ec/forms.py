from django import forms
from .models import ChoiceLocation

class LocationRegisterForm(forms.ModelForm):

    class Meta:
        model = ChoiceLocation
        fields = '__all__'
