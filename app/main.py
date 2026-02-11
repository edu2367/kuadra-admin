from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os

from app.routers import admin
from app.routers import reportes
from app.routers import auth

from app.db import engine, Base
import app.models

# Crear tablas automáticamente solo en desarrollo por conveniencia.
if os.getenv("ENV", "development") != "production":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="KUADRA - frutales verde limon")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "CAMBIA_ESTE_SECRET_LARGO_Y_RANDOM_123456789"),
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

        user_id = request.session.get("user_id")
        if not user_id:
            return RedirectResponse(url="/auth/login", status_code=302)

        # Para rutas /admin, verificar rol de admin
        if path.startswith("/admin") and not bool(request.session.get("is_admin", False)):
            return RedirectResponse(url="/auth/login", status_code=302)

    return await call_next(request)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(reportes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/admin", status_code=302)
