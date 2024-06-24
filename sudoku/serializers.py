from rest_framework import serializers
from .models import Sudoku
import json

class SudokuSerializer(serializers.ModelSerializer):
    transformed_state = serializers.SerializerMethodField()
    transformed_solution = serializers.SerializerMethodField()
    class Meta:
        model = Sudoku
        fields = [
            'id', 'player', 'puzzle', 'current_state', 'difficulty', 'time',
            'is_finished', 'win', 'created_at', 'updated_at', 'transformed_state', 'transformed_solution', 'solution'
        ]
        depth = 1  # This is optional, use if you want to include nested relations
    
    def get_transformed_state(self, obj):
        try:
            return json.loads(obj.current_state)
        except json.JSONDecodeError:
            print('Error decoding JSON')
            return None
        
    def get_transformed_solution(self, obj):
        try:
            return json.loads(obj.solution)
        except json.JSONDecodeError:
            print('Error decoding JSON')
            return None