from fastapi import APIRouter, HTTPException
from fastapi import Path as FastAPIPath
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.path_config import UPLOADS_DIR
from app.services.md2html import markdown_to_html


router = APIRouter()

# Path to the pages directory
PAGES_DIR = UPLOADS_DIR / "pages"
PAGES_DIR.mkdir(parents=True, exist_ok=True)

def get_file_path(page_name: str) -> Path:
    """
    根据文件名获取文件完整路径
    """
    # file_path = PAGES_DIR.joinpath(f"{page_name}.md")
    file_path = PAGES_DIR / f"{page_name}.md"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    return file_path


# @router.get("/")
# async def get_index():
#     """
#     获取index.md文件的内容并转换为HTML
#     :return: 返回转换后的HTML内容
#     """
#     try:
#         file_path = get_file_path("index")
#         file_content = file_path.read_text(encoding='utf-8')
#         html = markdown_to_html(file_content)
#         return {"html": html}
#     except HTTPException as e:
#         raise e     # 返回文件不存在的异常
#     except Exception:
#         raise HTTPException(status_code=500, detail="Markdown file conversion failed.")

@router.get("/{page_name:path}")
async def get_page(page_name:str = FastAPIPath(..., title="The name of the page to get")):
    """
    获取指定markdown page文件中的内容并转换为HTML提供给前端渲染page页面
    :param page_name: markdown文件名
    :return: 返回转换后的HTML内容
    """
    if ".." in page_name or page_name.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid page name.")
    try:
        file_path = get_file_path(page_name)
        file_content = file_path.read_text(encoding='utf-8')
        html = markdown_to_html(file_content)
        return {"html": html}
    except HTTPException as e:
        raise e     # 返回文件不存在的异常
    except Exception:
        raise HTTPException(status_code=500, detail="Markdown file conversion failed.")

@router.get("/images/{file_path:path}")
async def get_file(file_path: str):
    """
    返回指定的文件
    :param file_path: 文件路径
    :return: 返回文件
    """
    file_path = PAGES_DIR / file_path
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    return FileResponse(file_path)