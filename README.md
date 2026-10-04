# Preços de combustíveis no Brasil — 2015 a 2024

Projeto G2 • Tema 11 • **Análise e Visualização de Dados com Python**

Análise exploratória e dashboard interativo sobre a variação dos preços de gasolina, diesel, etanol, GNV e GLP no Brasil, por região, estado e ano, com base no dataset simulado fornecido pelo professor.

## O que o projeto entrega

- **Notebook** (`notebooks/analise_precos_combustiveis.ipynb`) com as 10 seções pedidas: introdução, base, leitura, limpeza, engenharia de atributos, EDA, KPIs, visualizações, interpretação e conclusão.
- **Dashboard Streamlit** (`app.py`) com 6 abas: visão geral, série temporal, comparação regional, por combustível, correlações e dados brutos — todas governadas por filtros múltiplos na barra lateral.
- **Página de apresentação** (`index.html`) para publicar no GitHub Pages.
- **Persistência em SQLite** via SQLAlchemy, com consulta SQL ao vivo dentro do dashboard.

## Como rodar localmente

```bash
# criar ambiente (opcional)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# instalar dependências
pip install -r requirements.txt

# rodar o dashboard
streamlit run app.py

# abrir o notebook
jupyter notebook notebooks/analise_precos_combustiveis.ipynb
```

O dashboard abre em `http://localhost:8501`.

## Estrutura

```
projeto-precos-combustiveis/
├── app.py                  # dashboard Streamlit (multipágina via tabs)
├── requirements.txt
├── README.md
├── index.html              # landing para GitHub Pages
├── dados/
│   └── simulacao_precos_combustiveis_brasil.csv
├── notebooks/
│   └── analise_precos_combustiveis.ipynb
├── database/               # SQLite gerado em runtime
└── imagens/
```

## Funcionalidades atendidas

**Intermediárias** (precisa 2 — tem 10):
filtros múltiplos no Streamlit, KPIs dinâmicos, análise temporal, tratamento avançado de dados, integração entre tabelas (pivots), upload de arquivos, dashboard organizado em seções, visualizações comparativas, análises geográficas, gráficos interativos.

**Avançadas** (precisa 2 — tem 5):
persistência em banco (SQLAlchemy + SQLite), dashboard multipágina (6 abas), séries temporais com média móvel, correlação estatística, integração CSV + banco com consulta SQL ao vivo.

## Publicação

| Plataforma | Objetivo | Como fazer |
|---|---|---|
| **GitHub** | código-fonte | criar repo, `git init && git add . && git commit && git push` |
| **GitHub Pages** | página do projeto | nas configurações do repositório → *Pages* → publicar a partir da branch `main`, raiz |
| **Streamlit Community Cloud** | dashboard online | `share.streamlit.io` → *New app* → apontar para o repo e `app.py` |

## Fonte de dados

Dataset simulado fornecido pelo professor em [AlexandreLouzada/Dados-Simulados-G2](https://github.com/AlexandreLouzada/Dados-Simulados-G2).

Para análise com dados reais, a fonte oficial é a [Série Histórica de Preços de Combustíveis da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis). O pipeline do projeto foi escrito de forma a aceitar o CSV real da ANP com ajustes mínimos nos nomes de coluna.

## Observação metodológica

Como os dados são simulados em uma faixa uniforme (R$ 3–R$ 8), as correlações entre preço, inflação e cotação do petróleo ficam próximas de zero, e as diferenças regionais são pequenas. O projeto cumpre o papel de demonstrar o ferramental completo (pandas + matplotlib + seaborn + Streamlit + SQLAlchemy); interpretações econômicas substantivas exigem uma base real.
