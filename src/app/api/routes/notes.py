from fastapi import APIRouter, HTTPException
from typing import List, Dict, Union
from pathlib import Path

from app.models import NoteResponse
from app.services.md2html import markdown_to_html
from app.core.path_config import UPLOADS_DIR

router = APIRouter()

# Path to the notes directory
NOTES_DIR = UPLOADS_DIR / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)

# Validate the notes directory
async def _validate_notes_directory(path: Path):
    if not path or not path.is_dir():
        raise HTTPException(status_code=404, detail="Notes directory not found")
    
# Convert markdown file to HTML  
async def _convert_markdown_file_to_html(file_path: Path):
    if not file_path.exists() or not file_path.is_file() or not file_path.suffix == ".md":
        raise HTTPException(status_code=404, detail="Note file not found")
    return markdown_to_html(file_path.read_text(encoding='utf-8'))

# List all notes folders in the uploads/notes directory and return as a list
@router.get("/subdirectories", response_model=Dict[str, Union[str, List[str]]])
async def list_notes_directories():
    """
    List all notes directories in the notes directory
    """
    try:
        subdirectories = [d.name for d in NOTES_DIR.iterdir() if d.is_dir()]
        return {"subdirectories": subdirectories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching notes directories: {str(e)}.")


# Get content of the README.md file in the notes directory and convert to HTML
@router.get("/{subdirectory:path}/readme", response_model=NoteResponse)
async def get_readme(subdirectory: str):
    """
    Get content of README.md file in the notes directory and convert to HTML
    """
    base_path = NOTES_DIR / subdirectory
    await _validate_notes_directory(base_path)
    try:
        readme_files = list((base_path).glob("README.md"))
        if readme_files:
            readme_path = readme_files[0]
            html = await  _convert_markdown_file_to_html(readme_path)
            return html
        else:
            raise HTTPException(status_code=404, detail="README file not found")

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching README file.{str(e)}")
            
            
# Get content of specified markdown file and convert to HTML   
@router.get("/{subdirectory:path}/{note_file:path}", response_model=NoteResponse)
async def get_note(subdirectory: str, note_file: str):
    """
    Get content of specified markdown file and convert to HTML
    """
    try:
        note_path = NOTES_DIR.joinpath(subdirectory, f"{note_file}")

        if not note_path.exists() or not note_path.is_file() or not note_path.suffix == ".md":
            raise HTTPException(status_code=404, detail="Note file not found")

        html = markdown_to_html(note_path.read_text(encoding='utf-8'))
        return html

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get note: {str(e)}")