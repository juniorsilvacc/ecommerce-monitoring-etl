# Data Model – Camada Silver

## Visão Geral

Este documento descreve o modelo de dados da camada **Silver** para a fonte Mercado Livre.

O objetivo do modelo é:
- Representar os dados de forma estruturada
- Facilitar análises e agregações
- Garantir clareza semântica dos campos
- Servir como referência para analistas e engenheiros

Os dados aqui descritos já passaram por:
- Limpeza
- Padronização
- Conversão de tipos
- Aplicação de regras de negócio básicas

## Nível do Modelo

- **Camada:** Silver
- **Granularidade:** Produto por coleta
- **Formato:** Parquet
- **Particionamento lógico:** Fonte + data de referência
- **Atualização:** Append (histórico preservado)

Cada linha representa **um produto coletado em um momento específico**.

## Tabela: `mercadolivre_produtos_silver`

## Chaves e Identificadores

### `produto_id`
- **Tipo:** string
- **Descrição:** Identificador único do produto no Mercado Livre
- **Origem:** Extraído da URL / estrutura do site
- **Observação:** Não é chave primária absoluta, pois o mesmo produto pode aparecer em diferentes datas de coleta.

## Atributos Descritivos

### `titulo`
- **Tipo:** string
- **Descrição:** Nome do produto conforme exibido no marketplace
- **Uso:** Análise textual, categorização, buscas

---

### `loja`
- **Tipo:** string
- **Descrição:** Nome da loja ou vendedor responsável pelo produto
- **Valores possíveis:**
  - Nome da loja
  - `"Não Informado"` quando indisponível
- **Uso:** Rankings por vendedor, análise de concentração

---

### `envio`
- **Tipo:** string
- **Descrição:** Informação sobre envio/frete do produto
- **Valores possíveis:**
  - `"Frete grátis"`
  - `"Consultar Frete"`
  - Outros textos fornecidos pelo marketplace
- **Uso:** Análise de competitividade e experiência do consumidor

## Atributos Financeiros

### `preco_atual`
- **Tipo:** float
- **Descrição:** Preço vigente do produto no momento da coleta
- **Observação:** Sempre preenchido
- **Uso:** Métricas de preço, média, mínimo, máximo

---

### `preco_antigo`
- **Tipo:** float
- **Descrição:** Preço original antes de promoção
- **Regra de Negócio:**
  - Quando nulo, recebe o valor de `preco_atual`
- **Uso:** Cálculo de desconto e identificação de promoções

---

## Atributos de Performance

### `avaliacao`
- **Tipo:** float
- **Descrição:** Nota média do produto (0 a 5)
- **Regra de Negócio:**
  - Produtos sem avaliação recebem `0.0`
- **Uso:** Análise de reputação e qualidade percebida

---

### `vendido`
- **Tipo:** integer
- **Descrição:** Quantidade estimada de unidades vendidas
- **Origem:** Campo textual tratado da camada Bronze
- **Transformação aplicada:**
  - Textos como `"+10 mil vendidos"` → `10000`
- **Uso:** Ranking de produtos, análise de popularidade

## Metadados

### `data_processamento`
- **Tipo:** timestamp (string formatada)
- **Descrição:** Data e hora em que o dado foi processado na camada Silver
- **Uso:**
  - Auditoria
  - Rastreabilidade
  - Comparação entre cargas

## Granularidade e Histórico

- O modelo **preserva histórico**
- O mesmo `produto_id` pode aparecer múltiplas vezes
- Cada registro representa o estado do produto no momento da coleta

Isso permite:
- Análise de evolução de preços
- Monitoramento de promoções ao longo do tempo
- Comparações históricas

## Relacionamentos Futuros (Gold)

Este modelo pode ser facilmente expandido para a camada Gold, por exemplo:

- Fato: vendas/popularidade por produto
- Dimensão: produto
- Dimensão: loja
- Dimensão: tempo

## Considerações Finais

Este modelo foi desenhado para:
- Ser simples
- Ser explícito
- Ser escalável

Ele atende tanto análises exploratórias quanto
dashboards e métricas consolidadas, mantendo clareza
e rastreabilidade desde a origem do dado.
