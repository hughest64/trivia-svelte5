"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from django.urls import re_path

from game import consumers
from user.authentication import JwtAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddlewareStack(
            URLRouter(
                [
                    re_path(
                        r"ws/(?P<gametype>(game|host))/(?P<joincode>\d+)",
                        consumers.SocketConsumer.as_asgi(),
                    )
                ]
            )
        )
    }
)
