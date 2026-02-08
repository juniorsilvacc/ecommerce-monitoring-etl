from src.drivers.interfaces.database_interface import DatabaseDriverInterface
from sqlalchemy import create_engine
from src.infra.db import DBConfig
import time

class DatabaseDriver(DatabaseDriverInterface):
    """Gerencia a conexão e a escrita de dados no banco PostgreSQL."""
    
    def __init__(self):
        self._connection_string = DBConfig.get_connection_string()
        self._engine = None

    def get_engine(self):
        """Cria a conexão com o banco de dados usando as configurações de ambiente."""
        if self._engine is None:
            # Tenta conectar até 5 vezes antes de desistir
            for i in range(5):
                try:
                    engine = create_engine(self._connection_string)
                    with engine.connect() as conn:
                        self._engine = engine
                        return self._engine
                except Exception as e:
                    print(f"⚠️ Aguardando banco de dados... (Tentativa {i+1}/5)")
                    time.sleep(3)
            
            raise Exception("❌ Não foi possível conectar ao banco de dados após várias tentativas")
        return self._engine

    def save_dataframe(self, df, table_name, if_exists='append'):
        """Envia os dados do Pandas diretamente para uma tabela no banco."""
        engine = self.get_engine()
        
        try:
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=1000 # Carrega em blocos para não travar a memória
            )
            print(f"✅ Dados persistidos no banco na tabela: {table_name}")
        except Exception as e:
            print(f"❌ Erro ao salvar no banco: {e}")
            raise e