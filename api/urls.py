from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('sudoku/', include('sudoku.urls')),
    path('weather/', include('weather.urls')),
    path('todo/', include('todo.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('finance/', include('finance.urls')),
]

router = routers.DefaultRouter()

urlpatterns += router.urls
