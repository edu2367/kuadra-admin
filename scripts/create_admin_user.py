import os
from app.db import SessionLocal
from app.models.user import User
from app.security import hash_password

# Datos del usuario de prueba
usuario = User(
    username="admin@kuadra.cl",
    password_hash=hash_password("admin1234"),
    first_name="Admin",
    last_name="Principal",
    phone="+56912345678",
    is_admin=True,
)

def crear_usuario():
    db = SessionLocal()
    try:
        existe = db.query(User).filter(User.username == usuario.username).first()
        if existe:
            print("El usuario ya existe.")
            return
        db.add(usuario)
        db.commit()
        print("Usuario creado con éxito.")
    finally:
        db.close()

if __name__ == "__main__":
    print("Base de datos:", os.getenv("DATABASE_URL", "sqlite:///./kuadra_reset.db"))
    crear_usuario()
