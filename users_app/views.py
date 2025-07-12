from users_app.forms import UserRegisterForm,UserLoginForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from typing import Dict, Any

# Create your views here.


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = '/'
    def get_context_data(self, **kwargs:Dict[str, Any]) -> Dict[str, Any]:
    
        """
        Extend the context data with an additional key-value pair indicating
        the form type as 'register'. This is used to differentiate the context
        for the registration view.
        """

        context = super().get_context_data(**kwargs)
        context['form_type'] = 'signup'
        return context

class LoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = '/'

    def get_context_data(self, **kwargs:Dict[str, Any]) -> Dict[str, Any]:
        """
        Extend the context data with an additional key-value pair indicating
        the form type as 'login'. This is used to differentiate the context
        for the login view.
        """
        
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'login'
        return context

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')