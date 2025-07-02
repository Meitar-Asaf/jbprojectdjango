from vacations_app.models import Vacation,Likes
from .froms import VacationForm, CountryForm

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import StaffuserRequiredMixin

class HomeView(LoginRequiredMixin,ListView):
    template_name = 'home.html'
    model = Vacation
    context_object_name = 'vacations'
    def get_context_data(self, **kwargs):
        """
        Add a 'liked' attribute to each vacation in the context
        indicating whether the current user has liked it or not.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vacations = context['vacations']
        for vacation in vacations:
            vacation.liked = vacation.likes.filter(user=user).exists()
        return context
    
class CreateVacationView(LoginRequiredMixin,StaffuserRequiredMixin,CreateView):
    template_name = 'add_vacation.html'
    form_class = VacationForm

def unlike_vacation(request):
    """
    Unlike a vacation. This view is supposed to be called via a POST request with
    a 'vacation_id' parameter. It deletes the like from the database and redirects
    to the home page.
    """
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    Likes.objects.filter(vacation=vacation,user = request.user).delete()
    return redirect('home')

def like_vacation(request):
    """
    Like a vacation. This view is supposed to be called via a POST request with
    a 'vacation_id' parameter. It creates a like in the database and redirects
    to the home page.
    """
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    Likes.objects.create(vacation=vacation, user=request.user)
    return redirect('home')
    