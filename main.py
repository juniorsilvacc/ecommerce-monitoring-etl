from src.pipelines.mercado_livre_pipeline import MercadoLivrePipeline

def main(): 
    # Executa o Pipeline de extração
    ml_pipeline = MercadoLivrePipeline()
    total_coletado = ml_pipeline.run()
    
    print("-" * 30)
    print(f"Sucesso! Processo finalizado.")
    print(f"Total de itens extraídos e salvos na Bronze: {total_coletado}")

if __name__ == "__main__": 
    main()