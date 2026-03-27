from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates_config import templates

router = APIRouter(tags=["Pages"])


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")