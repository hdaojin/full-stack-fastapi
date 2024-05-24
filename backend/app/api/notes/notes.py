from fastapi import APIRouter
from pydantic import BaseModel

from app.common.md2html import markdown_to_html
from app.core.path_config import UPLOADS_DIR

router = APIRouter()

# Path to the notes directory
NOTES_DIR = UPLOADS_DIR / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)

class NoteResponse(BaseModel):
    meta: dict
    toc: str
    content: str

@router.get("/{note_name}", response_model=NoteResponse)
async def api_get_note(note_name: str):
    """
    Get content of specified markdown file and convert to HTML
    """
    note_path = NOTES_DIR.joinpath(f"{note_name}.md")
    if note_path.exists() and note_path.is_file():
        with open(note_path, 'r', encoding='utf-8') as f:
            html = markdown_to_html(f.read())
            return html
    else:
        return {"error": "Note not found"}