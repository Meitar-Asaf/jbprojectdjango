from django.urls import path
from .views import *


urlpatterns = [path('', HomeView.as_view(), name='home'),
    path('like/', like_vacation, name='like_vacation'),
    path('unlike/', unlike_vacation, name='unlike_vacation'),
    ]