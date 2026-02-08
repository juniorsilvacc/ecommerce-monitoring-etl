import os
import pandas as pd
from datetime import datetime
from src.utils.file_handler import save_to_silver
from src.infra.mercadolivre_model import MercadoLivreProduto

class MercadoLivreTransform():
    def __init__(self, date_ref: str = None):
        self.date_ref = date_ref or datetime.now().strftime("%Y-%m-%d")
        self.source_path = os.path.join("data", "bronze", "mercadolivre", self.date_ref)
    
    def transform(self):
        """Executa o fluxo de transformação e retorna todos os dados limpos, organizados e padronizados."""
        
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
            'sold_raw': 'quantidade_vendida'
        })
        
        # 2. LIMPEZA E CONVERSÃO DE TIPOS (Cast)
        df['produto_id'] = df['produto_id'].astype(str)
        df['titulo'] = df['titulo'].astype(str).str.strip()
        df['loja'] = df['loja'].astype(str).str.strip()
        df['envio'] = df['envio'].astype(str).str.strip()
        df['preco_antigo'] = pd.to_numeric(df['preco_antigo'], errors='coerce')
        df['preco_atual'] = pd.to_numeric(df['preco_atual'], errors='coerce')
        df['avaliacao'] = pd.to_numeric(df['avaliacao'], errors='coerce')
        
        if 'quantidade_vendida' in df.columns:
            df['quantidade_vendida'] = df['quantidade_vendida'].astype(str).str.lower().str.strip()
            # Identifica quem tem a palavra "mil" antes de removê-la. Cria uma 'máscara' listando em Verdadeiro ou Falso.
            has_a_thousand = df['quantidade_vendida'].str.contains('mil', na=False)
            # Remove tudo que NÃO é número (limpa o "+", "mil", "quantidade_vendidas", etc...)
            df['quantidade_vendida'] = df['quantidade_vendida'].str.replace(r'[^\d]', '', regex=True) 
            # Multiplica por 1000 apenas onde a palavra "mil" existia
            df['quantidade_vendida'] = pd.to_numeric(df['quantidade_vendida'], errors='coerce').fillna(0) 
            df.loc[has_a_thousand, 'quantidade_vendida'] = df.loc[has_a_thousand, 'quantidade_vendida'] * 1000
            df['quantidade_vendida'] = df['quantidade_vendida'].astype(int)
        
        # 3. TRATAMENTO DE VALORES NULOS (Fillna ou Dropna)
        df['loja'] = df['loja'].replace('None', 'Não Informado').fillna('Não Informado')
        df['preco_antigo'] = df['preco_antigo'].fillna(df['preco_atual'])
        df['envio'] = df['envio'].replace('None', 'Consultar Frete').fillna('Consultar Frete')
        df['avaliacao'] = df['avaliacao'].fillna(0.0)
        
        # 4. MÉTRICAS
        # Cálculo de Desconto (Indicador de Oferta)
        # clip(lower=0.01) para evitar divisão por zero se o preço antigo estiver bugado
        df['percentual_desconto'] = (
            (df['preco_antigo'] - df['preco_atual']) / df['preco_antigo'].clip(lower=0.01)
        ).round(4)
        
        # Faturamento Estimado (Métrica de Volume Financeiro)
        df['faturamento_estimado'] = (df['preco_atual'] * df['quantidade_vendida']).round(2)
        
        # Score de Relevância (KPI)
        df['score_oportunidade'] = (df['avaliacao'] * df['quantidade_vendida']).round(2)
        
        # 5. APLICAÇÃO DO MODELO
        # Garante que o DF tenha apenas as colunas do Model e na ordem certa
        df = df.reindex(columns=MercadoLivreProduto.get_columns())
        # Força os tipos de dados definidos no Model, evitando erro no Banco
        df = df.astype(MercadoLivreProduto.get_schema_dict())
        
        # 6. ADICIONAR METADADOS DE CONTROLE
        df['data_processamento'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 7. SALVAR
        save_to_silver(df, source='mercadolivre', format="parquet")
        
        return df