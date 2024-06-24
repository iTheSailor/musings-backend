from django.urls import path
from . import views

urlpatterns = [
    path('get_stock', views.get_stock, name='get_stock'),
    path('get_watchlist', views.get_watchlist, name='get_watchlist'),
    path('add_watchlist', views.add_watchlist, name='add_watchlist'),
    path('remove_watchlist', views.remove_watchlist, name='remove_watchlist'),
    path('get_full_stock', views.get_full_stock, name='get_full_stock'),
]