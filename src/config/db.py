import os
from dotenv import load_dotenv

load_dotenv()

class DBConfig:
    HOST = os.getenv("DB_HOST", "db")
    USER = os.getenv("DB_USER", "postgres")
    PASS = os.getenv("DB_PASS", "postgres")
    NAME = os.getenv("DB_NAME", "ecommerce_monitoring-etl-db")
    PORT = int(os.getenv("DB_PORT", 5432))
    
    @classmethod
    def get_connection_string(cls):
        return f"postgresql://{cls.USER}:{cls.PASS}@{cls.HOST}:{cls.PORT}/{cls.NAME}"