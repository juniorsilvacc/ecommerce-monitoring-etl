# 🛠️ Setup do Projeto
Este projeto utiliza uma arquitetura de Medallion Lakehouse local e persistência em banco de dados relacional para análise.

## Ambiente de Execução (Local)
Utilizamos o `venv` para garantir que as versões das bibliotecas não conflitem com outros projetos.

```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt
```

## Ambiente de Execução (Docker)
Ideal para produção ou simulação de ambiente real. Garante que o banco de dados e a aplicação rodem em containers isolados.

```bash
# Primeira execução. Sobe o banco PostgreSQL e executa o ETL automaticamente
docker compose up --build

# Reexecutar o ETL, sem precisar reconstruir tudo
docker start -a etl_app_container
```

## Variáveis de Ambiente (.env)
```bash
DB_HOST=db
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASS=postgres
```

## Pacotes Utilizados
- `requests` Comunicação com a API/Site.
- `beautifulsoup4` Parsing robusto de HTML.
- `pandas` Motor de transformação e limpeza de dados.
- `pyarrow` Engine necessária para a persistência em formato Parquet (Camada Silver).
- `sqlalchemy`	ORM para comunicação com o PostgreSQL
- `psycopg2-binary`	Driver de conexão com o Banco de Dados.

## Organização do Data Lake Local
O projeto utiliza o conceito de partições temporais. A estrutura de pastas é gerada automaticamente pelo pipeline:

```text
data/
├── bronze/                                 # Dados brutos (Imutáveis)
│   └── mercadolivre/YYYY-MM-DD/*.json
└── silver/                                 # Dados limpos e tipados
    └── mercadolivre/YYYY-MM-DD/*.parquet
```

## Gestão de Dependências
Para garantir a rastreabilidade das versões, sempre que instalar um pacote novo, atualize o arquivo de requisitos

```bash
pip freeze > requirements.txt
```