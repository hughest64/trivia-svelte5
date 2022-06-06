import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import JwtAuthentication
from .serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response()

    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            raise AuthenticationFailed("Username or Password is Invalid")

        if not user.check_password(password):
            raise AuthenticationFailed('Username or Password is Invalid')

        serializer = UserSerializer(user)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_TOKEN_TTL),
            'iat': datetime.datetime.utcnow()
        }

        # TODO: make an actual token variable
        token = jwt.encode(payload, settings.JWT_TOKEN_SECRET, algorithm='HS256')

        response =  JsonResponse(serializer.data)
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response


class UserView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def get(self, request):
        serializer = UserSerializer(request.user)

        return JsonResponse(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.delete_cookie('csrftoken')
        response.data = {
            "message": "success"
        }

        return response