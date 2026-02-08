from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.routers import admin
from app.routers import reportes
from app.routers import auth

from app.db import engine, Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Vivero")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(reportes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/admin", status_code=302)
