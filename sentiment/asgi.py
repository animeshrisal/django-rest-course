"""
ASGI config for sentiment project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django.core.asgi import get_asgi_application
from app import consumers
from .middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": TokenAuthMiddleware(
        URLRouter([
            re_path("", consumers.NotificationConsumer.as_asgi()),
        ])
    ),
})