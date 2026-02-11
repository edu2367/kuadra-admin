from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


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
    email = username.strip().lower()
    user = db.query(User).filter(User.username == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Credenciales incorrectas"})

    request.session["user_id"] = user.id
    return RedirectResponse(url="/panel/dashboard", status_code=303)


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
    phone: str = Form(""),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip().lower()
    phone = phone.strip() if phone else ""

    if password != password2:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Las contraseñas no coinciden"},
        )

    new_user = User(
        username=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        is_admin=False,
    )

    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/auth/login", status_code=303)
