from typing import List, Dict
from abc import ABC, abstractmethod

class HtmlScrapeInterface(ABC):
    
    @abstractmethod
    def _extract_price(item) -> str | None:
        pass
    
    @abstractmethod
    def _extract_product_id(link: str) -> str:
        pass
    
    @abstractmethod
    def extract_product_list(cls, html: str) -> List[Dict[str, str]]:
        pass