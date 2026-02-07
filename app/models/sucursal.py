from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), unique=True, index=True, nullable=False)  # ej: "Centro"
    direccion = Column(String(180), nullable=True)

    stocks = relationship(
        "Stock", back_populates="sucursal", cascade="all, delete-orphan"
    )
