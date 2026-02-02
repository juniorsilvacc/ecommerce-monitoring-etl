import requests
from typing import Dict

class HttpRequester:
    def __init__(self) -> None:
        self._url = (
            "https://lista.mercadolivre.com.br/_Container_household-appliances"
        )

        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
        }

        # Cria uma sessão HTTP (Mantém cookies, ou seja, abre uma navegador e mantê-lo aberto).
        self._session = requests.Session()
        
        # Aplica os headers na sessão, toda requisição feita pela sessão usará esses headers automaticamente.
        self._session.headers.update(self._headers)

    def fetch(self) -> requests.Response:
        # Usa a sessão, usa headers automaticamente e espera no máximo 10 segundos (Evita que o programa trave).
        response = self._session.get(self._url, timeout=10)
        response.raise_for_status()
        return response

    def request_from_page(self) -> Dict[str, str | int]:
        response = self.fetch()
        
        return {
            "status_code": response.status_code,
            "html": response.text[:500]
        }
