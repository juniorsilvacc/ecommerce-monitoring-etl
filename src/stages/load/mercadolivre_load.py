from src.drivers.database import DatabaseDriver

class MercadoLivreLoad:
    def __init__(self):
        self.db_driver = DatabaseDriver()

    def load(self, df):
        """Executa a carga dos dados transformados para a Camada Gold (Postgres)."""
        
        if df is not None and not df.empty:
            print(f"🚀 Carregando {len(df)} registros no banco de dados...")
            self.db_driver.save_dataframe(df, table_name="mercadolivre_produtos")
            return True
        return False