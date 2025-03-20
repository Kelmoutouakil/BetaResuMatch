from django import forms
from django.core.exceptions import ValidationError

class UserRegistationForm(forms.Form):
    first_name= forms.CharField(max_length=20,required=True)
    last_name= forms.CharField(max_length=20,required=True)
    email= forms.EmailField(required=True)
    password1= forms.CharField(widget=forms.PasswordInput,required=True)
    password2= forms.CharField(widget=forms.PasswordInput,required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password1