import json
import os
from datetime import datetime

def save_to_bronze(data: list, source: str, page_number: int):
    # 1. Pega a data atual para a pasta
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Monta o caminho: data/bronze/mercadolivre/2026-02-03/
    base_path = os.path.join("data", "bronze", source, today)
    
    # 3. Cria as pastas se não existirem (o exist_ok=True evita erros)
    os.makedirs(base_path, exist_ok=True)
    
    # 4. Define o nome do arquivo: produtos_page_1.json
    filename = f"produtos_ml_page_{page_number}.json"
    full_path = os.path.join(base_path, filename)
    
    # 5. Salva o arquivo
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    return full_path