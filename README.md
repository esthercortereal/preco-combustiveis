# Preços de combustíveis no Brasil — 2015 a 2024

Projeto G2 • Tema 11 • **Análise e Visualização de Dados com Python**

Análise exploratória e dashboard interativo sobre a variação dos preços de gasolina, diesel, etanol, GNV e GLP no Brasil, por região, estado e ano.

## O que o projeto entrega

- **Notebook** (`notebooks/analise_precos_combustiveis.ipynb`) com as 10 seções pedidas: introdução, base, leitura, limpeza, engenharia de atributos, EDA, KPIs, visualizações, interpretação e conclusão.
- **Dashboard Streamlit** (`app.py`) com 5 abas: visão geral, série temporal, comparação regional, por combustível e dados brutos — todas governadas por filtros múltiplos na barra lateral.
- **Página de apresentação** (`index.html`) publicada no GitHub Pages.

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

```
projeto-precos-combustiveis/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_precos_combustiveis_brasil.csv
├── notebooks/
│   └── analise_precos_combustiveis.ipynb
├── database/
└── imagens/
```

## Funcionalidades

**Intermediárias:** filtros múltiplos, KPIs dinâmicos, análise temporal, dashboard em seções, visualizações comparativas, análises geográficas, upload de arquivos.

**Avançadas:** dashboard multipágina (5 abas via `st.tabs`) e séries temporais avançadas (média móvel de 3 meses + índice base 100 para variação acumulada).

## Fonte de dados

Dataset simulado fornecido pelo professor. Para análise com dados reais, a fonte oficial é a [Série Histórica de Preços de Combustíveis da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis).

