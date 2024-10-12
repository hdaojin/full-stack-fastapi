from fastapi import APIRouter

from app.api.routes import notes
from app.api.routes import pages

api_router = APIRouter()
api_router.include_router(pages.router, prefix="/pages")
api_router.include_router(notes.router, prefix="/notes")