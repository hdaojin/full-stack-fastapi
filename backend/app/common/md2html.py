import frontmatter
import mistune
from bs4 import BeautifulSoup

from app.core.path_config import UPLOADS_DIR



def markdown_to_html(md_content: str) -> str:
    """
    Convert markdown content to HTML using mistune
    """
    post = frontmatter.loads(md_content)
    meta = post.metadata
    content = post.content
    html = mistune.html(content)
    return {"meta": meta, "html": html}