from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

import os

print("CWD =", os.getcwd())
print("DATABASE_URL =", settings.DATABASE_URL)

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL, pool_pre_ping=True, connect_args=connect_args
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 👇 Importa tus modelos para que se registren en Base
from app.models import user

# 👇 Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)
