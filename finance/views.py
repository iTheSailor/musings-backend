from django.shortcuts import render
from django.http import JsonResponse
from .models import UserWatchlist
import requests
import os
from icecream import ic
from collections import OrderedDict
import yfinance as yf
from .forms import UserWatchlistForm
from django.contrib.auth.models import User
import json
import pandas as pd

# Create your views here.
def get_stock(request):
    data = {}
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        stock = yf.Ticker(symbol)
        user = request.GET.get('user')
        user_watchlist = UserWatchlist.objects.filter(user=user)
        watchlist = [watch.symbol for watch in user_watchlist]
        data = {
            'symbol': stock.info,
            'watchlist': watchlist
        }
    return JsonResponse(data)

def get_watchlist(request):
    data = {}
    if request.method == 'GET':
        user = request.GET.get('user')
        user = User.objects.get(id=user)
        watchlist = UserWatchlist.objects.filter(user=user)
        symbols = [watch.symbol for watch in watchlist]
        ic(symbols, type(symbols))
        data = {
            'symbols': symbols,
            'success': True
        }
    return JsonResponse(data)

def add_watchlist(request):
    data = {}
    if request.method == 'POST':
        form = UserWatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save()
            data = {'message': 'Watchlist added successfully', 'success': True}
        else:
            data = form.errors

    return JsonResponse(data)

def remove_watchlist(request):
    data = {}
    if request.method == 'POST':
        ic(request.POST.dict())
        data = request.POST.dict()
        user = User.objects.get(id=data['user'])
        symbol = data['symbol']
        watchlist = UserWatchlist.objects.filter(user=user, symbol=symbol)
        watchlist.delete()
        data = {'message': 'Watchlist removed successfully', 'success': True}
    return JsonResponse(data)

def get_watchlist_group(request):
    data = {}
    if request.method == 'GET':
        user = request.user
        group = request.GET.get('group')
        watchlist = UserWatchlist.objects.filter(user=user, group=group)
        data = [watch.symbol for watch in watchlist]
    return JsonResponse(data)

def get_full_stock(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        range = request.GET.get('range')
        interval = request.GET.get('interval')
        stock = yf.Ticker(symbol)
        info = stock.info
        news = stock.news
        history = stock.history(period=range, interval=interval)
        history_dict = {}
        for date, data in history.iterrows():
            history_dict[str(date)] = data.to_dict()
        ic(type(history), type(stock.info), type(stock.news))
        
        data = {
            'info': info,
            'news': news,
            'history': history_dict
        }



    return JsonResponse(data)


