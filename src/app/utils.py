from fastapi import HTTPException

from pathlib import Path


# validate the directory path
async def validate_directory(path: str):
    if not Path(path) or not Path(path).is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

