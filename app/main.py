from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import importlib
import os

from app.routers import admin
from app.routers import reportes
from app.routers import auth

from app.db import engine, Base
from app.models.user import User  # 👈 Importa el modelo para registrar la tabla

# Crear tablas automáticamente al iniciar la app (en cualquier entorno)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KUADRA - frutales verde limon")

# Si está configurado REDIS_URL usaremos sesiones server-side con Redis
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL:
    try:
        import redis
        from app.session_redis import RedisSessionMiddleware

        r = redis.from_url(REDIS_URL, decode_responses=True)
        app.add_middleware(RedisSessionMiddleware, redis_client=r)
    except Exception:
        # Fallback a cookie-based sessions
        app.add_middleware(
            SessionMiddleware,
            secret_key=os.getenv(
                "SESSION_SECRET", "CAMBIA_ESTE_SECRET_LARGO_Y_RANDOM_123456789"
            ),
            same_site="lax",
            https_only=(os.getenv("ENV", "development") == "production"),
        )
else:
    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv(
            "SESSION_SECRET", "CAMBIA_ESTE_SECRET_LARGO_Y_RANDOM_123456789"
        ),
        same_site="lax",
        https_only=(os.getenv("ENV", "development") == "production"),
    )


# Middleware para proteger áreas administrativas y de panel
@app.middleware("http")
async def protect_admin_panel(request, call_next):
    path = request.url.path or ""
    # Excepciones públicas
    public_prefixes = ("/auth", "/static", "/reportes/excel")

    if path.startswith("/admin") or path.startswith("/panel"):
        if any(path.startswith(p) for p in public_prefixes):
            return await call_next(request)

        try:
            sess = request.session
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=302)

        user_id = sess.get("user_id")
        if not user_id:
            return RedirectResponse(url="/auth/login", status_code=302)

        # Para rutas /admin, verificar rol de admin
        if path.startswith("/admin") and not bool(sess.get("is_admin", False)):
            return RedirectResponse(url="/auth/login", status_code=302)

    return await call_next(request)


@app.middleware("http")
async def ensure_csrf_token(request, call_next):
    # Ensure every session has a CSRF token for forms
    import secrets

    try:
        sess = request.session
    except Exception:
        return await call_next(request)

    if "csrf_token" not in sess:
        sess["csrf_token"] = secrets.token_urlsafe(32)

    response = await call_next(request)
    return response


app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(reportes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/admin", status_code=302)
