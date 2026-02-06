class SilverPipeline:
    def __init__(self, transform):
        self.transform = transform

    def run(self):
        print("🥈 Iniciando transformação Bronze -> Silver...")
        
        self.transform.transform()
        
        print(f"Dados transformados e salvos com sucesso ✅")