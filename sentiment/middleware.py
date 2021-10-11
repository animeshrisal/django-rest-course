from channels.db import database_sync_to_async
from .settings import SECRET_KEY
from django.contrib.auth.models import AnonymousUser, User
import jwt
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token):
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])["user_id"]
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        scope['user'] = await get_user(token)

        return await self.app(scope, receive, send)