from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from .utils import decode_token

import jwt

User = get_user_model()


class JwtAuthentication(authentication.BaseAuthentication):
    """custom JWT authentication for Django Rest Framework"""

    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("You need to log in!")

        try:
            # TODO: make an actual token variable
            payload = jwt.decode(token, settings.JWT_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("You need to log in!")

        # TODO: handle bad id? Is that possible at this point?
        # should we just return AnonymousUser?
        user = User.objects.get(id=payload["id"])

        return (user, None)


@database_sync_to_async
def get_user(token):
    """
    Sync to async wrapper around the decode token function which returns an authenticated
    authenticated user instance if the token is valid or an instance of AnonymousUser if not.
    """
    return decode_token(token)


class JwtAuthMiddleware:
    """custom JWT authentication for Django Channels. Requires CookieMiddleware higher in the stack"""

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        jwt = scope["cookies"].get("jwt")

        scope["user"] = await get_user(jwt)

        return await self.app(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """bypass the session middleware and use custom auth middleware to handle JWT authentication"""
    return CookieMiddleware(JwtAuthMiddleware(inner))
