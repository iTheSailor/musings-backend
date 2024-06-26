from django.urls import path
from . import views

urlpatterns = [
    path('play', views.create_sudoku_game, name='sudoku'),
    path('updateTime', views.main_sudoku, name='sudokuTimer'),
    path('checkSolution', views.check_sudoku_solution, name='sudokuSolution'),
    path('giveUp', views.give_up, name='sudokuGiveUp'),
    path('savedGames', views.get_user_games, name='savedGames'),
    path('deleteGame', views.delete_game, name='deleteGame'),
    path('saveGame', views.save_game, name='saveGame'),
]

