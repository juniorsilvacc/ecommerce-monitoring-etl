import requests
from typing import Dict
from .interfaces.http_requester_interface import HttpRequesterInterface

class HttpRequester(HttpRequesterInterface):
    def __init__(self) -> None:
        self._url = (
            "https://lista.mercadolivre.com.br/_Container_household-appliances"
        )

        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        self._session = requests.Session()
        self._session.headers.update(self._headers)

    def fetch(self) -> requests.Response:
        response = self._session.get(self._url, timeout=10) 
        response.raise_for_status()
        
        return response
       
    def request_from_page(self) -> Dict[str, str | int]:
        response = self.fetch()
        
        if response is None:
            return None
    
        return {
            "status_code": response.status_code,
            "html": response.text
        }