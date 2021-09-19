import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import ws_gateway.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_arsmoon.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_gateway.routing.urlpatterns)
    ),
})