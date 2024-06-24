from django import forms
from .models import UserWatchlist

class UserWatchlistForm(forms.ModelForm):
    class Meta:
        model = UserWatchlist
        fields = ['symbol', 'group', 'user']