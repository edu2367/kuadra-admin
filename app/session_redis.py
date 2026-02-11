import json
from typing import Callable
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Receive, Scope, Send
from http import cookies
import time


class RedisSessionMiddleware:
    def __init__(self, app: ASGIApp, redis_client, cookie_name: str = "session_id", max_age: int = 7 * 24 * 3600):
        self.app = app
        self.redis = redis_client
        self.cookie_name = cookie_name
        self.max_age = max_age

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = MutableHeaders(scope=scope["headers"])
        # parse cookies
        raw = None
        for k, v in scope.get("headers", []):
            if k.decode().lower() == "cookie":
                raw = v.decode()
                break

        sid = None
        if raw:
            c = cookies.SimpleCookie()
            c.load(raw)
            if self.cookie_name in c:
                sid = c[self.cookie_name].value

        session = {}
        if sid:
            data = self.redis.get(sid)
            if data:
                try:
                    session = json.loads(data)
                except Exception:
                    session = {}
        else:
            # generate sid
            sid = str(int(time.time() * 1000)) + "-" + str(id(scope))

        scope.setdefault("session", session)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # save session
                try:
                    self.redis.set(sid, json.dumps(scope.get("session", {})), ex=self.max_age)
                    # set cookie header
                    headers = MutableHeaders(scope=message.setdefault("headers", []))
                    # starlette expects header tuples; ensure cookie present
                    cookie_val = f"{self.cookie_name}={sid}; Path=/; HttpOnly; Max-Age={self.max_age}"
                    message["headers"].append((b"set-cookie", cookie_val.encode()))
                except Exception:
                    pass
            await send(message)

        await self.app(scope, receive, send_wrapper)
