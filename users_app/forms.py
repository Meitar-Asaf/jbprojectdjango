from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Optional.', label='First Name', required= True)
    last_name = forms.CharField(max_length=30, help_text='Optional.', label='Last Name', required= True)
    email = forms.EmailField(required=True)



    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    

