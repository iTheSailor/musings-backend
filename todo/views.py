from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TodoItem
from django.contrib.auth.models import User
import json
from icecream import ic


# Create your views here.

class TodoView(APIView): 
    def get(self, request, format=None):
        ic(request.GET)
        if 'user' in request.GET:
            user_id = request.GET['user']
            user = User.objects.get(id=user_id)
        else:
            user_id = None
            user = None
        todos = TodoItem.objects.filter(user=user, completed=False)
        completed_todos = TodoItem.objects.filter(user=user, completed=True)
        todo_list = []
        finished_list = []
        for todo in todos:
            todo_list.append({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed
            })
        for todo in completed_todos:
            finished_list.append({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed
            })
        todo_list = {'todos': todo_list, 'completed': finished_list}
        return Response(todo_list)
    
    def post(self, request, format=None):
        print(request)
        data = json.loads(request.body)
        print(data)
        user_id = data['user']
        title = data['title']
        description = data['description']
        completed = 0
        ic(user_id, title, description)
        if user_id:
            user = User.objects.get(id=user_id) 
        else:
            user = None 
        todo = TodoItem(user=user, title=title, description=description, completed=completed)
        todo.save()
        return Response({'status': 'success'})
    
    def put(self, request, format=None):
        todo_id = request.data['todo_id']
        todo = TodoItem.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
        return Response({'status': 'success'})
    
    def patch(self, request, format=None):
        todo_id = request.data['todo_id']
        title = request.data['title']
        description = request.data['description']
        completed = request.data['completed']
        todo = TodoItem.objects.get(id=todo_id)
        todo.title = title
        todo.description = description
        todo.completed = completed
        todo.save()
        return Response({'status': 'success'})

    def delete(self, request, format=None):
        todo_id = request.data['todo_id']
        user_id = request.data['user']
        todo = TodoItem.objects.get(id=todo_id, user=user_id)
        todo.delete()
        return Response({'status': 'success'})
