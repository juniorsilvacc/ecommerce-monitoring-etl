import requests
from typing import Dict
from abc import ABC, abstractmethod

class HttpRequesterInterface(ABC):
   
    @abstractmethod
    def fetch(self) -> requests.Response:
        pass
    
    @abstractmethod
    def request_from_page(self) -> Dict[str, str | int]:
        pass
