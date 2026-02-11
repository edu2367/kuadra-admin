from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Producto, Sucursal, Stock


router = APIRouter(prefix="/panel", tags=["Panel"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def panel_home():
    return RedirectResponse(url="/panel/dashboard", status_code=302)


@router.get("/dashboard")
def panel_dashboard(request: Request, db: Session = Depends(get_db)):
    total_productos = db.query(Producto).count()
    total_sucursales = db.query(Sucursal).count()
    total_registros_stock = db.query(Stock).count()

    return templates.TemplateResponse(
        "panel_dashboard.html",
        {
            "request": request,
            "title": "Dashboard",
            "subtitle": "Resumen general del vivero",
            "total_productos": total_productos,
            "total_sucursales": total_sucursales,
            "total_registros_stock": total_registros_stock,
            "active": "dashboard",  # ✅ ESTE
        },
    )


# -------------------------
# PRODUCTOS
# -------------------------
@router.get("/productos")
def panel_productos(request: Request, db: Session = Depends(get_db)):
    productos = db.query(Producto).order_by(Producto.id.desc()).all()

    return templates.TemplateResponse(
        "panel_productos.html",
        {
            "request": request,
            "productos": productos,
            "title": "Productos",
            "subtitle": "Crear y administrar productos",
            "current_sucursal": "Frutales Verde Limón",
            "active": "productos",  # ✅ CORRECTO AQUÍ
        },
    )


@router.post("/productos/crear")
def panel_crear_producto(
    nombre: str = Form(...),
    sku: str = Form(""),
    precio: float = Form(0),
    descripcion: str = Form(""),
    db: Session = Depends(get_db),
    _csrf: None = csrf_dependency(),
):
    nombre = nombre.strip()
    sku = sku.strip()

    p = Producto(
        nombre=nombre,
        sku=sku if sku else f"SKU-{nombre[:10]}",
        precio=precio,
        descripcion=descripcion if descripcion else None,
    )
    db.add(p)
    db.commit()
    return RedirectResponse(url="/panel/productos", status_code=303)


# -------------------------
# STOCK POR SUCURSAL
# -------------------------
@router.get("/stock")
def panel_stock(
    request: Request, sucursal_id: int | None = None, db: Session = Depends(get_db)
):
    sucursales = db.query(Sucursal).order_by(Sucursal.id.asc()).all()

    if sucursal_id is None and sucursales:
        sucursal_id = sucursales[0].id

    productos = db.query(Producto).order_by(Producto.nombre.asc()).all()

    stock_map = {}
    if sucursal_id is not None:
        stocks = db.query(Stock).filter(Stock.sucursal_id == sucursal_id).all()
        stock_map = {st.producto_id: st.cantidad for st in stocks}

    return templates.TemplateResponse(
        "panel_stock.html",
        {
            "request": request,
            "sucursales": sucursales,
            "sucursal_id": sucursal_id,
            "productos": productos,
            "stock_map": stock_map,
            "title": "Stock",
            "subtitle": "Ajusta cantidades por sucursal",
            "active": "stock",  # ✅ ESTE
        },
    )


@router.post("/stock/ajustar")
def panel_ajustar_stock(
    sucursal_id: int = Form(...),
    producto_id: int = Form(...),
    delta: int = Form(...),
    db: Session = Depends(get_db),
    _csrf: None = csrf_dependency(),
):
    st = (
        db.query(Stock)
        .filter(Stock.sucursal_id == sucursal_id, Stock.producto_id == producto_id)
        .first()
    )

    if not st:
        st = Stock(sucursal_id=sucursal_id, producto_id=producto_id, cantidad=0)
        db.add(st)

    nueva = (st.cantidad or 0) + int(delta)
    if nueva < 0:
        nueva = 0

    st.cantidad = nueva
    db.commit()

    return RedirectResponse(
        url=f"/panel/stock?sucursal_id={sucursal_id}", status_code=303
    )
