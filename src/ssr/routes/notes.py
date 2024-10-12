from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bs4 import BeautifulSoup as bs


from ssr.services.api_service import ApiService
from ssr.core.path_config import TEMPLATES_DIR


router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Get all notes subdirectories
@router.get("/notes", response_class=HTMLResponse)
async def list_note_dirs(request: Request):
    api_endpoint = "/notes/subdirectories"
    subdirectories = await ApiService.get(endpoint=api_endpoint)
    return templates.TemplateResponse(request=request, name="notes/index.html", context={"title": "笔记列表", "data": subdirectories})

# View the README.md file of a subdirectory
@router.get("/notes/{subdirectory}", response_class=HTMLResponse)
async def view_subdir_readme(request: Request, subdirectory: str):
    api_endpoint = f"/notes/{subdirectory}/readme"
    readme = await ApiService.get(endpoint=api_endpoint)
    if readme.keys() == {'error_message'}:
        return templates.TemplateResponse(request=request, name="error.html", context={"error_message": readme['error_message']})
    # 需要把返回的内容中的目录的内链替换为增加了子目录的内链，并去掉.md后缀
    # 例如：href="Bash-Script-Introduction.md" 替换为 href="{subdirectory}/Bash-Script-Introduction"
    soup = bs(readme['content'], 'lxml')
    for link in soup.find_all('a'):
        href = link.get('href')
        if isinstance(href, str) and href.endswith('.md'):
            link['href'] = f"{subdirectory}/{href.removesuffix('.md')}"   
    readme['content'] = str(soup)
    return templates.TemplateResponse(request=request, name="notes/readme.html", context={"data": readme})

# View a note file in a subdirectory
@router.get("/notes/{subdirectory}/{note_name}", response_class=HTMLResponse)
async def view_subdir_note(request: Request, subdirectory: str, note_name: str):
    api_endpoint = f"/notes/{subdirectory}/{note_name}.md"
    note = await ApiService.get(endpoint=api_endpoint)
    return templates.TemplateResponse(request=request, name="notes/note.html", context={"data": note})
