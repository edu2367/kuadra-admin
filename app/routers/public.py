from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Public"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def public_home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Frutales Verde Limón",
        },
    )
