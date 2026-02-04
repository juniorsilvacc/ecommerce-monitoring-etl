from src.drivers.http_requester import HttpRequester 
from src.drivers.html_scrape import MercadoLivreParser 

def main(): 
    print("Inicializando...") 
    
    requester = HttpRequester() 
    response = requester.request_from_page() 
    
    html = response["html"] 
    
    products = MercadoLivreParser.extract_product_list(html)
    
    print(f"{len(products)} produtos coletados") 
    
    for product in products[:5]: 
        print(product)
        
    print(type(products))
    print(products)

if __name__ == "__main__": 
    main()