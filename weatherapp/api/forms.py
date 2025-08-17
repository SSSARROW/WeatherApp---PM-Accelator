from django import forms
from .models import WeatherRequest

class WeatherRequestForm(forms.ModelForm):
    class Meta:
        model = WeatherRequest
        fields = ['location_input', 'source', 'lat', 'lon']
