from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name', required= True)
    last_name = forms.CharField(max_length=30, label='Last Name', required= True)
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        """
        Save the user instance. Use the ``commit`` kwarg to enable/disable
        saving the user to the database. This is useful if you want to add
        additional data to the user (e.g. a profile) before saving.
        """
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        """
        Overwrite the default init method to remove the help_text attribute
        of password1 and password2 fields. This is because the default help_text
        is too long and we don't want to display it in the form.
        """
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
        
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1', 'password2']
    def clean_email(self):
        """
        Cleans the email field by checking if the email already exists in the database.
        If it does, a forms.ValidationError is raised with the message "Email already exists".
        Otherwise, the email is returned as is.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


    


