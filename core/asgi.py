import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import chats.routing
from .auth_middleware import TokenAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app  = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': 
        AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(chats.routing.websocket_urlpatterns)
            )
        )
})
