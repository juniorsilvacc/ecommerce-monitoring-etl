import json
import os
import pandas as pd
from datetime import datetime

def save_to_bronze(data: list, source: str, page_number: int) -> str:
    # 1. Pega a data atual
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Monta o caminho: data/bronze/mercadolivre/YYYY-mm-d/
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

def save_to_silver(df: pd.DataFrame, source: str, format: str = "parquet") -> str:
    # 1. Pega a data atual
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Monta o caminho: data/silver/mercadolivre/YYYY-mm-d/
    base_path = os.path.join("data", "silver", source, today)
    os.makedirs(base_path, exist_ok=True)
    
    # 3. Define o nome do arquivo e salva em Parquet ou CSV
    if format == "parquet":
        filename = f"{source}_produtos_{today}.parquet"
        full_path = os.path.join(base_path, filename)
        df.to_parquet(full_path, index=False)
    else:
        filename = f"{source}_produtos_{today}.csv"
        full_path = os.path.join(base_path, filename)
        df.to_csv(full_path, index=False)
    
    return full_path