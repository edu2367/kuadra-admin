import os
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User

# Script para listar usuarios en la base de datos actual

def listar_usuarios():
    db: Session = SessionLocal()
    try:
        usuarios = db.query(User).all()
        if not usuarios:
            print("No hay usuarios en la base de datos.")
        else:
            for u in usuarios:
                print(f"ID: {u.id} | Email: {u.username} | Nombre: {u.first_name} {u.last_name} | Admin: {u.is_admin}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Base de datos:", os.getenv("DATABASE_URL", "sqlite:///./kuadra_reset.db"))
    listar_usuarios()
