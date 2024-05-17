from fastapi import APIRouter

from app.core.path_config import UPLOADS_DIR
from app.common.md2html import markdown_to_html


router = APIRouter()

# Path to the pages directory
PAGES_DIR = UPLOADS_DIR / "pages"
PAGES_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/{page_name}")
async def get_pages(page_name):
    """
    获取指定markdown文件中的内容并转换为HTML
    """
    page_path = PAGES_DIR.joinpath(f"{page_name}.md")
    if page_path.exists() and page_path.is_file():
        with open(page_path, 'r', encoding='utf-8') as f:
            return markdown_to_html(f.read())
    else:
        return {"error": "Page not found"}

