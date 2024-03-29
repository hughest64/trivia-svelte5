"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

from django.core.asgi import get_asgi_application
from django.urls import re_path
django_asgi_app = get_asgi_application()

from game import consumers
from user.authentication import JwtAuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
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
