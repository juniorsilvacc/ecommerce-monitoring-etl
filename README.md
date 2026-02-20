# 📦 Ecommerce Monitoring ETL – Mercado Livre

Pipeline de dados completo para **coleta, tratamento, organização e análise** de produtos do Mercado Livre, seguindo boas práticas de **engenharia de dados** e arquitetura em camadas (**Bronze → Silver → Gold**).

Este projeto simula um cenário real de monitoramento de e-commerce, com foco em rastreabilidade, padronização e escalabilidade.

## 🚀 Objetivo do Projeto

Construir um pipeline ETL capaz de:

- Coletar dados de produtos do Mercado Livre
- Armazenar dados brutos preservando a origem
- Tratar, padronizar e enriquecer os dados
- Preparar os dados para análise e BI
- Manter histórico e rastreabilidade

## 📐 Arquitetura

<img width="1750" height="874" alt="Image" src="https://github.com/user-attachments/assets/c8b6aab3-e5b6-4187-aba1-20263ced67fe" />

## 💎 Padrão de Design de Dados

### `O projeto segue o padrão Medallion Architecture`

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

## 📂 Estrutura do Projeto

```text
ecommerce-monitoring-etl/
├── src/
│   ├── drivers/                            # Tecnologia bruta (Requests, BS4, SQLAlchemy)
│   │   ├── database.py
│   │   ├── http_requester.py
│   │   ├── html_scrape.py
│   │   └── interfaces/                     # Contratos para garantir flexibilidade
│   │       ├── db_interface.py
│   │       ├── http_interface.py
│   │       └── scrape_interface.py
│   │
│   ├── stages/                             # Estágios das Camadas de Dados (Bronze, Silver e Gold)
│   │   ├── extract/                        # Coleta e salva na Bronze
│   │   ├── transform/                      # Limpa, Transforma e Organiza e salva na Silver
│   │   └── load/                           # Persistência final na Gold (Postgres)
│   │
│   ├── pipelines/                          # Orquestração dos fluxos de dados
│   │   ├── bronze_pipeline.py              # Extract -> Extração (Bronze)
│   │   └── silver_pipeline.py              # Transform -> Transformação -> Load (Silver/Gold)
│   │
│   ├── infra/                              # Configurações de sistema e modelos
│   │   ├── mercadolivre_model.py           # O "molde" dos dados (Schemas)
│   │   └── db_config.py                    # Strings de conexão e setup do banco
│   │
│   └── utils/                              # Utilitários
│       └── file_handler.py                 # Leitura/Escrita de arquivos físicos
│
├── data/                                   # Camadas de arquivos (Lake Local)
│   ├── bronze/                             # Dados brutos (Imutáveis)
│   └── silver/                             # Dados limpos (Tratados)
│
├── docs/                                   # Documentação técnica completa
│   ├── architecture.md                     # Desenho da solução
│   ├── setup.md                            # Como rodar (Docker/Local)
│   ├── data_model.md                       # Dicionário de dados
│   └── analytics_metrics.md                # Explicação dos KPIs (Desconto, Faturamento)
│
├── .env                                    # Variáveis sensíveis (não commitado)
├── .gitignore                              # Ignorar venv, data/ e .env
├── Dockerfile                              # Receita da imagem
├── docker-compose.yml                      # Orquestra App + PostgreSQL
├── main.py                                 # Ponto de partida
├── README.md                               # Guia rápido do projeto
└── requirements.txt                        # Dependências do projeto
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- **Requests**
- **BeautifulSoup4**
- **Pandas**
- **Parquet**
- **Virtualenv**
- **SQLAlchemy**
- **Docker**

## 🔄 Pipeline ETL

### 1️⃣ Extração (Extract) 📥

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

### 2️⃣ Transformação (Transform) ⚙️

Principais regras aplicadas:

- Padronização de nomes (inglês → português)
- Conversão de tipos
- Tratamento de valores nulos
- Interpretação de dados textuais
- Criação de metadados

📄 Detalhes completos em `docs/transformations.md`

---

### 3️⃣ Carga (Load) 📤

- Escrita otimizada em Parquet
- Organização por fonte
- Histórico preservado
- Pronto para análise e BI

📁 Saída: `data/silver/mercadolivre/`

## 📊 Modelo de Dados (Silver)

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
| quantidade_vendida | int | Quantidade vendida |
| envio  | string  | Info de frete |
| percentual_desconto  | float  | Indicador de % de desconto aplicado |
| faturamento_estimado | float  | Métrica: preco_atual * vendido |
| score_oportunidade  | float  | KPI: avaliacao * vendido |
| data_processamento | timestamp | Data e hora em que o dado foi tratado |

📄 Detalhes completos em `docs/data_model.md`

## ▶️ Como Executar o Projeto

### 🐳 Ambiente Docker (RECOMENDADO)

Comandos Principais:

```bash
# 1. Primeira execução ou após mudanças no código/dependências
# (Constrói a imagem e sobe os containers)
docker compose up --build

# 2. Reexecutar o ETL (sem precisar reconstruir tudo)
# O parâmetro -a exibe os logs no terminal em tempo real
docker start -a etl_app_container

# 3. Parar os containers mantendo os dados do banco
docker compose stop
```

### 🐍 Ambiente Local
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

Caso precise verificar a saúde dos serviços ou inspecionar os dados persistidos:

```bash
# Verificar se os containers estão rodando e a saúde (healthcheck) do banco
docker ps

# Acessar os logs do banco de dados em caso de erro de conexão
docker logs ecommerce_db_container

# Acessar o terminal interativo do PostgreSQL para rodar queries SQL
docker exec -it ecommerce_db_container psql -U postgres -d ecommerce_monitoring-etl-db

# Limpar o ambiente completamente (remove containers, imagens e VOLUMES de dados)
# CUIDADO: Isso apagará seu banco de dados!
docker compose down -v
```

👨‍💻 Autor

Projeto desenvolvido por Junior Silva
