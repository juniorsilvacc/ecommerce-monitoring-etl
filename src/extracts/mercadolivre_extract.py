import time
from src.drivers.http_requester import HttpRequester
from src.drivers.html_scrape import MercadoLivreParser
from src.utils.file_handler import save_to_bronze

class MercadoLivreExtract:
    def __init__(self, requester: HttpRequester, parser: MercadoLivreParser) -> None:
        self._requester = requester
        self._parser = parser

    def extract(self) -> int:
        """Executa o fluxo de extração e retorna o total coletado."""
        
        page = 0
        items_per_page = 48
        total_collected = 0

        while True:
            current_offset = (page * items_per_page) + 1
            try:   
                # Faz a requisição HTTP passando o offset atual
                response = self._requester.request_from_page(offset=current_offset)
                
                # Transforma o HTML da resposta em uma lista de dicionários
                products = self._parser.extract_product_list(response["html"])
                
                if not products:
                    break
                    
                # Salva os dados brutos da página atual na pasta /data/bronze/
                path = save_to_bronze(
                    data=products, 
                    source="mercadolivre", 
                    page_number=page + 1
                )
                
                # Atualiza o contador total e imprime o progresso no terminal
                total_collected += len(products)
                print(f"Página {page + 1} salva em: {path}")
                
                # Incrementa para a próxima página e espera 1 segundo
                page += 1
                time.sleep(1)

            except Exception as e:
                # Tratamento específico para o limite de paginação
                if "404" in str(e):
                    print("Limite de páginas atingido.")
                    break
                print(f"Erro: {e}")
                break
            
        return total_collected