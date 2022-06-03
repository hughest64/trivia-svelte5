from django.contrib.auth.models import User
from django.http import request
import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .serializers import UserSerializer


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):

    # TODO: handle login with username OR email address,
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # This is ok as we've required username to be unique in UserSerializer
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("No User Found!")

        if not user.check_password(password):
            raise AuthenticationFailed('Bad Password')

        serializer = UserSerializer(user)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'setasecretasanenvvariable', algorithm='HS256')

        response =  Response()
        response.data = serializer.data
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response

    
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('You need to log in!')

        try:
            payload = jwt.decode(token, 'setasecretasanenvvariable', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('You need to log in!')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }

        return response