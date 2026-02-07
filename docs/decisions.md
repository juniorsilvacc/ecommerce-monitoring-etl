# Decisions Log 📝

Este documento registra as principais decisões técnicas e de arquitetura tomadas ao longo do desenvolvimento do projeto **Ecommerce Monitoring ETL – Mercado Livre**. O objetivo é deixar claro o *porquê* das escolhas, facilitando manutenção, evolução do projeto e avaliação técnica por terceiros.

---

## 1. Uso de Python no Pipeline ETL

**Decisão:** Utilizar Python como linguagem principal do projeto.

**Motivo:**

* Forte ecossistema para ETL (requests, BeautifulSoup, pandas)
* Facilidade de leitura e manutenção
* Linguagem amplamente usada em Engenharia e Análise de Dados
* Boa integração futura com orquestradores (Airflow, Prefect)

---

## 2. Coleta via Requests + BeautifulSoup

**Decisão:** Utilizar `requests` para requisições HTTP e `BeautifulSoup` para parsing do HTML.

**Motivo:**

* Evitar ferramentas pesadas como Selenium
* Menor custo computacional
* Maior controle sobre headers e estrutura da requisição
* Adequado para scraping de páginas estáticas

**Observação:**
O projeto está preparado para evoluir para ferramentas mais robustas caso o site passe a exigir renderização JavaScript.

---

## 3. Adoção da Medallion Architecture

**Decisão:** Estruturar os dados em camadas **Bronze → Silver → Gold**.

**Motivo:**

* Separação clara de responsabilidades
* Facilita debugging e reprocessamentos
* Padrão amplamente utilizado em projetos de dados modernos

**Resumo das camadas:**

* **Bronze:** dados brutos, sem alterações semânticas
* **Silver:** dados limpos, tipados e padronizados
* **Gold:** dados prontos para análise e métricas (futuro)

---

## 4. Manter Dados Brutos (Raw)

**Decisão:** Armazenar campos como `sold_raw` na camada Bronze.

**Motivo:**

* Preservar o dado original exatamente como coletado
* Evitar perda de informação
* Permitir reinterpretação futura das regras de negócio

Exemplo:

```
"sold_raw": "+10mil vendidos"
```

---

## 5. Transformações Apenas na Camada Silver

**Decisão:** Não aplicar regras de negócio nem conversões complexas na extração.

**Motivo:**

* Separar coleta de tratamento
* Facilitar testes e manutenção
* Permitir reaproveitamento do dado bruto

Exemplos de transformações feitas na Silver:

* Conversão de preços para numérico
* Normalização da coluna `vendido`
* Padronização de nomes de colunas

---

## 6. Padronização de Nomes em Português

**Decisão:** Renomear colunas do inglês para português (`price_current` → `preco_atual`).

**Motivo:**

* Facilitar leitura para análises
* Alinhar com contexto de negócio local
* Melhor compreensão em dashboards e relatórios

---

## 7. Tratamento de Valores Nulos

**Decisão:** Aplicar regras explícitas para valores ausentes.

**Motivo:**

* Dados do Mercado Livre são inconsistentes entre produtos
* Necessário garantir estabilidade para análises

**Exemplos:**

* `preco_antigo` nulo → produto sem promoção → usar `preco_atual`
* `avaliacao` nula → preenchida com 0
* `loja` ausente → "Não Informado"

---

## 8. Conversão da Coluna `vendido`

**Decisão:** Converter textos como `+10mil vendidos` em valores inteiros.

**Motivo:**

* Permitir análises quantitativas
* Facilitar agregações e comparações

**Regra aplicada:**

* Identificação da palavra `mil`
* Extração apenas de números
* Multiplicação por 1000 quando necessário

---

## 9. Inclusão de Metadados de Processamento

**Decisão:** Adicionar a coluna `data_processamento` na camada Silver.

**Motivo:**

* Auditoria do pipeline
* Rastreabilidade
* Suporte a reprocessamentos

---

## 10. Estrutura de Pastas por Responsabilidade

**Decisão:** Separar o projeto em camadas claras (`drivers`, `utils`, `data`).

**Motivo:**

* Facilitar escalabilidade
* Tornar o projeto mais profissional
* Seguir boas práticas de Engenharia de Dados

---

## 11. Documentação em Markdown

**Decisão:** Criar arquivos `.md` explicando arquitetura, decisões e transformações.

**Motivo:**

* Facilitar onboarding
* Demonstrar maturidade técnica
* Registrar contexto das decisões

---

## Considerações Finais

Este documento é vivo e deve ser atualizado conforme o projeto evolui. Ele reflete o racional técnico por trás das decisões e reforça o compromisso com boas práticas de Engenharia de Dados.
