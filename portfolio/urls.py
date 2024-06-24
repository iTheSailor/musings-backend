from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortfolioItemView, name='portfolio'),
    path('create', views.PortfolioItemCreate, name='portfolioCreate'),
    path('update/<int:pk>', views.PortfolioItemUpdate, name='portfolioUpdate'),
    path('delete/<int:id>', views.PortfolioItemDelete, name='portfolioDelete'),
]