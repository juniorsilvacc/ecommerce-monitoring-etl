from dataclasses import dataclass
from typing import Dict

@dataclass
class MercadoLivreProduto:
    """Contrato de dados que define a estrutura da camada Silver e Gold."""

    @classmethod
    def get_columns(cls) -> list:
        """Lista oficial de colunas para o banco de dados."""
        return [
            "produto_id", 
            "titulo", 
            "link", 
            "loja", 
            "preco_antigo", 
            "preco_atual", 
            "envio", 
            "avaliacao", 
            "quantidade_vendida",
            "percentual_desconto",
            "faturamento_estimado",
            "score_oportunidade",
            "data_processamento"
        ]

    @classmethod
    def get_schema_dict(cls) -> Dict[str, str]:
        """Mapeamento de tipos para garantir integridade no PostgreSQL."""
        return {
            "produto_id": "string",
            "titulo": "string",
            "link": "string",
            "loja": "string",
            "preco_antigo": "float64",
            "preco_atual": "float64",
            "envio": "string",
            "avaliacao": "float64",
            "quantidade_vendida": "int64",
            "percentual_desconto": "float64",
            "faturamento_estimado": "float64",
            "score_oportunidade": "float64",
            "data_processamento": "datetime64[ns]"
        }