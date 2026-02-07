from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.db import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)  # ej: "PLT-001"
    nombre = Column(String(120), index=True, nullable=False)  # ej: "Lavanda"
    descripcion = Column(String(255), nullable=True)

    # precio base referencial (puedes luego manejar por sucursal si quieres)
    precio = Column(Numeric(10, 2), nullable=False, default=0)

    stocks = relationship(
        "Stock", back_populates="producto", cascade="all, delete-orphan"
    )
