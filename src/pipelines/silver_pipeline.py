from src.stages.load.mercadolivre_load import MercadoLivreLoad

class SilverPipeline:
    def __init__(self, transform):
        self.transform = transform
        self.load = MercadoLivreLoad()

    def run(self):
        print(f"\n🥈 Iniciando processamento: Bronze -> Silver")
        
        df = self.transform.transform()
        
        success = self.load.load(df)
        
        if success:
            print(f"✅ Pipeline Silver finalizado com sucesso.")
        else:
            print(f"⚠️ Aviso: Nenhum dado novo foi processado ou carregado.")