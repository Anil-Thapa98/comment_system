import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import comments.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_comments.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(comments.routing.websocket_urlpatterns),
})
