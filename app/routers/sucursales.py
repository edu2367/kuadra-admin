from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Sucursal

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_sucursal(
    nombre: str, direccion: str | None = None, db: Session = Depends(get_db)
):
    existe = db.query(Sucursal).filter(Sucursal.nombre == nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="La sucursal ya existe")

    s = Sucursal(nombre=nombre, direccion=direccion)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/")
def listar_sucursales(db: Session = Depends(get_db)):
    return db.query(Sucursal).order_by(Sucursal.id.asc()).all()
