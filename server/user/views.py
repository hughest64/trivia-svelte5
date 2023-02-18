from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from user.authentication import create_token, decode_token, JwtAuthentication
from user.models import User

from game.views.validation.data_cleaner import DataCleaner


class CreateView(APIView):
    # @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        # TODO: add as_username to DataClass and validate it's a valid Django style username
        # i.e =- This value may contain only letters, numbers, and @/./+/-/_ characters.
        username = data.as_string("username")
        email = data.as_string("email")
        pass1 = data.as_string("pass")
        pass2 = data.as_string("pass2")

        # return Response({"success": True})
        user_query = User.objects.filter(username=username)
        if user_query.exists():
            return Response(
                {"detail": "A user with that username already exists"},
                status=HTTP_400_BAD_REQUEST,
            )

        if pass1 != pass2:
            return Response(
                {"detail": "passwords do not match"}, status=HTTP_400_BAD_REQUEST
            )

        try:
            # create the user and set the password
            user = User.objects.create_user(
                username=username, email=email, password=pass1
            )
        except ValidationError as e:
            return Response({"detail": e}, status=HTTP_400_BAD_REQUEST)

        # log them in
        token = create_token(user)

        response = Response({"user_data": user.to_json()})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class ResetPasswordView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        raise NotFound("this is not the page you are looking for")

        data = DataCleaner(request.data)
        username = data.as_string("username")  # is this needed?
        email = data.as_string("email")  # or just this?
        pass1 = data.as_string("pass1")
        pass2 = data.as_string("pass2")

        # look up the user throw if not a thing
        # validate that the passwords match
        # user.set_password
        # create a token ???
        # let them know everthing is hunky dory


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
