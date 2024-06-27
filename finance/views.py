from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from icecream import ic
import yfinance as yf
from .forms import UserWatchlistForm
from django.contrib.auth.models import User
import json
import pandas as pd
from icecream import ic

### stock views
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

### watchlist views
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

@csrf_exempt
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

@csrf_exempt
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

### wallet views
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, F, Value as V
from django.db.models.functions import Coalesce

"""
Explanation:
create_wallet: Allows users to create a new wallet with an initial balance of $100,000.
add_stock_to_wallet: Adds stocks to a specified wallet, deducting the total spending from the wallet's balance.
sell_stock_from_wallet: Sells stocks from a specified wallet, updating the wallet balance and recording the transaction history.
get_wallets: Retrieves all wallets for a specified user.
get_wallet_details: Retrieves details of a specified wallet, including the stocks it contains.
get_wallet_history: Retrieves the balance history of a specified wallet.
get_stock_history: Retrieves the stock transaction history for a specified wallet.
"""

@csrf_exempt
def create_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(id=data['user_id'])
        wallet_name = data['wallet_name']
        
        if UserPlayWallet.objects.filter(user=user, wallet_name=wallet_name).exists():
            return JsonResponse({'message': 'Wallet with this name already exists', 'success': False})
        
        wallet = UserPlayWallet.objects.create(user=user, wallet_name=wallet_name)
        UserWalletHistory.objects.create(wallet=wallet, balance=wallet.balance)
        
        return JsonResponse({'message': 'Wallet created successfully', 'wallet_id': wallet.id, 'success': True})
@csrf_exempt
def add_stock_to_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_id = data['wallet_id']
        symbol = data['symbol']
        quantity = int(data['quantity'])
        bought_price = Decimal(data['bought_price'])
        total_spent = quantity * bought_price
        
        wallet = UserPlayWallet.objects.get(id=wallet_id)
        
        if wallet.balance < total_spent:
            return JsonResponse({'message': 'Insufficient balance', 'success': False})
        
        with transaction.atomic():
            wallet.balance -= total_spent
            wallet.save()
            UserPlayStock.objects.create(wallet=wallet, symbol=symbol, quantity=quantity, bought_price=bought_price, current_value=total_spent)
            UserWalletHistory.objects.create(wallet=wallet, balance=wallet.balance)
            UserStockHistory.objects.create(wallet=wallet, symbol=symbol, quantity=quantity, bought_price=bought_price, total_spending=total_spent, current_value=total_spent)
        
        return JsonResponse({'message': 'Stock added to wallet successfully', 'success': True})

@csrf_exempt
def sell_stock_from_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_id = data['wallet_id']
        symbol = data['symbol']
        quantity = int(data['quantity'])
        sold_price = Decimal(data['sold_price'])
        
        wallet = UserPlayWallet.objects.get(id=wallet_id)
        stock = UserPlayStock.objects.filter(wallet=wallet, symbol=symbol).first()
        
        if not stock or stock.quantity < quantity:
            return JsonResponse({'message': 'Insufficient stock quantity', 'success': False})
        
        total_sale_value = quantity * sold_price
        remaining_quantity = stock.quantity - quantity
        change_percentage = ((sold_price - stock.bought_price) / stock.bought_price) * 100
        
        with transaction.atomic():
            if remaining_quantity == 0:
                stock.delete()
            else:
                stock.quantity = remaining_quantity
                stock.current_value = remaining_quantity * stock.bought_price
                stock.save()
            
            wallet.balance += total_sale_value
            wallet.save()
            UserWalletHistory.objects.create(wallet=wallet, balance=wallet.balance)
            UserStockHistory.objects.create(wallet=wallet, symbol=symbol, quantity=quantity, bought_price=stock.bought_price, sold_price=sold_price, total_sale_value=total_sale_value, change_percentage=change_percentage)
        
        return JsonResponse({'message': 'Stock sold from wallet successfully', 'success': True})
@csrf_exempt
def get_wallets(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        wallets = UserPlayWallet.objects.filter(user=user).annotate(
            current_value=F('balance')
        )

        wallets_data = []
        for wallet in wallets:
            wallet_data = {
                'wallet_id': wallet.id,
                'wallet_name': wallet.wallet_name,
                'balance': str(wallet.balance),
                'stocks': [],
            }
            total_stock_value = 0.0
            for stock in wallet.userplaystock_set.all():
                ticker = yf.Ticker(stock.symbol)
                history = ticker.history(period='1d')
                if not history.empty:
                    current_price = float(history.iloc[-1]['Close'])
                    current_value = current_price * stock.quantity
                    total_stock_value += current_value
                    stocks = {
                        'symbol': stock.symbol,
                        'quantity': stock.quantity,
                        'bought_price': str(stock.bought_price),
                        'current_price': str(current_price),
                        'current_value': str(current_value),
                    }
                    wallet_data['stocks'].append(stocks)
                else:
                    print(f"No price data for {stock.symbol}")

            wallet_data['current_value'] = str(float(wallet.balance) + total_stock_value)
            wallets_data.append(wallet_data)
            ic(wallets_data)
        
        return JsonResponse({'wallets': wallets_data, 'success': True})

def get_wallet_details(request):
    if request.method == 'GET':
        wallet_id = request.GET.get('wallet_id')
        wallet = UserPlayWallet.objects.get(id=wallet_id)
        stocks = UserPlayStock.objects.filter(wallet=wallet)
        wallet_data = {
            'wallet_id': wallet.id,
            'wallet_name': wallet.wallet_name,
            'balance': str(wallet.balance),
            'stocks': [],
        }
        total_stock_value = 0.0
        stocks_data = []
        for stock in stocks:
            ticker = yf.Ticker(stock.symbol)
            history = ticker.history(period='1d')
            if not history.empty:
                    current_price = float(history.iloc[-1]['Close'])
                    current_value = current_price * stock.quantity
                    total_stock_value += current_value
                    stock = {
                        'symbol': stock.symbol,
                        'quantity': stock.quantity,
                        'bought_price': str(stock.bought_price),
                        'current_price': str(current_price),
                        'current_value': str(current_value),
                    }
                    stocks_data.append(stock)
            else:
                print(f"No price data for {stock.symbol}")
        
        wallet_data['current_value'] = str(float(wallet.balance) + total_stock_value)
        wallet_data['stocks'] = stocks_data

        return JsonResponse({'wallet': wallet_data, 'success': True})


def get_wallet_history(request):
    if request.method == 'GET':
        wallet_id = request.GET.get('wallet_id')
        history = UserWalletHistory.objects.filter(wallet_id=wallet_id).order_by('-created_at')
        history_data = [{
            'balance': record.balance,
            'created_at': record.created_at
        } for record in history]
        
        return JsonResponse({'history': history_data, 'success': True})

def get_stock_history(request):
    if request.method == 'GET':
        wallet_id = request.GET.get('wallet_id')
        history = UserStockHistory.objects.filter(wallet_id=wallet_id).order_by('-created_at')
        history_data = [{
            'symbol': record.symbol,
            'quantity': record.quantity,
            'bought_price': record.bought_price,
            'sold_price': record.sold_price,
            'total_spending': record.total_spending,
            'current_value': record.current_value,
            'total_sale_value': record.total_sale_value,
            'change_percentage': record.change_percentage,
            'created_at': record.created_at
        } for record in history]
        
        return JsonResponse({'history': history_data, 'success': True})

@csrf_exempt
def rename_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_id = data['wallet_id']
        new_wallet_name = data['new_wallet_name']

        wallet = UserPlayWallet.objects.get(id=wallet_id)
        wallet.wallet_name = new_wallet_name
        wallet.save()

        return JsonResponse({'message': 'Wallet renamed successfully', 'success': True})

@csrf_exempt
def delete_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_id = data['wallet_id']

        wallet = UserPlayWallet.objects.get(id=wallet_id)
        wallet.delete()

        return JsonResponse({'message': 'Wallet deleted successfully', 'success': True})
