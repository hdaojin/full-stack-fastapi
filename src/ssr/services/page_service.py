from typing import Optional
from ssr.services.api_service import ApiService

class PageService:
    @staticmethod
    async def get_page(page_name: Optional[str] = None):
        path = "/pages/index" if not page_name else f"/pages/{page_name}"
        return await ApiService.get(path)