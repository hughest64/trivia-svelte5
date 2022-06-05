import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .serializers import UserSerializer

from .authentication import JwtAuthentication

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

    # TODO: handle login with username OR email address,
    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # This is ok as we've required username to be unique in UserSerializer
        # but we should probably use the authenticate method?
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("No User Found!")

        if not user.check_password(password):
            raise AuthenticationFailed('Bad Password')

        serializer = UserSerializer(user)

        payload = {
            'id': user.id,
            # TODO: set time delta in settings as JWT_TTL (in minutes)
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow()
        }

        # TODO: make an actual token variable
        token = jwt.encode(payload, 'setasecretasanenvvariable', algorithm='HS256')

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