from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name', required= True)
    last_name = forms.CharField(max_length=30, label='Last Name', required= True)
    email = forms.EmailField(required=True)



    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    


