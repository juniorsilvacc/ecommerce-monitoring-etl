# 🛠️ Ambiente de Desenvolvimento

## Isolamento do Ambiente
Utilizamos o `venv` para garantir que as versões das bibliotecas não conflitem com outros projetos.

```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt
```

## Pacotes Utilizados
- `requests` Comunicação com a API/Site.
- `beautifulsoup4` Parsing robusto de HTML.
- `pandas` Motor de transformação e limpeza de dados.
- `pyarrow` Engine necessária para a persistência em formato Parquet (Camada Silver).

## Organização do Data Lake Local
O projeto utiliza o conceito de partições temporais. A estrutura de pastas é gerada automaticamente pelo pipeline:

```text
data/
├── bronze/         # Dados brutos (Imutáveis)
│   └── mercadolivre/YYYY-MM-DD/*.json
└── silver/         # Dados limpos e tipados
    └── mercadolivre/YYYY-MM-DD/*.parquet
```

## Gestão de Dependências
Para garantir a rastreabilidade das versões, sempre que instalar um pacote novo, atualize o arquivo de requisitos

```bash
pip freeze > requirements.txt
```