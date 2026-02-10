from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.post("/login")
def login_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "error": "Credenciales incorrectas"},
        )

    request.session["user_id"] = user.id
    request.session["user_email"] = user.username
    request.session["is_admin"] = bool(user.is_admin)

    return RedirectResponse("/admin/dashboard", status_code=302)


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("admin/register.html", {"request": request})


@router.post("/register")
def register_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()

    if password != password2:
        return templates.TemplateResponse(
            "admin/register.html",
            {"request": request, "error": "Las contraseñas no coinciden"},
        )

    exists = db.query(User).filter(User.username == email).first()
    if exists:
        return templates.TemplateResponse(
            "admin/register.html",
            {"request": request, "error": "Ese correo ya está registrado"},
        )

    new_user = User(
        username=email,
        password_hash=hash_password(password),
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # auto-login opcional (queda más cómodo)
    request.session["user_id"] = new_user.id
    request.session["user_email"] = new_user.username
    request.session["is_admin"] = bool(new_user.is_admin)

    return RedirectResponse("/admin/dashboard", status_code=302)


@router.get("/recuperar")
def recuperar_page(request: Request):
    # placeholder simple para mañana (después lo hacemos bien con email)
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request, "error": "Recuperación: mañana lo dejamos con email 😉"},
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)
