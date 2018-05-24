from django import forms
from .models import Driver, Vehicle
from django.forms import ModelForm

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ["name", "number"]

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ["name", "surname"]

class TravelForm(forms.Form):
    filled_date = forms.DateField(widget=forms.SelectDateWidget())
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        empty_label="(Nothing)"
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        empty_label="(Nothing)"
    )
    odometer_before = forms.IntegerField()
    odometer_after = forms.IntegerField()
    fuel_given = forms.FloatField()
    fuel_before = forms.FloatField()
    fuel_after = forms.FloatField()

