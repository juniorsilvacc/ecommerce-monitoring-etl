# 📦 Ecommerce Monitoring ETL – Mercado Livre

Pipeline de dados completo para **coleta, tratamento, organização e análise** de produtos do Mercado Livre, seguindo boas práticas de **engenharia de dados** e arquitetura em camadas (**Bronze → Silver → Gold**).

Este projeto simula um cenário real de monitoramento de e-commerce, com foco em rastreabilidade, padronização e escalabilidade.

## 🎯 Objetivo do Projeto

Construir um pipeline ETL capaz de:

- Coletar dados de produtos do Mercado Livre
- Armazenar dados brutos preservando a origem
- Tratar, padronizar e enriquecer os dados
- Preparar os dados para análise e BI
- Manter histórico e rastreabilidade

## 🏗️ Arquitetura de Dados

### O projeto segue o padrão **Medallion Architecture**:

### Bronze 🥉
- Dados brutos
- Sem perda de informação
- Formato JSON
- Estrutura próxima à origem

### Silver 🥈
- Dados tratados e padronizados
- Conversão de tipos
- Aplicação de regras de negócio
- Formato Parquet

### Gold 🥇
- Dados prontos para análise
- Métricas e agregações
- Dashboards e KPIs

📄 Documentação detalhada disponível em `docs/architecture.md`

## Estrutura do Projeto

```text
ecommerce-monitoring-etl/
│
├── src/
│ ├── drivers/
│ │ ├── http_requester.py
│ │ ├── html_scrape.py 
│ │ └── interfaces/
│ │ └── http_requester_interface.py
│ │ └── html_scrape_interface.py
│ │
│ ├── transforms/
│ │ └── mercadolivre_transform.py
│ │
│ ├── extracts/
│ │ └── mercadolivre_extract.py
│ │
│ ├── pipelines/
│ │ └── bronze_pipeline.py
│ │ └── silver_pipeline.py
│ │
│ ├── utils/
│ │ └── file_handler.py
│ │
│ └── main.py
│
├── data/
│ ├── bronze/
│ │ └── mercadolivre/
│ │ └── *.json
│ │
│ ├── silver/
│ │ └── mercadolivre/
│ │ └── *.parquet
│
├── docs/
│ ├── architecture.md
│ ├── transformations.md
│ └── data_model.md
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## 🛠 Tecnologias Utilizadas

- **Python 3.12**
- **Requests**
- **BeautifulSoup4**
- **Pandas**
- **Parquet**
- **Virtualenv**

## 🔄 Pipeline ETL

### 1️⃣ Extração (Extract)

- Requisições HTTP simulando navegador
- Paginação controlada
- Parsing com BeautifulSoup
- Extração de:
  - Produto
  - Preço
  - Avaliação
  - Loja
  - Quantidade vendida
  - Envio

📁 Saída: `data/bronze/mercadolivre/YYYY-MM-DD/*.json`

---

### 2️⃣ Transformação (Transform)

Principais regras aplicadas:

- Padronização de nomes (inglês → português)
- Conversão de tipos
- Tratamento de valores nulos
- Interpretação de dados textuais
- Criação de metadados

Exemplo:
- `"+10 mil vendidos"` → `10000`
- `preco_antigo = null` → produto sem promoção

📄 Detalhes completos em `docs/transformations.md`

---

### 3️⃣ Carga (Load)

- Escrita otimizada em Parquet
- Organização por fonte
- Histórico preservado
- Pronto para análise e BI

📁 Saída: `data/silver/mercadolivre/`

## 🧩 Modelo de Dados (Silver)

Cada registro representa **um produto em um momento específico**.

Principais campos:

| Coluna            | Tipo    | Descrição |
|------------------|---------|----------|
| produto_id       | string  | ID do produto |
| titulo           | string  | Nome do produto |
| loja             | string  | Vendedor |
| preco_atual      | float   | Preço vigente |
| preco_antigo     | float   | Preço original |
| avaliacao        | float   | Nota média |
| vendido          | int     | Quantidade vendida |
| envio            | string  | Info de frete |
| data_processamento | timestamp | Controle ETL |

📄 Detalhes completos em `docs/data_model.md`

## ▶️ Como Executar o Projeto

```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt

# Executa o main.py
python3 main.py
```

👨‍💻 Autor

Projeto desenvolvido por **Junior Silva**.
