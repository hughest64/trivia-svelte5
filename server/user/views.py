from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND

from user.authentication import create_token, decode_token, JwtAuthentication
from user.models import User


class RegisterView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):

        return Response({"detail": "Not Found"}, code=HTTP_404_NOT_FOUND)


class GuestView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"success": True})

    @method_decorator(csrf_protect)
    def post(self, request):
        valid_token = True
        jwt = request.COOKIES.get("jwt")
        user = decode_token(jwt)

        if user.is_anonymous:
            user = User.objects.get(username="guest")
            valid_token = False

        user_data = user.to_json()
        response = Response({"user_data": user_data})

        if not valid_token:
            token = create_token(user)
            response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class LoginView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"success": True})

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

        user_data = user.to_json()
        token = create_token(user)

        response = Response({"user_data": user_data})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class UserView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


# NOTE: not currently used as cookies are controlled in SvelteKit
class LogoutView(APIView):
    def post(self, request):

        response = Response()
        response.delete_cookie("jwt")
        response.delete_cookie("csrftoken")
        response.data = {"message": "success"}

        return response
