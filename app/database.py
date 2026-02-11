import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render te da la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Conexión al motor de Postgres
engine = create_engine(DATABASE_URL)

# Sesión para interactuar con la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para tus modelos
Base = declarative_base()


# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
