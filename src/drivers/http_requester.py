import requests
from typing import Dict
from src.drivers.interfaces.http_requester_interface import HttpRequesterInterface

class HttpRequester(HttpRequesterInterface):
    """Gerencia conexões e buscas de páginas via HTTP."""
    
    def __init__(self) -> None:
        self._base_url = (
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

    def fetch(self, offset: int = 1) -> requests.Response:
        """Faz a chamada técnica ao site e retorna a resposta bruta."""
        url = self._base_url if offset == 1 else f"{self._base_url}_Desde_{offset}"
        
        response = self._session.get(url, timeout=10) 
        response.raise_for_status()
        return response
        
    def request_from_page(self, offset: int = 1) -> Dict[str, str | int]:
        """Busca o conteúdo da página e organiza em um dicionário."""
        response = self.fetch(offset)
        if not response: return None
    
        return {
            "status_code": response.status_code,
            "html": response.text
        }