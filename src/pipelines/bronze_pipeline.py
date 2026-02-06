import os
from datetime import datetime

class BronzePipeline:
    def __init__(self, extract):
        self.extract = extract

    def run(self):
        today = datetime.now().strftime("%Y-%m-%d")
        bronze_dir = f"data/bronze/mercadolivre/{today}"
        
        if os.path.exists(bronze_dir) and any(f.endswith('.json') for f in os.listdir(bronze_dir)):
            print(f"✅ Extração de hoje ({today}) já encontrada. Pulando para Transformação...")
        else:
            print("🚀 Iniciando transformação Bronze...")
            self.extract.extract()
            print(f"Dados extraidos e salvos com sucesso ✅")