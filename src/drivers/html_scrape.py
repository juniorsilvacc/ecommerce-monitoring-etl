import re
from typing import List, Dict
from bs4 import BeautifulSoup
from src.drivers.interfaces.html_scrape_interface import HtmlScrapeInterface

class MercadoLivreParser(HtmlScrapeInterface):
    """Classe responsável por transformar HTML bruto do ML em dados estruturados."""
    
    @staticmethod
    def _extract_price(item) -> str | None:
        """Extrai o valor de qualquer container de preço"""
        if not item:
            return None
        
        fraction_tag = item.select_one(".andes-money-amount__fraction")
        cents_tag = item.select_one(".andes-money-amount__cents")
        
        if not fraction_tag:
            return None

        value = fraction_tag.get_text(strip=True).replace('.', '')

        cents = cents_tag.get_text(strip=True) if cents_tag else "00"
        
        return f"{value}.{cents}"
    
    @staticmethod
    def _extract_product_id(link: str) -> str:
        """Extrai o ID (MLB+números) de uma URL do Mercado Livre."""
        if not link:
            return None
        
        match = re.search(r'(MLB\d+)', link)
    
        if match:
            return match.group(1)
        
        return None

    @classmethod
    def extract_product_list(cls, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")

        products_items = soup.find_all("li", class_="ui-search-layout__item")
        products_information = []

        for item in products_items:
            # Título
            title_tag = item.select_one("a.poly-component__title")
            title = (title_tag.get_text(strip=True) if title_tag else None)
            
            if not title:
                continue
            
            # Link
            link = title_tag.get("href")
            
            # Loja
            store_tag = item.select_one("span.poly-component__seller")
            store = (store_tag.get_text(strip=True) if store_tag else None)
            
            # Extração dos container
            old_price_container = item.select_one("s.andes-money-amount--previous")
            current_price_container = item.select_one("div.poly-price__current")
            
            # Valor antigo
            price_old = cls._extract_price(old_price_container)
            
            # Valor atual
            price_current = cls._extract_price(current_price_container)
            
            # Envio
            shipping_tag = item.select_one("div.poly-component__shipping")
            shipping = None
            if shipping_tag:
                shipping = (shipping_tag.get_text(separator=" ", strip=True) if shipping_tag else None)

            # Avaliações
            labels  = item.select(
                "span.poly-component__review-compacted span.poly-phrase-label"
            )
            rating = (labels[0].get_text(strip=True) if len(labels) > 0 else None)
            
            # Vendas
            sold_raw = (labels[1].get_text(strip=True).replace("| ", "") if len(labels) > 1 else None)

            product = {
                "product_id": cls._extract_product_id(link),
                "title": title,
                "link": link,
                "store": store,
                "price_old": price_old,
                "price_current": price_current,
                "shipping": shipping,
                "rating": rating,
                "sold_raw": sold_raw,
            }

            products_information.append(product)

        return products_information
