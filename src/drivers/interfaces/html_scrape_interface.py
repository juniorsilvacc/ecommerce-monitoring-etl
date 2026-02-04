from typing import List, Dict
from abc import ABC, abstractmethod

class HtmlScrapeInterface(ABC):
    
    @abstractmethod
    def extract_product_list(cls, html: str) -> List[Dict[str, str]]:
        pass