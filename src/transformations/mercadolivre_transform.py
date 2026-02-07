import os
import pandas as pd
from datetime import datetime
from src.utils.file_handler import save_to_silver

class MercadolivreTransform():
    def __init__(self, date_ref: str = None):
        self.date_ref = date_ref or datetime.now().strftime("%Y-%m-%d")
        self.source_path = os.path.join("data", "bronze", "mercadolivre", self.date_ref)
    
    def transform(self):    
        # Carregar todos os JSONs da pasta Bronze
        all_files = []
        for f in os.listdir(self.source_path):
            if f.endswith('.json'):
                all_files.append(f)

        # Ler o conteúdo de cada arquivo
        df_list = []
        for file in all_files:
            file_path = os.path.join(self.source_path, file)
            
            # Carrega o JSON em um DataFrame e adiciona em uma lista para cosolidar todos
            df_list.append(pd.read_json(file_path))
            
        # Une todos os arquivos em um único em um DataFrame
        if len(df_list) > 0:
            df = pd.concat(df_list, ignore_index=True)
        else:
            print("Aviso: Nenhum dado encontrado para transformar.")
            return None
        
        # 1. RENOMEAR COLUNAS (Padronização)
        df = df.rename(columns={
            'product_id': 'produto_id',
            'title': 'titulo',
            'store': 'loja',
            'price_old': 'preco_antigo',
            'price_current': 'preco_atual',
            'shipping': 'envio',
            'rating': 'avaliacao',
            'sold_raw': 'vendido'
        })
        
        # 2. LIMPEZA E CONVERSÃO DE TIPOS (Cast)
        df['produto_id'] = df['produto_id'].astype(str)
        df['titulo'] = df['titulo'].astype(str).str.strip()
        df['loja'] = df['loja'].astype(str).str.strip()
        df['envio'] = df['envio'].astype(str).str.strip()
        df['preco_antigo'] = pd.to_numeric(df['preco_antigo'], errors='coerce')
        df['preco_atual'] = pd.to_numeric(df['preco_atual'], errors='coerce')
        df['avaliacao'] = pd.to_numeric(df['avaliacao'], errors='coerce')
        
        if 'vendido' in df.columns:
            df['vendido'] = df['vendido'].astype(str).str.lower().str.strip()
            # Identifica quem tem a palavra "mil" antes de removê-la. Cria uma 'máscara' listando em Verdadeiro ou Falso.
            has_a_thousand = df['vendido'].str.contains('mil', na=False)
            # Remove tudo que NÃO é número (limpa o "+", "mil", "vendidos", etc...)
            df['vendido'] = df['vendido'].str.replace(r'[^\d]', '', regex=True) 
            # Multiplica por 1000 apenas onde a palavra "mil" existia
            df['vendido'] = pd.to_numeric(df['vendido'], errors='coerce').fillna(0) 
            df.loc[has_a_thousand, 'vendido'] = df.loc[has_a_thousand, 'vendido'] * 1000
            df['vendido'] = df['vendido'].astype(int)
        
        # 3. TRATAMENTO DE VALORES NULOS (Fillna ou Dropna)
        df['loja'] = df['loja'].replace('None', 'Não Informado').fillna('Não Informado')
        df['preco_antigo'] = df['preco_antigo'].fillna(df['preco_atual'])
        df['envio'] = df['envio'].replace('None', 'Consultar Frete').fillna('Consultar Frete')
        df['avaliacao'] = df['avaliacao'].fillna(0.0)
        
        # 4. ADICIONAR METADADOS DE CONTROLE
        df['data_processamento'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Salvar
        save_to_silver(df, source='mercadolivre', format="parquet")
        
        return df