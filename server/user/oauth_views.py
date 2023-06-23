from authlib.integrations.django_client import OAuth
from authlib.integrations.requests_client import OAuth2Session

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


import json
from django.urls import reverse
from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentication import create_token, decode_token
from user.models import User

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


# TODO: reference https://github.com/authlib/demo-oauth-client/tree/master/django-google-login for implementation details
def google_login(request):
    # change the uri to a sveltekit endpoint (for dev like: http://localhost:5173/user/google)
    # create an api endpoint there which will
    # redirect_uri = request.build_absolute_uri(reverse("auth"))
    # return oauth.google.authorize_redirect(request, redirect_uri)
    return redirect("game:team")


# probably not a thing
def google_auth(request):
    token = oauth.google.authorize_access_token(request)
    user_email = token.get("email")

    # this needs to get or create a user based on
    # request.session['user'] = token['userinfo']
    return redirect("/team")


# ref: https://docs.authlib.org/en/latest/client/oauth2.html#oidc-session
class GoogleLoginView(APIView):
    def post(self, request):
        client = OAuth2Session(
            "client_id", "client_secret", scope="openid email profile"
        )
        client.fetch_token()
