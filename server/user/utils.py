# utils.py
""" Helper functions for user views
"""
import datetime

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

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
        return AnonymousUser

    try:
        payload = jwt.decode(token, settings.JWT_TOKEN_SECRET, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return AnonymousUser

    user = User.objects.filter(id=payload["id"]).first()

    return user or AnonymousUser
