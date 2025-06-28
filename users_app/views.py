from users_app.forms import UserRegisterForm
from django.shortcuts import render
from django.views.generic.edit import CreateView

# Create your views here.


# class RegisterView(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'register.html'
#     success_url = '/'