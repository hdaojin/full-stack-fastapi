# /full-stack-fastapi/main.py

from fastapi import FastAPI
from app.main import app as api_app
from ssr.main import ssr_app

app = FastAPI()

app.mount("/backend", api_app)
app.mount("/", ssr_app)


# Start the app with the command: uv run fastapi dev main:main_app