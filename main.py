from src.pipelines.mercado_livre_pipeline import MercadoLivrePipeline
from src.drivers.http_requester import HttpRequester
from src.drivers.html_scrape import MercadoLivreParser

def main(): 
    print("Iniciando extração dos dados...")
    
    # Instanciar os Drivers
    request = HttpRequester()
    parser = MercadoLivreParser()
    
    # Injeta os drivers no pipeline
    ml_pipeline = MercadoLivrePipeline(requester=request, parser=parser)
    
    # Execução do processo
    total_coletado = ml_pipeline.run()
    
    print("-" * 30)
    print(f"Sucesso! Processo finalizado.")
    print(f"Total de itens extraídos e salvos na Bronze: {total_coletado}")

if __name__ == "__main__": 
    main()