from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST

from user.authentication import create_token, decode_token, JwtAuthentication
from user.models import User
from user.utils import Mailer

from game.views.validation.data_cleaner import DataCleaner


class CreateView(APIView):
    def post(self, request):
        data = DataCleaner(request.data)
        # TODO: add as_username to DataClass and validate it's a valid Django style username
        # i.e =- This value may contain only letters, numbers, and @/./+/-/_ characters.
        username = data.as_string("username")
        email = data.as_string("email")
        pass1 = data.as_string("pass")
        pass2 = data.as_string("pass2")

        # return an existing guest user is the jwt is valid otheriwise, create new
        is_guest = data.as_bool("guest_user")
        if is_guest:
            jwt = request.COOKIES.get("jwt")
            user = decode_token(jwt)
            if user.is_anonymous:
                user = User.objects.create_guest_user()

        else:
            user_query = User.objects.filter(Q(username=username) | Q(email=email))
            if user_query.exists():
                return Response(
                    {
                        "detail": "A user with that username or email address already exists"
                    },
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


# TODO: reference https://github.com/authlib/demo-oauth-client/tree/master/django-google-login for implementation details
class GoogleLoginView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        # TODO: is this actually available on the DRF request?
        # redirect_uri = request.build_absolute_uri(reverse('auth'))
        # return oauth.google.authorize_redirect(request, redirect_uri)
        return Response({"success": True})


class GoogleAuthView(APIView):
    # TODO: is this a post? (probably)
    # token = oauth.google.authorize_access_token(request)
    # get_or_create a user w/ token["userinfo"] (or whatever key it is)
    # we may need to modify the username in the case of create if the username already exists (try/catch?)

    # create a jwt and set the cookie as in standard login
    pass


# for now this is only used to auto-login on password reset
# it requires a non-expired short-lived token
class RefreshTokenView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        token = request.data.get("token")
        user = decode_token(token)
        if user.is_anonymous:
            raise AuthenticationFailed("the token is missing or has expired")
        token = create_token(user)

        response = Response({"success": True})
        response.set_cookie(key="jwt", value=token, httponly=True)
        return response


class UserView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class ForgotPasswordView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        username = data.as_string("username")

        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            raise NotFound("No user with that username or email address exists")

        Mailer(user).send_password_reset()

        return Response({"sucess": True})


class ResetPasswordView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        token = request.data.get("token")

        if token is None:
            raise AuthenticationFailed("The reset token is missing")

        user = decode_token(token)

        if user.is_anonymous:
            raise AuthenticationFailed("The reset token is not valid")

        pass1 = data.as_string("pass1")
        pass2 = data.as_string("pass2")
        if pass1 != pass2:
            raise AuthenticationFailed("Passwords do not match!")

        user.set_password(pass1)
        user.save()
        token = create_token(user)

        response = Response({"user_data": user.to_json()})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


# NOTE: not currently used as cookies are controlled in SvelteKit
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.delete_cookie("csrftoken")
        response.data = {"message": "success"}

        return response
