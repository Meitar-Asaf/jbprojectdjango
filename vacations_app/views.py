from vacations_app.models import Vacation, Likes
from .froms import VacationForm, CountryForm, UpdateVacationForm

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from typing import Dict, Any
from django.contrib import messages
from django.forms import BaseForm
from django.contrib.auth.decorators import login_required

class StaffuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method to check if the user is a staff member.
        
        This method ensures that only staff members are allowed to access 
        this view. If the user is not a staff member, it returns an 
        HttpResponseForbidden.
        """
        # Check if the user is a staff member
        if not request.user.is_staff:
            # Deny access to non-staff members
            return HttpResponseForbidden("You are not allowed to access this page.")
        
        # Proceed with the standard dispatch method for staff members
        return super().dispatch(request, *args, **kwargs)
class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    model = Vacation
    context_object_name = 'vacations'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a 'liked' attribute to each vacation in the context
        indicating whether the current user has liked it or not.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vacations = context['vacations']
        context["today"] = datetime.now().date()
        for vacation in vacations:
            vacation.liked = vacation.likes.filter(user=user).exists()
        return context

class UpdateVacationView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    template_name = 'add_vacation.html'
    form_class = UpdateVacationForm
    model = Vacation
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Save the form and add a success message to the request.
        """
        messages.success(self.request, "Vacation updated successfully")
        return super().form_valid(form)

class CreateVacationView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    template_name = 'add_vacation.html'
    form_class = VacationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Save the form and add a success message to the request.
        """
        messages.success(self.request, "Vacation added successfully")
        return super().form_valid(form)

class DeleteVacationView(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Vacation
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Save the form and add a success message to the request.
        """
        messages.success(self.request, "Vacation deleted successfully")
        return super().form_valid(form)
@login_required
def unlike_vacation(request: HttpRequest) -> HttpResponse:
    
    
    """
    Remove a like from a vacation.

    This view is used to unlike a vacation. It requires a POST request with a
    'vacation_id' parameter. If the user is an admin, it returns an
    HttpResponseForbidden with a message saying that admins are not allowed to
    do this. If the user has not liked the vacation yet, it returns an
    HttpResponseForbidden with a message saying that the user hasn't liked the
    vacation yet. Otherwise, it removes the like from the database and returns a
    redirect to the home page.

    :param request: The request object.
    :return: An HttpResponse object.
    """
    if request.user.is_staff:
        return HttpResponseForbidden("Admins are not allowed to do this.")
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    like = Likes.objects.filter(vacation=vacation, user=request.user)
    if not like:
        return HttpResponseForbidden("You haven't liked this vacation yet.")
    like.delete()
    return redirect('home')
@login_required
def like_vacation(request: HttpRequest) -> HttpResponse:
    """
    Like a vacation. This view is supposed to be called via a POST request with
    a 'vacation_id' parameter. It creates a like in the database and redirects
    to the home page.

    If the user is a staff member, it returns a 403 Forbidden response.
    """
    if request.user.is_staff:
        return HttpResponseForbidden("Admins are not allowed to do this.")
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    like = Likes.objects.filter(vacation=vacation, user=request.user)
    if like:
        return HttpResponseForbidden("You have already liked this vacation.")
    Likes.objects.create(vacation=vacation, user=request.user)
    return redirect('home')
