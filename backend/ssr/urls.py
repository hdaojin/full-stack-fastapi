from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

from app.core.path_config import TEMPLATES_DIR
from app.api.notes.notes import api_get_note


router = APIRouter(tags=["urls"])

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="/pages/index.html")

@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(request=request, name="/pages/about.html")

@router.get("/notes/{note_name}", response_class=HTMLResponse)
async def read_note(request: Request, note_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/api/v1/notes/{note_name}")
        html_content = response.json()
    return templates.TemplateResponse(request=request, name="/notes/note.html", context=html_content)

# def read_note(request: Request, note_name: str):
#     response = httpx.get(f"http://127.0.0.1:8000/api/v1/notes/{note_name}")

#     html_content = response.json()
#     # print(html_content)
#     return templates.TemplateResponse(request=request, name="/notes/note.html", context=html_content)


 