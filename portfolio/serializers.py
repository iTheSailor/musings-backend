from rest_framework import serializers
from .models import PortfolioItem

class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ['id', 'title', 'description', 'image', 'technology','backend_features', 'frontend_features', 'created', 'updated']
        depth = 1