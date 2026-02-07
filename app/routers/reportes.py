from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from openpyxl import Workbook

from app.db import get_db
from app.models.ventas import Venta, VentaItem

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/reportes/excel")
def reporte_excel(db: Session = Depends(get_db)):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    ws.append(["venta_id", "fecha", "sucursal_id", "producto_id", "qty", "precio"])

    ventas = db.query(Venta).order_by(Venta.id.desc()).limit(200).all()
    for v in ventas:
        for it in v.items:
            ws.append(
                [
                    v.id,
                    str(v.created_at),
                    v.sucursal_id,
                    it.producto_id,
                    it.qty,
                    it.precio,
                ]
            )

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)

    headers = {"Content-Disposition": 'attachment; filename="reporte_ventas.xlsx"'}
    return StreamingResponse(
        bio,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
