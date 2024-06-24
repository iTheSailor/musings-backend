from django.db import models

# Create your models here.
class PortfolioItem(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    backend_features = models.TextField(blank=True)
    frontend_features = models.TextField(blank=True)
    technology = models.CharField(max_length=256)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title