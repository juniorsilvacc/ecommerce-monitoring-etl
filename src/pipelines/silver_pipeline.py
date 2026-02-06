class SilverPipeline:
    def __init__(self, transform):
        self.transform = transform

    def run(self):
        print(f"\n[SILVER] 🥈 Iniciando processamento: Bronze -> Silver")
        
        path = self.transform.transform()
        
        if path:
            print(f"✅ Transformação concluída com sucesso!")
            print(f"🚀 Dados prontos para análise na camada Silver.")
        else:
            print(f"⚠️  Aviso: Nenhum dado novo foi processado.")