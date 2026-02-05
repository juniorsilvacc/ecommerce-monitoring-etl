from src.drivers.http_requester import HttpRequester 
from src.drivers.html_scrape import MercadoLivreParser 

def main(): 
    print("Inicializando...") 
    
    requester = HttpRequester() 
    response = requester.request_from_page() 
    
    products = MercadoLivreParser.extract_product_list(response["html"] )
    
    print(f"{len(products)} produtos coletados") 
    
    if products: 
        print(products[:5])

if __name__ == "__main__": 
    main()