from ssr.services.api_service import ApiService

class NoteService:
    @staticmethod
    async def get_note_data(endpoint: str):
        return await ApiService.get(endpoint)