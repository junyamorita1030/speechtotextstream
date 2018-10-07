from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from stt_with_browser import routing as stt_with_browser_routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            stt_with_browser_routing.websocket_urlpatterns
        )
    ),
})
