from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeatherView.as_view(), name='weather'),
    path('saved', views.UserLocationView.as_view(), name='weatherSaved'),
]