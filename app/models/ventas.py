from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base


class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)

    # relaciones (si ya tienes Sucursal model, con __tablename__="sucursales")
    items = relationship(
        "VentaItem", back_populates="venta", cascade="all, delete-orphan"
    )


class VentaItem(Base):
    __tablename__ = "venta_items"
    id = Column(Integer, primary_key=True, index=True)

    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)

    qty = Column(Integer, nullable=False)  # cantidad vendida
    precio = Column(Integer, default=0, nullable=False)  # opcional (puede quedar 0)

    venta = relationship("Venta", back_populates="items")
