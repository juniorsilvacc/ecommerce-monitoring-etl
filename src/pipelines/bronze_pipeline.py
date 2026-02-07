import os
from datetime import datetime

class BronzePipeline:
    def __init__(self, extract):
        self.extract = extract

    def run(self):
        today = datetime.now().strftime("%Y-%m-%d")
        bronze_dir = f"data/bronze/mercadolivre/{today}"
        
        if os.path.exists(bronze_dir) and any(f.endswith('.json') for f in os.listdir(bronze_dir)):
            print(f"\n⏩ Extração de hoje ({today}) encontrada. Pulando extração...")
        else:
            print(f"\n🥉 Iniciando extração do Mercado Livre para {today}...")
            
            self.extract.extract()
            
            print(f"✅ Extração concluída com sucesso.")