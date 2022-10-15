from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import create_token, decode_token, JwtAuthentication
from .serializers import UserSerializer

User = get_user_model()


# TODO: update as necessary
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class GuestView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        return Response()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        valid_token = True
        jwt = request.COOKIES.get("jwt")
        user = decode_token(jwt)

        # TODO: create a user
        if user.is_anonymous:
            user = User.objects.get(username="guest")
            valid_token = False

        serializer = UserSerializer(user)
        response = Response({"user_data": serializer.data})

        # TODO: should we "refresh" the token if it is valid?
        if not valid_token:
            token = create_token(user)
            response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class LoginView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        return Response()

    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid Username or Password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid Username or Password")

        serializer = UserSerializer(user)
        token = create_token(user)

        response = Response({"user_data": serializer.data})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class UserView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})


# TODO: maybe don't need to do this since the cookies are controlled in SvelteKit
class LogoutView(APIView):
    def post(self, request):

        response = Response()
        response.delete_cookie("jwt")
        response.delete_cookie("csrftoken")
        response.data = {"message": "success"}

        return response
