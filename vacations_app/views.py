from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from vacations_app.models import Vacation

class HomeView(ListView):
    template_name = 'home.html'
    model = Vacation
    context_object_name = 'vacations'

# Create your views here.
