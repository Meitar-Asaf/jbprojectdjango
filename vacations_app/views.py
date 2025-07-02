from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView
from vacations_app.models import Vacation,Likes
from django.contrib.auth.mixins import LoginRequiredMixin

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

def unlike_vacation(request):
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    Likes.objects.filter(vacation=vacation,user = request.user).delete()
    return render(request, 'home.html')

def like_vacation(request):
    vacation = Vacation.objects.get(id=request.POST['vacation_id'])
    Likes.objects.create(vacation=vacation, user=request.user)
    return render(HomeView, 'home.html')