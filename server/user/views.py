from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, get_user_model, login, logout

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer

import json

User = get_user_model()

class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                { "message": "Username or Password is Incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        print(user.is_authenticated)
        login(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                data={"message": "Not Logged In"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(username=request.user.username).first()
        serializer = UserSerializer(user)
        print(serializer.data)

        return Response(data=serializer.data, content_type="application/json")


class LogoutView(APIView):
    
    def post(self, request):
        logout(request.user)

        return Response({"message": "success"})
