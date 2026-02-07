from typing import List, Dict
from abc import ABC, abstractmethod

class DatabaseDriverInterface(ABC):
    
    @abstractmethod
    def get_engine(self):
        pass
    
    @abstractmethod
    def save_dataframe(self, df, table_name, if_exists='append'):
        pass
