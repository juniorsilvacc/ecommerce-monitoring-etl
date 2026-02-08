## 📊 Métricas, Indicadores e KPIs

Este projeto realiza o enriquecimento dos dados por meio da criação de **métricas**, **indicadores** e **KPIs**, com o objetivo de transformar dados brutos em informações úteis para análise e tomada de decisão.

As novas colunas criadas permitem avaliar **ofertas**, **potencial financeiro** e **oportunidades de negócio**, seguindo boas práticas de Data Analytics e BI.

## 🧠 Conceitos Aplicados

### 🔹 Métrica (O "Dado Cru" Calculado)

Métricas são medidas quantitativas simples. No caso, o **Preço Atual, a Quantidade Vendida** e o Faturamento Estimado são métricas.

**Exemplo de código:**
```python
df['faturamento_estimado'] = df['preco_atual'] * df['quantidade_vendida']
```

---

### 🔹 Indicador (Contexto)

Um indicador é uma métrica que aponta para uma tendência. O **Percentual de Desconto** é um ótimo indicador. Ele não apenas diz o preço, mas indica o quão agressiva está sendo a oferta daquela loja.

**Exemplo de código:**
```python
df['percentual_desconto'] = (
        (df['preco_antigo'] - df['preco_atual']) / df['preco_antigo'].clip(lower=0.01)
    ).round(4)
```

---

### 🔹 KPI (Key Performance Indicator)

KPIs são os indicadores **mais importantes** para a estratégia da empresa. Nem todo indicador é um KPI. Se o objetivo do seu projeto for "Identificar as melhores oportunidades de revenda", então o seu KPI principal pode ser o **Top 10 produtos com Desconto > 20%.**

**Exemplo de código:**
```python
df['score_oportunidade'] = (df['avaliacao'] * df['quantidade_vendida']).round(2)
```

**Resumo:**  
Métrica mede → Indicador interpreta → KPI direciona ação.

## Colunas Criadas

### 1️⃣ Percentual de Desconto (Indicador)

```python
df['percentual_desconto'] = (
    (df['preco_antigo'] - df['preco_atual']) 
    / df['preco_antigo'].clip(lower=0.01)
).round(4)
```

**Exemplo:**
Preço Antigo: R$ 100,00
Preço Atual: R$ 80,00
    -> Desconto = 20%

**Descrição:**
Calcula o percentual de desconto aplicado em relação ao preço original do produto.

**Objetivo:**
Identificar ofertas relevantes e comparar produtos de forma proporcional, independentemente do valor absoluto do preço.

**Boas práticas aplicadas:**

- Uso de clip(lower=0.01) para evitar divisão por zero em casos de dados inconsistentes.
- Arredondamento para quatro casas decimais, facilitando análises e visualizações em dashboards.

**Vantagens:**

- Facilita a identificação de promoções reais.
- Permite comparação justa entre produtos de diferentes faixas de preço.

---

### 2️⃣ Faturamento Estimado (Métrica)

```python
df['faturamento_estimado'] = (
    df['preco_atual'] * df['quantidade_vendida']
).round(2)
```

**Exemplo:**
Preço: R$ 50,00
Vendidos: 10
    -> Faturamento = R$ 500,00

**Descrição:**
Representa o volume financeiro estimado gerado por cada produto.

**Objetivo:**
Mensurar o impacto financeiro de cada item com base no preço atual e na quantidade vendida.

**Vantagens:**
- Identificação de produtos com maior relevância financeira.
- Base para análises de receita, rankings e dashboards financeiros.

---

### 3️⃣ Score de Oportunidade (KPI)

```python
df['score_oportunidade'] = (
    df['avaliacao'] * df['vendido']
).round(2)
```

**Exemplo:**
Um ranking de oportunidade baseado em:
- qualidade (avaliação)
- demanda (vendido)

```text
| Produto | Avaliação | Vendido | Score |
| ------- | --------- | ------- | ----- |
| A       | 4.8       | 100     | 480   |
| B       | 3.9       | 300     | 1170  |

Produto B vende mais, mas A pode ser mais estratégico dependendo do objetivo.
```

**Descrição:**
Cria um score estratégico combinando qualidade do produto (avaliação) e demanda (quantidade vendida).

**Objetivo:**
Priorizar produtos com maior potencial de oportunidade comercial.

**Por que é um KPI?**

- Combina múltiplas métricas em um único valor.
- Gera um ranking acionável.
- Apoia decisões estratégicas, como:
    - produtos a serem promovidos
    - foco de investimentos em marketing
    - itens prioritários para monitoramento

**Vantagens:**

- Simplifica a tomada de decisão.
- Facilita análises comparativas em grandes volumes de dados.