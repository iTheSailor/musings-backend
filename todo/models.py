from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    duedate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title