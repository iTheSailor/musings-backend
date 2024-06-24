from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer
import json
from icecream import ic
from .forms import PortfolioItemForm
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
@csrf_exempt
def PortfolioItemCreate(request):
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_item = form.save()
            return JsonResponse({'id': portfolio_item.id}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@api_view(['PUT'])
def PortfolioItemUpdate(request, pk):
    try:
        portfolio_item = PortfolioItem.objects.get(pk=pk)
    except PortfolioItem.DoesNotExist:
        return JsonResponse({'error': 'PortfolioItem not found'}, status=404)
    
    if request.method == 'PUT':
        parser_classes = (MultiPartParser, FormParser)
        data = request.data
        files = request.FILES
        form = PortfolioItemForm(data, files, instance=portfolio_item)
        if form.is_valid():
            portfolio_item = form.save()
            return JsonResponse({'id': portfolio_item.id}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def PortfolioItemView(request):
    context = {'request': request}
    items = PortfolioItem.objects.all()
    serializer = PortfolioItemSerializer(items, many=True, context=context)
    return JsonResponse(serializer.data, safe=False)

def SinglePortfolioItem(request, id):
    item = PortfolioItem.objects.get(id=id)
    serializer = PortfolioItemSerializer(item)
    return JsonResponse(serializer.data, safe=False)

def PortfolioItemDelete(request, id):
    item = PortfolioItem.objects.get(id=id)
    item.delete()
    return JsonResponse({'status': 'success'})