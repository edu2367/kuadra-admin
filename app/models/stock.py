from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)

    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="CASCADE"), nullable=False)

    cantidad = Column(Integer, nullable=False, default=0)

    # Evita duplicados: 1 producto solo puede tener 1 registro de stock por sucursal
    __table_args__ = (
        UniqueConstraint("producto_id", "sucursal_id", name="uq_stock_producto_sucursal"),
    )

    producto = relationship("Producto", back_populates="stocks")
    sucursal = relationship("Sucursal", back_populates="stocks")