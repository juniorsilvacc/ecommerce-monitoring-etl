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

### Tratamento do Preço Antigo

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

## 4. Tratamento da Coluna `vendido`

Problema na camada Bronze

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

## 5. Tratamento da Coluna `loja`

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

## 6. Tratamento da Coluna `envio`

### Problema

O campo de envio pode não estar disponível no momento da coleta.

### Solução

Substituição por `"Consultar Frete"`.

### Motivo

- Representa corretamente o comportamento do marketplace
- Evita inferências erradas (ex: assumir frete grátis)
- Mantém o dado interpretável para o analista

## 7. Tratamento da Coluna `avaliacao`

### Regra aplicada

Valores nulos são preenchidos com `0.0`.

### Justificativa

- Produtos novos podem não ter avaliação
- Zero representa ausência de avaliação, não erro
- Facilita cálculos de média e filtros

## 8. Metadado `data_processamento`

### Por que adicionar essa coluna?

A coluna `data_processamento` indica quando o dado foi transformado.

Benefícios:
- Rastreabilidade
- Auditoria
- Comparação entre cargas
- Diagnóstico de reprocessamentos

Esse campo é essencial em pipelines de dados profissionais.

---

## Considerações Finais

As transformações aplicadas nesta camada:
- respeitam o dado original (Bronze)
- seguem regras explícitas de negócio
- tornam os dados prontos para análise (Silver)

Nenhuma decisão foi tomada apenas por conveniência técnica, todas possuem impacto direto na qualidade analítica dos dados.
