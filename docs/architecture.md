# 📐 Architecture Overview – Ecommerce Monitoring ETL

## Objetivo do Projeto

Este projeto tem como objetivo coletar, estruturar, transformar e disponibilizar
dados de produtos do Mercado Livre para fins de análise de preços, vendas,
descontos e comportamento de mercado.

A arquitetura foi pensada para ser:
- simples
- escalável
- rastreável
- alinhada a boas práticas de engenharia de dados

## Visão Geral da Arquitetura

O projeto segue um modelo inspirado em **ELT (Extract, Load, Transform)**,
com separação clara de responsabilidades entre coleta, armazenamento e tratamento
dos dados.

A estrutura principal é dividida em:

- Drivers (coleta e parsing)
- Camada de dados (Bronze / Silver / Gold)
- Transformações
- Análise (notebooks)

## Estrutura de Pastas

```text
ecommerce-monitoring-etl/
├── src/                        # Código-fonte principal da aplicação
│   ├── drivers/                # Conectores externos (HTTP Requester, Database Driver)
│   ├── pipelines/              # Orquestração dos fluxos (BronzePipeline, SilverPipeline)
│   ├── transformations/        # Regras de negócio e limpeza (Lógica de conversão/Regex)
│   ├── utils/                  # Funções auxiliares (File handler, logs, formatadores)
│   ├── models/                 # Definição de schemas e contratos de dados
│   └── config/                 # Configurações globais, DB e Variáveis de ambiente
├── data/                       # Nosso "Data Lake" local dividido por camadas
│   ├── bronze/                     # Dados brutos (Raw JSON) - Origem da verdade
│   ├── silver/                     # Dados limpos e tipados (Parquet) - Pronto para análise
│   └── gold/                       # Dados agregados e KPIs - Pronto para Dashboards
├── notebooks/                  # Experimentos, análise exploratória e prototipagem
├── docs/                       # Documentação técnica, arquitetura e decisões
├── tests/                      # Testes unitários e de integração (Garante a confiabilidade)
├── main.py                     # Ponto de entrada do sistema
├── Dockerfile                  # Receita para criar a imagem do container
├── docker-compose.yml          # Orquestração do Python + Banco de Dados
└── .env                        # Variáveis sensíveis (Senhas, URLs, chaves)
```

## Drivers

A pasta `src/drivers` é responsável pela **interação com fontes externas**.

### HttpRequester
- Realiza requisições HTTP
- Gerencia headers e sessão
- Não contém regras de negócio

### HtmlScrape (Parser)
- Converte HTML bruto em estruturas de dados
- Extrai apenas informações visíveis no HTML
- Não realiza normalizações ou cálculos analíticos

Essa separação garante que mudanças na interface do site não afetem diretamente as regras de negócio.

## Camada de Dados

O projeto utiliza o padrão medalhão (**Bronze / Silver / Gold**).

### Bronze 🥉
- Dados crus, sem tratamento
- Representam exatamente o que foi coletado
- Servem como fonte de reprocessamento

Exemplos:
- `Ingestão de dados` Os dados são armazenados exatamente no formato original, sem transformações complexas, mantendo a integridade original para auditoria.
- `Historização Completa` Mantém o histórico completo de dados. Se uma regra de negócio mudar no futuro, os dados da camada Bronze permitem reprocessar tudo desde o início.
- `Adição de Metadados de Ingestão` Acrescenta colunas de controle, como a hora de chegada do arquivo (timestamp), nome do arquivo de origem, e ID do processo de carga, facilitando a rastreabilidade (data lineage).
- `Isolamento para Reprocessamento` Atua como uma "rede de segurança". Se houver erros nas camadas Silver ou Gold, os engenheiros podem usar a camada Bronze para recriar as camadas superiores sem precisar voltar aos sistemas de origem.
- `Gerenciamento de Schema Evolution` Consegue lidar com mudanças na estrutura dos dados de origem (novas colunas, etc.) sem interromper o pipeline de ingestão.

---

### Silver 🥈
- Dados tratados e normalizados
- Tipos corrigidos (string → número)
- Campos derivados adicionados

Exemplos:
- `Limpeza e Conformidade` Padroniza formatos (datas, moedas), remove nulos indesejados, trata erros de ingesta e aplica regras de qualidade de dados.
- `Desduplicação` Garante que cada registro seja único, eliminando linhas duplicadas que surgiram durante o processo de extração.
- `Estruturação` Transforma arquivos semiestruturados, como JSON ou logs, em tabelas relacionais ou colunares estruturadas, facilitando a consulta.
- `Enriquecimento` Adiciona informações contextuais aos dados, como geolocalização, cruzamento de chaves ou cálculos prévios simples.
- `Aplicação de Schemas`: Define tipos de dados rigorosos (inteiro, string, timestamp) para garantir consistência antes da camada Gold.

---

### Gold 🥇
- Dados prontos para análise e visualização
- Agregações, rankings e métricas
- Utilizados por dashboards e notebooks

## Transformations

A pasta `src/transformations` contém as regras de negócio e tratamentos de dados.

Princípios adotados:
- Nenhuma transformação ocorre na extração
- Dados Bronze nunca são modificados
- Toda regra é explícita e rastreável

Exemplos de transformações:
- conversão de "+10mil vendidos" → 10000
- cálculo de percentual de desconto
- padronização de preços com centavos

## Utils

A pasta `src/utils` contém funções auxiliares reutilizáveis,
como:
- parsing de textos
- conversão de valores monetários
- manipulação de datas
- salvar para bronze
- salvar para silver

Essas funções não dependem de uma fonte específica.

## Models

A pasta `src/models` define contratos de dados, facilitando validação, tipagem e padronização entre camadas.

## Notebooks

A pasta `notebooks/` é utilizada exclusivamente para análise exploratória, visualização e validação dos dados.

Regras:
- notebooks não realizam scraping
- notebooks não alteram dados
- consomem apenas dados Silver ou Gold

## Princípios Arquiteturais

- Separação de responsabilidades
- Rastreabilidade dos dados
- Facilidade de reprocessamento
- Clareza entre dado bruto e dado tratado
- Estrutura preparada para escalar com orquestradores (ex: Airflow)

## Considerações Finais

O projeto pode evoluir facilmente para:
- múltiplas fontes
- execução agendada
- integração com data warehouses
