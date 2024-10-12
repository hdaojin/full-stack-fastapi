from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from ssr.services.page_service import PageService
from ssr.core.path_config import TEMPLATES_DIR


router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def get_pages(request: Request):
    page_content = await PageService.get_page()
    return templates.TemplateResponse(request=request, name="pages/index.html", context={"data": page_content['html']})


@router.get("/{page_name:path}", response_class=HTMLResponse)
async def get_page(request: Request, page_name: str):
    page_content = await PageService.get_page(page_name)
    if page_content.keys() == {'error_message'}:
        return templates.TemplateResponse(request=request, name="error.html", context={"error_message": page_content['error_message']})
    return templates.TemplateResponse(request=request, name="pages/page.html", context={"data": page_content['html']})