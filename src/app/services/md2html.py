# import frontmatter
import markdown2
# import nh3
from bs4 import BeautifulSoup


def markdown_to_html(md_content: str) -> dict:
    """
    Convert markdown content to HTML using markdown2
    """
    # post = frontmatter.loads(md_content)  # python-frontmatter is used to load and parse files (or just text) with YAML (or JSON, TOML or other) front matter
    # meta = post.metadata
    # content = post.content
    extras = [
        # "breaks", # Convert '\n' in paragraphs into <br>
        "code-friendly", # Disable _ and __ for em and strong
        "cuddled-lists", # Allow lists to be cuddled to the preceding paragraph
        "fenced-code-blocks", # Allow code blocks to be fenced by ```
        "metadata", # Parse metadata at the beginning of the markdown content
        "footnotes", # Parse footnotes
        "highlightjs-lang", # Highlight code blocks with language
        "numbering", # Create counters to number tables,figures, equations and graphs
        "tables", # Parse tables
        "toc", # Generate a table of contents
        "header-ids", # Adds "id" attribute to headers
        "task_list", # Parse task lists
    ]
    html_content = markdown2.markdown(md_content, extras=extras)
    meta = html_content.metadata
    toc_content = html_content.toc_html
    # safe_html_content = nh3.clean(html_content)   # nh3 is used to sanitize HTML content
    # safe_toc_content = nh3.clean(toc_content)
    # safe_meta_content = {k.lower(): nh3.clean(v) for k, v in meta.items()} if meta else {}
    meta_content = {k.lower(): v for k, v in meta.items()} if meta else {}
    return {"meta": meta_content, "toc": toc_content, "content": html_content}

def extract_soup_from_html(html: str) -> str:
    """
    Extract BeautifulSoup object from HTML content
    """
    soup = BeautifulSoup(html, 'html.parser')
    h1_string = soup.h1.string if soup.h1 else "article"
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    toc = [{"level": header.name, "text": header.string} for header in headers]
    return {"title": h1_string, "toc": toc}



