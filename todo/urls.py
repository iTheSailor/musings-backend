from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TodoView.as_view(), name='todo'),
    # path('delete', views.delete_todo_item, name='deleteTodo'),
]