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
    email: str = Form(None),
    username: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_value = (email or username or "").strip().lower()

    if not login_value:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Debes ingresar tu correo",
            },
            status_code=400,
        )


@router.post("/login")
def login_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    import logging

    log = logging.getLogger("uvicorn.error")

    login_value = (username or "").strip().lower()

    if not login_value:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Debes ingresar tu correo"},
            status_code=400,
        )

    user = db.query(User).filter(User.username == login_value).first()
    log.info(f"LOGIN email={login_value} user_found={bool(user)}")

    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Credenciales incorrectas"},
            status_code=401,
        )

    # ya sabemos que user no es None
    if not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Credenciales incorrectas"},
            status_code=401,
        )

    # OK: setear sesión y entrar
    request.session["user_id"] = user.id
    request.session["user_email"] = user.username
    request.session["is_admin"] = bool(user.is_admin)

    return RedirectResponse("/admin/dashboard", status_code=302)


# ---------- LOGOUT ----------
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)


# ---------- REGISTER ----------
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
def register_action(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()

    if password != password2:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Las contraseñas no coinciden"},
            status_code=400,
        )

    # validar que no exista
    exists = db.query(User).filter(User.username == email).first()
    if exists:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Este correo ya está registrado"},
            status_code=400,
        )

    user = User(
        username=email,
        password_hash=hash_password(password),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        phone=(phone or "").strip() or None,
        is_admin=False,
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/auth/login", status_code=303)
