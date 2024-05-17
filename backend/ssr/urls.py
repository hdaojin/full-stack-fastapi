from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.path_config import TEMPLATES_DIR


router = APIRouter(tags=["urls"])

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="/pages/index.html")

@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(request=request, name="/pages/about.html")

@router.get("/note", response_class=HTMLResponse)
def read_note(request: Request):
    return templates.TemplateResponse(request=request, name="/notes/note.html")


