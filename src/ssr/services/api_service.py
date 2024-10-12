# Desc: API service for fetching data from the server using httpx
# app/ssr/services/api_service.py
import httpx
from typing import Any, Optional


class ApiService:
    BASE_URL = "http://127.0.0.1:8000/backend/api/v1"

    @staticmethod
    async def get(endpoint: str, params: Optional[dict] = None) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ApiService.BASE_URL}{endpoint}", params=params)
                response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
                data = response.json()
        except (httpx.RequestError, httpx.HTTPStatusError):
            data = {"error_message": "An error occurred while requesting data."}
        # except httpx.RequestError as e:
        #     data = {"error_message": f"An error occurred while requesting {e.request.url!r}."}
        # except httpx.HTTPStatusError as e:
        #     data = {"error_message": f"Error response {e.response.status_code} while requesting {e.request.url!r}."}
        return data
        

        
    @staticmethod
    async def post(endpoint: str, data: dict) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{ApiService.BASE_URL}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        
    @staticmethod
    async def put(endpoint: str, data: dict) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{ApiService.BASE_URL}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        
    @staticmethod
    async def delete(endpoint: str) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{ApiService.BASE_URL}{endpoint}")
            response.raise_for_status()
            return response.json()
        
    @staticmethod
    async def patch(endpoint: str, data: dict) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{ApiService.BASE_URL}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        