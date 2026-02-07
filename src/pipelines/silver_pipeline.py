from src.drivers.database import DatabaseDriver

class SilverPipeline:
    def __init__(self, transform):
        self.transform = transform
        self.db_driver = DatabaseDriver()

    def run(self):
        print(f"\n🥈 Iniciando processamento: Bronze -> Silver")
        
        df = self.transform.transform()
        
        if df is not None:
            self.db_driver.save_dataframe(df, table_name="mercadolivre_produtos")
            
            print(f"✅ Pipeline Silver finalizado com sucesso.")
        else:
            print(f"⚠️ Aviso: Nenhum dado novo foi processado.")