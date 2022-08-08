import datetime

from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

import jwt

User = get_user_model()


def create_token(user_id):
    """Create a jwt token from a user id"""
    payload = {
        "id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=settings.JWT_TOKEN_TTL),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.JWT_TOKEN_SECRET, algorithm="HS256")

    return token


def decode_token(token):
    """Return a User object if passed a valid JWT or an instance of AnonymousUser otherwise"""
    if not token:
        return AnonymousUser()

    try:
        payload = jwt.decode(token, settings.JWT_TOKEN_SECRET, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return AnonymousUser()

    user = User.objects.filter(id=payload["id"]).first()

    return user or AnonymousUser()


@database_sync_to_async
def get_user(token):
    """
    Sync to async wrapper around decode_token
    """
    return decode_token(token)


class JwtAuthentication(authentication.BaseAuthentication):
    """custom JWT authentication for Django Rest Framework"""

    def authenticate(self, request):
        token = request.COOKIES.get("jwt")
        print(request.COOKIES)

        if not token:
            raise AuthenticationFailed("You need to log in!")

        try:
            payload = jwt.decode(token, settings.JWT_TOKEN_SECRET, algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("You need to log in!")

        # TODO: handle bad id? Is that possible at this point?
        # should we just return AnonymousUser?
        user = User.objects.get(id=payload["id"])

        return (user, None)


class JwtAuthMiddleware:
    """custom JWT authentication for Django Channels. Requires CookieMiddleware higher in the stack"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        jwt = scope["cookies"].get("jwt")

        scope["user"] = await get_user(jwt)

        return await self.app(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """bypass the session middleware and use custom auth middleware to handle JWT authentication"""
    return CookieMiddleware(JwtAuthMiddleware(inner))
