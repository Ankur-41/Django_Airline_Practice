from django import forms
from .models import Flight,Airport,Passenger

class FlightDetails(forms.Form):
    origin_code = forms.CharField(max_length=3)
    origin_city = forms.CharField(max_length=32)
    destination_code = forms.CharField(max_length=3)
    destination_city = forms.CharField(max_length=32)
    duration = forms.IntegerField()

    def clean_origin_code(self):
        return self.cleaned_data['origin_code'].upper()

    def clean_destination_code(self):
        return self.cleaned_data['destination_code'].upper()

    def clean_origin_city(self):
        return self.cleaned_data['origin_city'].title()

    def clean_destination_city(self):
        return self.cleaned_data['destination_city'].title()
    

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name','last_name','flights']
        

    
class SearchDetails(forms.Form):
    flight_id = forms.IntegerField()