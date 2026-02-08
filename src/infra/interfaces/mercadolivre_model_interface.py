from abc import ABC, abstractmethod
from typing import Dict

class MercadoLivreProdutoInterface(ABC):
    
    @abstractmethod
    def get_columns(cls) -> list:
        pass
    
    @abstractmethod
    def get_schema_dict(cls) -> Dict[str, str]:
        pass
