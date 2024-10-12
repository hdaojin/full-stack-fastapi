# import uuid
from pydantic import BaseModel

class NoteResponse(BaseModel):
    meta: dict
    toc: str
    content: str