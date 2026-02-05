import time
from src.drivers.http_requester import HttpRequester
from src.drivers.html_scrape import MercadoLivreParser
from src.utils.file_handler import save_to_bronze

class MercadoLivrePipeline:
    def __init__(self):
        self.requester = HttpRequester()
        self.parser = MercadoLivreParser()

    def run(self):
        page = 0
        items_per_page = 48
        total_collected = 0

        while True:
            current_offset = (page * items_per_page) + 1
            try:   
                response = self.requester.request_from_page(offset=current_offset)
                products = self.parser.extract_product_list(response["html"])
                
                if not products:
                    break
                    
                # Salva a página atual na Bronze
                path = save_to_bronze(
                    data=products, 
                    source="mercadolivre", 
                    page_number=page + 1
                )
                
                total_collected += len(products)
                print(f"Página {page + 1} salva em: {path}")
                
                page += 1
                time.sleep(1)

            except Exception as e:
                if "404" in str(e):
                    print("Limite de páginas atingido.")
                    break
                print(f"Erro: {e}")
                break
            
        return total_collected