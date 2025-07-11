from vacations_app.models import Vacation, Country
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date

        
        
class VacationForm(forms.ModelForm):
    

    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True, label='Country')
    start_date = forms.DateField(widget = forms.DateInput(attrs={'min': date.today().isoformat(), "type": 'date'}), required=True, label='Start Date')
    end_date = forms.DateField(widget = forms.DateInput(attrs={'min': date.today().isoformat(), "type": 'date'}), required=True, label='End Date')
    price = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0, message="Price must be greater than 0"), MaxValueValidator(10000, message="Price must be less than 10000")], required=True, label='Price', widget=forms.NumberInput(attrs={'type': 'number'}))
    image = forms.ImageField(required=True, label='Image', widget=forms.FileInput(attrs={'type': 'file'}))

                

    class Meta:
        model = Vacation
        fields = ['country', 'description', 'start_date', 'end_date', 'price', 'image']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = None

class UpdateVacationForm(VacationForm):
    image = forms.ImageField(required=False, label='Image', widget=forms.FileInput(attrs={'type': 'file', "class": "overlay-btn"}))
    start_date = forms.DateField(widget = forms.DateInput(attrs={"type": 'date'}), required=True, label='Start Date')
    end_date = forms.DateField(widget = forms.DateInput(attrs={"type": 'date'}), required=True, label='End Date')
    
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_name']