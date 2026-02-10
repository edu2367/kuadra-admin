from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.post("/login")
def login_action(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    if username == "admin" and password == "1234":
        request.session["user"] = "admin"
        return RedirectResponse("/admin/dashboard", status_code=302)

    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request, "error": "Credenciales incorrectas"},
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)
