import requests
from typing import Dict
from abc import ABC, abstractmethod

class HttpRequesterInterface(ABC):
   
    @abstractmethod
    def fetch(self, offset: int = 1) -> requests.Response:
        pass
    
    @abstractmethod
    def request_from_page(self, offset: int = 1) -> Dict[str, str | int]:
        pass
