from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def auth_root():
    return RedirectResponse("/auth/login", status_code=302)


# ---------- LOGIN ----------
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def login_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_value = username.strip().lower()

    if not login_value:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Debes ingresar tu correo"},
            status_code=400,
        )

    user = db.query(User).filter(User.username == login_value).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Credenciales incorrectas"},
            status_code=401,
        )

    request.session["user_id"] = user.id
    request.session["is_admin"] = bool(getattr(user, "is_admin", False))

    return RedirectResponse("/admin/dashboard", status_code=302)


# ---------- LOGOUT ----------
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)


# ---------- RECOVER ----------
@router.get("/recover")
def recover_page(request: Request):
    return templates.TemplateResponse("auth/recover.html", {"request": request})


@router.post("/recover")
def recover_action(
    request: Request,
    username: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username.strip().lower()).first()
    if not user:
        return templates.TemplateResponse(
            "auth/recover.html",
            {"request": request, "error": "No existe un usuario con ese correo"},
