import frontmatter
import markdown2
from bs4 import BeautifulSoup

# from app.core.path_config import UPLOADS_DIR



def markdown_to_html(md_content: str) -> str:
    """
    Convert markdown content to HTML using mistune
    """
    post = frontmatter.loads(md_content)  # python-frontmatter is used to load and parse files (or just text) with YAML (or JSON, TOML or other) front matter
    meta = post.metadata
    meta = {k.lower(): v for k, v in meta.items()}
    content = post.content
    extras = [
        # "breaks", # Convert '\n' in paragraphs into <br>
        "code-friendly", # Disable _ and __ for em and strong
        "cuddled-lists", # Allow lists to be cuddled to the preceding paragraph
        "fenced-code-blocks", # Allow code blocks to be fenced by ```
        "footnotes", # Parse footnotes
        # "header-ids", # Adds "id" attribute to headers
        "highlightjs-lang", # Highlight code blocks with language
        "numbering", # Create counters to number tables,figures, equations and graphs
        "tables", # Parse tables
        "toc", # Generate a table of contents
        "task_list", # Parse task lists
    ]
    html_content = markdown2.markdown(content, extras=extras)
    toc_content = html_content.toc_html
    return {"meta": meta, "toc": toc_content, "content": html_content}

def extract_soup_from_html(html: str) -> str:
    """
    Extract BeautifulSoup object from HTML content
    """
    soup = BeautifulSoup(html, 'html.parser')
    h1_string = soup.h1.string if soup.h1 else "article"
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    toc = [{"level": header.name, "text": header.string} for header in headers]
    return {"title": h1_string, "toc": toc}

# TESTING
if __name__ == "__main__":
    from pathlib import Path
    import json
    md_file = Path(__file__).parent.parent.parent / "uploads" / "notes" / "test.md"
    with open(md_file, "r", encoding='utf-8') as f:
        md_content = f.read()
    html_content = markdown_to_html(md_content)
    print(json.dumps(html_content, indent=4))
    soup = extract_soup_from_html(html_content["html"])
    print(json.dumps(soup, indent=4))
