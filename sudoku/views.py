from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from .models import Sudoku
from .serializers import SudokuSerializer
from django.contrib.auth.models import User
import json
from . import sudoku_logic

# Create your views here.
class GenerateSudokuView(RetrieveUpdateAPIView):
    def get(self, request, format=None):
        try:
            userid = request.GET['userid']
            user = User.objects.get(id=userid)
        except:
            user = None
        difficulty = request.GET['difficulty']
        puzzle = sudoku_logic.generate_puzzle(difficulty)
        puzzle_list = puzzle.tolist()
        if puzzle is not None:
            Sudoku.objects.create(
                difficulty=difficulty, 
                puzzle=puzzle_list, 
                current_state=puzzle, 
                player=user)
            game = Sudoku.objects.filter(puzzle=puzzle_list, player=user).latest('created_at')
            
            return Response(
                {'status': 'success', 
                 'gameid' : game.id, 
                 'puzzle': puzzle_list,
                 'difficulty': game.difficulty,
                 'time': game.time})
        else:
            return Response({'status': 'failure'})
        
    def put(self, request, format=None):
        data = json.loads(request.body)
        sudoku_id = data['sudoku_id']
        time = data['time']
        sudoku = Sudoku.objects.get(id=sudoku_id)
        sudoku.time = time
        sudoku.save()
        return Response({'status': 'success'})


def create_sudoku_game(request):
    data=request.GET
    print(data)
    userid = data['userid']
    difficulty = data['difficulty']
    pack = {'userid': userid, 'difficulty': difficulty}
    game = Sudoku.create(pack)
    if game:
        serializer = SudokuSerializer(game)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to create game'}, status=404)

    
def get_user_games(request):
    userid = request.GET['userid']
    games = Sudoku.get_user_games(userid)
    if games:
        serializer = SudokuSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)  # Convert to JSON and return
    else:
        return JsonResponse({'error': 'User not found or no games available'}, status=404)

def delete_game(request):
    data= json.loads(request.body)
    gameid = data['gameid']
    userid = data['userid']
    
    deleted = Sudoku.delete_game(gameid, userid)
    if deleted:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failure'}, status=404)
    
def save_game(request):
    data = json.loads(request.body)
    gameid = data['gameid']
    current_state = data['current_state']
    time = data['time']
    saved = Sudoku.save_game(gameid, current_state, time)
    if saved:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failure'}, status=404)
    
def check_sudoku_solution(request):
    data = json.loads(request.body)
    board = data['board']
    result = sudoku_logic.check_sudoku_solution(board)
    is_correct = result[0]
    errors = result[1]
    if result:
        return JsonResponse({'status': 'success', 'is_correct': is_correct, 'errors': errors})
    else:
        return JsonResponse({'status': 'failure'}, status=404)

def give_up(request):
    data = json.loads(request.body)
    gameid = data['gameid']
    game = Sudoku.objects.get(id=gameid)
    game.is_finished = True
    game.win = False
    game.save()
    return JsonResponse({'status': 'success'})

