# 🧹 Transformations – Camada Silver 

## Objetivo das Transformações

As transformações realizadas neste projeto têm como objetivo converter os dados brutos coletados na camada Bronze em dados confiáveis, padronizados e prontos para análise na camada Silver.

Nenhuma regra de negócio é aplicada durante a extração. Todas as decisões de limpeza, padronização e enriquecimento acontecem aqui, garantindo rastreabilidade e reprocessamento.

## Por que os dados mudam de Bronze → Silver?

Na camada Bronze, os dados:
- Refletem exatamente o que foi coletado do site
- Podem conter textos, símbolos, valores nulos
- Não possuem tipagem adequada para análise

Na camada Silver, os dados:
- Possuem nomes padronizados
- Estão tipados corretamente
- Seguem regras explícitas de negócio
- Podem ser usados diretamente em análises e dashboards

## 1. Padronização e Renomeação de Colunas

### Motivo da Renomeação (Inglês → Português)

As colunas foram renomeadas do inglês para o português por três motivos principais:

1. **Padronização do projeto**
   - O contexto do projeto utilizam português
   - Evita mistura de idiomas nos dados finais

2. **Facilidade de leitura e entendimento**
   - Analistas e stakeholders entendem rapidamente o significado
   - Reduz necessidade de documentação extra para nomes óbvios

3. **Clareza semântica**
   - `price_old` → `preco_antigo`
   - `price_current` → `preco_atual`
   - `sold_raw` → `vendido`

Essa decisão impacta positivamente a usabilidade dos dados.

## 2. Conversão de Tipagem (Type Casting)

### Por que converter tipos explicitamente?

Dados coletados via scraping chegam, em sua maioria, como `string`. Para análises corretas, comparações e agregações, é necessário converter os tipos de forma explícita.

Conversões realizadas:
- Identificadores (`produto_id`) → string
- Campos textuais (`titulo`, `loja`, `envio`) → string limpa
- Campos numéricos (`preco_antigo`, `preco_atual`, `avaliacao`) → numérico

Uso de `errors='coerce'`:
- Evita falhas no pipeline
- Converte valores inválidos em `NaN`, permitindo tratamento posterior

## 3. Tratamento de Valores

### Tratamento da Coluna `preco_antigo`

Quando `preco_antigo` é nulo, ele recebe o valor de `preco_atual`.

### Justificativa de Negócio

No Mercado Livre:
- Se não existe preço antigo, o produto **não está em promoção**
- O preço atual representa o preço real do produto

Ao aplicar essa regra:
- Mantemos coerência entre os preços
- Facilitamos cálculos de desconto
- Evitamos valores nulos que quebrariam análises

Essa abordagem permite identificar promoções de forma indireta:
- Se `preco_antigo == preco_atual` → sem desconto
- Se `preco_antigo > preco_atual` → produto em promoção

---

### Tratamento da Coluna `quantidade_vendida`

### Problema na camada Bronze

O campo `sold_raw` vem em formatos variados, por exemplo:
- "+10 mil vendidos"
- "500 vendidos"
- "+1mil"

Esse formato textual não é adequado para análise quantitativa.

### Estratégia de Transformação

1. Converter para lowercase e limpar espaços
2. Identificar registros que contêm a palavra `"mil"`
3. Remover qualquer caractere que não seja número
4. Converter para numérico
5. Multiplicar por 1000 apenas quando `"mil"` estava presente
6. Converter o resultado final para inteiro

### Resultado

A coluna `vendido` passa a representar:
- número absoluto de unidades vendidas
- pronta para agregações, rankings e análises

Essa abordagem mantém a **intenção original do dado**, sem perder informação.

---

### Criação do Indicador `percentual_desconto`

#### Objetivo

Mensurar o percentual de desconto aplicado em relação ao preço original do produto, permitindo identificar promoções reais e comparar ofertas de forma proporcional.

#### Regra de Cálculo
- (preco_antigo - preco_atual) / preco_antigo

#### Tratamento Aplicado

- O valor de `preco_antigo` é limitado a um mínimo de `0.01` (`clip(lower=0.01)`)
- Essa abordagem evita divisão por zero em casos de dados inconsistentes
- O resultado é arredondado para 4 casas decimais

#### Justificativa

- Garante estabilidade do pipeline
- Permite análise proporcional independente do preço absoluto
- Facilita uso em dashboards e rankings de oferta

**Classificação:** Indicador

---

### Criação da Métrica `faturamento_estimado`

#### Objetivo

Estimar o volume financeiro gerado por cada produto no momento da coleta.

#### Regra de Cálculo
   - preco_atual * quantidade_vendida

#### Tratamento Aplicado

- Resultado arredondado para 2 casas decimais
- Nenhuma agregação entre registros é realizada

#### Justificativa

- Representa impacto financeiro direto
- Serve como base para análises de receita
- Facilita priorização de produtos por volume financeiro

**Classificação:** Métrica

---

### Criação do KPI `score_oportunidade`

#### Objetivo

Criar um indicador estratégico que combine **popularidade** e **qualidade percebida** do produto.

#### Regra de Cálculo
- avaliacao * quantidade_vendida

#### Tratamento Aplicado

- Produtos sem avaliação recebem valor `0.0`
- Resultado arredondado para 2 casas decimais

#### Justificativa

- Combina métricas independentes em um único score
- Gera um ranking acionável
- Apoia decisões como:
  - priorização de produtos
  - foco de campanhas
  - identificação de oportunidades comerciais

**Classificação:** KPI

---

### Tratamento da Coluna `loja`

### Problema

Alguns produtos não apresentam o nome da loja, resultando em:
- `None`
- valores nulos

### Solução

Substituição por `"Não Informado"`.

### Motivo

- Evita valores nulos em análises categóricas
- Permite agrupar produtos sem loja identificada
- Mantém consistência visual em relatórios e dashboards

---

### Tratamento da Coluna `envio`

### Problema

O campo de envio pode não estar disponível no momento da coleta.

### Solução

Substituição por `"Consultar Frete"`.

### Motivo

- Representa corretamente o comportamento do marketplace
- Evita inferências erradas (ex: assumir frete grátis)
- Mantém o dado interpretável para o analista

---

### Tratamento da Coluna `avaliacao`

### Regra aplicada

Valores nulos são preenchidos com `0.0`.

### Justificativa

- Produtos novos podem não ter avaliação
- Zero representa ausência de avaliação, não erro
- Facilita cálculos de média e filtros

## Metadado `data_processamento`

### Por que adicionar essa coluna?

A coluna `data_processamento` indica quando o dado foi transformado.

Benefícios:
- Rastreabilidade
- Auditoria
- Comparação entre cargas
- Diagnóstico de reprocessamentos

Esse campo é essencial em pipelines de dados profissionais.

## Considerações Finais

As transformações aplicadas nesta camada:
- respeitam o dado original (Bronze)
- seguem regras explícitas de negócio
- tornam os dados prontos para análise (Silver)

Nenhuma decisão foi tomada apenas por conveniência técnica, todas possuem impacto direto na qualidade analítica dos dados.
