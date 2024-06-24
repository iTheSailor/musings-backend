from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.middleware.csrf import get_token


class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                csrf_token = get_token(request)
                return Response({'status': 'success', 'username': username, 'user_id': user.id, 'code': 200, 'csrf_token': csrf_token})
            else:
                return Response({'status': 'failure', 'message': 'Invalid password', 'code': 401})
        except:
            return Response({'status': 'failure', 'message': 'User not found', 'code': 404})
        

class SignupView(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return Response({'status': 'success', 'username': username, 'user_id': user.id, 'code': 200})
        except:
            return Response({'status': 'failure', 'message': 'User already exists', 'code': 401})
        