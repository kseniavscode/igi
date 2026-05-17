from django import forms
from django.contrib.auth.models import User
from .models import Client 
from datetime import date
import re


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    phone = forms.CharField(label="Phone +375(XX)XXX-XX-XX")
    
    birth_date = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    city = forms.ChoiceField(
        choices=Client.CITY_CHOICES,
        label="City",
        initial='Minsk'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Street, house, flat...'}), 
        required=False,
        label="Delivery Address")
    


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_birth_date(self):
        birth = self.cleaned_data.get('birth_date')
        today = date.today()

        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age < 18:
            raise forms.ValidationError("You must be 18+ years old.")
        return birth
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r"^\+375\((25|29|33|44)\)\d{3}\-\d{2}-\d{2}$", phone):
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 7:
            raise forms.ValidationError("Phone number is too short.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
