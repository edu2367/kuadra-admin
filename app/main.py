from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os

from app.routers import admin, reportes, auth
from app.db import engine, Base
from app.models import user  # importa modelos

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KUADRA")

SESSION_SECRET = os.getenv("SESSION_SECRET")

if not SESSION_SECRET or SESSION_SECRET == "dev-secret-change-me":
    raise RuntimeError("SESSION_SECRET no configurado o inseguro")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False,  # en producción con https
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(reportes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/admin", status_code=302)
