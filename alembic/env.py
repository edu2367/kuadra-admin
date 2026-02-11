from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.routers import admin, reportes, auth
from app.db import engine, Base
from app.models import user  # 👈 Importa los modelos para registrar las tablas

# Crear tablas automáticamente al iniciar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KUADRA")

# ⚠️ Usa un secreto seguro desde variables de entorno
# En Render configúralo como SESSION_SECRET en Environment
import os

SESSION_SECRET = os.getenv("SESSION_SECRET")
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET no configurado en variables de entorno")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=True,  # en producción con https debe ser True
)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(admin.router)
app.include_router(reportes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/admin", status_code=302)
