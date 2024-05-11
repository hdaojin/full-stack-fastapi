from fastapi import APIRouter

from app.api.notes import notes

api_router = APIRouter()
api_router.include_router(notes.router, tags=["notes"], prefix="/notes")