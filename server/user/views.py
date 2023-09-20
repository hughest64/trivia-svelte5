import logging

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST

import requests

from user.authentication import create_token, decode_token, JwtAuthentication
from user.models import User
from user.utils import Mailer

from game.views.validation.data_cleaner import DataCleaner

logger = logging.getLogger(__name__)


class CreateView(APIView):
    def post(self, request):
        data = DataCleaner(request.data)
        username = data.as_string("username")
        email = data.as_string("email")
        pass1 = data.as_string("pass")
        pass2 = data.as_string("pass2")

        user_created = True

        # return an existing guest user if the jwt is valid otheriwise, create new
        is_guest = data.as_bool("guest_user")
        if is_guest:
            jwt = request.COOKIES.get("jwt")
            user = decode_token(jwt)
            if user.is_anonymous:
                user = User.objects.create_guest_user()
            else:
                user_created = False

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
            except (ValidationError, IntegrityError) as e:
                return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)

        # log them in
        token = create_token(user, user_created=user_created)

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


def get_or_create_oauth_user(name, email):
    """
    use an email address to get or create a user, attempt to create a unique username from
    oauth credentials. in cases where the provided username is taken but the email is not
    """
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        normalized_name = name.lower().replace(" ", "_")

        # the username is taken, try to make it unique
        user_set = User.objects.filter(username=normalized_name)
        if user_set.exists():
            normalized_name += f"_{get_random_string(6)}"

        user = User.objects.create_user(
            username=normalized_name, email=email, password=get_random_string(12)
        )
    return user


class GoogleAuthView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION")
        if access_token is None:
            raise AuthenticationFailed("could not authenticate with google")

        auth_response = requests.get(
            settings.GOOGLE_AUTH_ENDPOINT,
            headers={
                "Authorization": access_token,
                "content-type": "application/json",
                "accept": "application/json",
            },
        )

        if auth_response.status_code != 200:
            raise AuthenticationFailed("could not authenticate with google")

        response_data = auth_response.json()
        name = response_data.get("name")
        email = response_data.get("email")

        user = get_or_create_oauth_user(name, email)
        token = create_token(user)

        response = Response({"user_data": user.to_json()})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


class GithubAuthView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION")
        if access_token is None:
            raise AuthenticationFailed("could not authenticate with google")

        auth_response = requests.get(
            settings.GITHUB_AUTH_ENDPOINT,
            headers={
                "Authorization": access_token,
                "content-type": "application/json",
                "accept": "application/json",
            },
        )

        if auth_response.status_code != 200:
            raise AuthenticationFailed("could not authenticate with github")

        response_data = auth_response.json()
        name = response_data.get("name")
        email = response_data.get("email")

        user = get_or_create_oauth_user(name, email)
        token = create_token(user)

        response = Response()  # Response({"user_data": user.to_json()})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response


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

        response = Response({"user_data": user.to_json()})
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


class UpdateUserview(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        user: User = request.user
        data = DataCleaner(request.data).as_dict()
        password = data.pop("password", None)
        old_pass = data.pop("old_pass", None)

        try:
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            if password:
                if not user.check_password(old_pass):
                    return Response(
                        {"detail": {"password": "The current password is incorrect"}},
                        status=HTTP_400_BAD_REQUEST,
                    )
                user.set_password(password)

            user.save()
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"detail": {"update": "Could not update. The error has been logged."}}
            )

        token = create_token(user)

        response = Response({"user_data": user.to_json()})
        response.set_cookie(key="jwt", value=token, httponly=True)

        return response
