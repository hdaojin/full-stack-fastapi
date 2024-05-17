from fastapi import APIRouter

import frontmatter
import mistune
from bs4 import BeautifulSoup

from app.core.path_config import UPLOADS_DIR

router = APIRouter()

# Path to the notes directory
NOTES_DIR = UPLOADS_DIR / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)



@router.get("/note")
def markdown_to_html():
    """
    Convert content of markdown file to HTML using mistune
    """
    note_path = NOTES_DIR.joinpath("test.md")
    if note_path.exists() and note_path.is_file():
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            meta = post.metadata
            content = post.content
            html = mistune.html(content)
        return {"meta": meta, "html": html}
    else:
        return {"error": "Note not found"}





