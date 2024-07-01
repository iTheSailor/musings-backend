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

class UserPlayWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wallet_name
    
    class Meta:
        unique_together = ('user', 'wallet_name')

class UserPlayStock(models.Model):
    wallet = models.ForeignKey(UserPlayWallet, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    bought_price = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    class Meta:
        unique_together = ('wallet', 'symbol')
class UserWalletHistory(models.Model):
    wallet = models.ForeignKey(UserPlayWallet, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    stocks_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wallet.wallet_name
    
    class Meta:
        ordering = ['-created_at']


class UserStockHistory(models.Model):
    wallet = models.ForeignKey(UserPlayWallet, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    bought_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_spending = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_sale_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    change_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.symbol

    class Meta:
        ordering = ['-created_at']

