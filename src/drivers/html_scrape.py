from typing import List, Dict
from bs4 import BeautifulSoup
from .interfaces.html_scrape_interface import HtmlScrapeInterface

class MercadoLivreParser(HtmlScrapeInterface):
    """Classe responsável por transformar HTML bruto do ML em dados estruturados."""

    @classmethod
    def extract_product_list(cls, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")

        products_items = soup.find_all("li", class_="ui-search-layout__item")
        products_information = []

        for item in products_items:
            title = item.select_one("a.poly-component__title")
            
            # Procuramos pela tag <s> que o Mercado Livre usa para preços riscados
            old_price_tag = item.select_one("s.andes-money-amount--previous span.andes-money-amount__fraction")
            price_old = old_price_tag.get_text(strip=True).replace('.', '') if old_price_tag else None
            
            # Entramos primeiro no container do preço atual para garantir o valor certo
            current_container = item.select_one("div.poly-price__current")
            price_current = None
            if current_container:
                current_tag = current_container.select_one("span.andes-money-amount__fraction")
                price_current = current_tag.get_text(strip=True).replace('.', '') if current_tag else None

            reviews = item.select(
                "span.poly-component__review-compacted span.poly-phrase-label"
            )
            
            store = item.select_one("span.poly-component__seller").replace('| ', '')

            product = {
                "title": title.get_text(strip=True),
                "link": title["href"],
                "store": store.get_text(strip=True) if store else None,
                "price_old": price_old.get_text(strip=True),
                "price_current": price_current.get_text(strip=True),
                "rating": reviews[0].get_text(strip=True) if len(reviews) > 0 else None,
                "sold": reviews[1].get_text(strip=True) if len(reviews) > 1 else None,
            }

            products_information.append(product)

        return products_information
