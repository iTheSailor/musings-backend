from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserWatchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    group = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol
    
    class Meta:
        unique_together = ('user', 'symbol')