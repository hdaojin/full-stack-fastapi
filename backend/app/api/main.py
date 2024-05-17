from fastapi import APIRouter

from app.api.notes import notes
from app.api.pages import pages

api_router = APIRouter()
api_router.include_router(pages.router, tags=["pages"], prefix="/pages")
api_router.include_router(notes.router, tags=["notes"], prefix="/notes")