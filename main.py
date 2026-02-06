from src.extracts.mercadolivre_extract import MercadoLivreExtract
from src.transformations.mercadolivre_transform import MercadolivreTransform
from src.pipelines.bronze_pipeline import BronzePipeline
from src.pipelines.silver_pipeline import SilverPipeline
from src.drivers.http_requester import HttpRequester
from src.drivers.html_scrape import MercadoLivreParser

def main(): 
    # --- CAMADA BRONZE (EXTRAÇÃO) ---
    request = HttpRequester()
    parser = MercadoLivreParser()
    extract_tool = MercadoLivreExtract(requester=request, parser=parser)
    bronze_pipeline = BronzePipeline(extract=extract_tool)
    bronze_pipeline.run()
    
    # --- CAMADA SILVER (TRANSFORMAÇÃO) ---
    transformer = MercadolivreTransform()
    silver_pipeline = SilverPipeline(transform=transformer)
    silver_pipeline.run()

if __name__ == "__main__": 
    main()