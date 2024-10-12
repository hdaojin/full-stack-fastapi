from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ssr.core.path_config import STATIC_DIR

from ssr.routes import pages, notes

ssr_app = FastAPI()


ssr_app.include_router(notes.router, tags=["notes"])
# ssr_app.include_router(pages.router, tags=["index", "pages"])

ssr_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")