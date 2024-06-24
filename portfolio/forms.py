# forms.py

from django import forms
from .models import PortfolioItem

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'image', 'technology', 'backend_features', 'frontend_features']
