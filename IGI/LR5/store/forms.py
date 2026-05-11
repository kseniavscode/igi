from django import forms
from django.contrib.auth.models import User
from .models import Client 


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    phone = forms.CharField(label="Phone +375(XX)XXX-XX-XX")
    age = forms.IntegerField(label="Age (18+)")
    address = forms.CharField(widget=forms.Textarea, required=False)


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("You must be 18+ years old.")
        return age

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
