from django.urls import path
from . import views

urlpatterns = [
    path('get_stock', views.get_stock, name='get_stock'),
    path('get_watchlist', views.get_watchlist, name='get_watchlist'),
    path('add_watchlist', views.add_watchlist, name='add_watchlist'),
    path('remove_watchlist', views.remove_watchlist, name='remove_watchlist'),
    path('get_full_stock', views.get_full_stock, name='get_full_stock'),

    # Wallet URLs
    path('create_wallet', views.create_wallet, name='create_wallet'),
    path('add_stock_to_wallet', views.add_stock_to_wallet, name='add_stock_to_wallet'),
    path('sell_stock_from_wallet', views.sell_stock_from_wallet, name='sell_stock_from_wallet'),
    path('get_wallets', views.get_wallets, name='get_wallets'),
    path('get_wallet_details', views.get_wallet_details, name='get_wallet_details'),
    path('get_wallet_history', views.get_wallet_history, name='get_wallet_history'),
    path('get_stock_history', views.get_stock_history, name='get_stock_history'),
    path('rename_wallet', views.rename_wallet, name='rename_wallet'),
    path('delete_wallet', views.delete_wallet, name='delete_wallet'),
    path('add_stock_to_wallet', views.add_stock_to_wallet, name='add_stock_to_wallet'),
    path('sell_stock_from_wallet', views.sell_stock_from_wallet, name='sell_stock_from_wallet'),

]
