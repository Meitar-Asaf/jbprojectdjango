from django.urls import path
from .views import HomeView, like_vacation, unlike_vacation, CreateVacationView


urlpatterns = [path('', HomeView.as_view(), name='home'),
    path('like/', like_vacation, name='like_vacation'),
    path('unlike/', unlike_vacation, name='unlike_vacation'),
    path('add/', CreateVacationView.as_view(), name='add_vacation'),
    ]