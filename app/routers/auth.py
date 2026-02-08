from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="app/templates")


# 👉 LOGIN (GET)
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


# 👉 LOGIN (POST)
@router.post("/login")
def login_action(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    # login simple por ahora
    if username == "admin" and password == "1234":
        request.session["user"] = "admin"  # 🔥 SESIÓN REAL
        return RedirectResponse("/admin/dashboard", status_code=302)

    return templates.TemplateResponse(
        "admin/login.html", {"request": request, "error": "Credenciales incorrectas"}
    )


# 👉 LOGOUT
@router.get("/logout")
def logout():
    response = RedirectResponse("/auth/login", status_code=302)
    response.delete_cookie("session")
    return response
