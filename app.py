"""
Dashboard — Variação dos Preços de Combustíveis no Brasil (2015–2024)
Projeto G2 • Tema 11 • Análise e Visualização de Dados com Python
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Preços de Combustíveis no Brasil",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETA = {
    "Gasolina": "#e85d04",
    "Diesel":   "#6a4c93",
    "Etanol":   "#2a9d8f",
    "GNV":      "#118ab2",
    "GLP":      "#d62828",
}

REGIAO_CORES = {
    "Norte":        "#2a9d8f",
    "Nordeste":     "#e9c46a",
    "Centro-Oeste": "#f4a261",
    "Sudeste":      "#e76f51",
    "Sul":          "#264653",
}

sns.set_theme(style="whitegrid", rc={"axes.spines.top": False, "axes.spines.right": False})

CAMINHO_CSV_PADRAO = Path(__file__).parent / "dados" / "simulacao_precos_combustiveis_brasil.csv"


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def carregar_csv(caminho_ou_buffer) -> pd.DataFrame:
    df = pd.read_csv(caminho_ou_buffer)
    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = df["ano"].astype(int)
    df["mes"] = df["mes"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Sidebar — upload + filtros
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⛽ Fonte de dados")
    arquivo = st.file_uploader("Enviar CSV alternativo (opcional)", type=["csv"])
    if arquivo is not None:
        df = carregar_csv(arquivo)
        st.success(f"CSV carregado: {len(df):,} linhas")
    else:
        if not CAMINHO_CSV_PADRAO.exists():
            st.error(f"Arquivo não encontrado: {CAMINHO_CSV_PADRAO}")
            st.stop()
        df = carregar_csv(CAMINHO_CSV_PADRAO)

    st.markdown("---")
    st.markdown("### Filtros")

    anos_opts = sorted(df["ano"].unique())
    anos_sel = st.slider(
        "Período (anos)",
        min_value=int(min(anos_opts)),
        max_value=int(max(anos_opts)),
        value=(int(min(anos_opts)), int(max(anos_opts))),
    )

    meses_sel = st.multiselect(
        "Meses",
        options=list(range(1, 13)),
        default=list(range(1, 13)),
        format_func=lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"][m-1],
    )

    regioes_sel = st.multiselect(
        "Regiões",
        options=sorted(df["regiao"].unique()),
        default=sorted(df["regiao"].unique()),
    )

    ufs_disp = sorted(df.loc[df["regiao"].isin(regioes_sel), "uf"].unique())
    ufs_sel = st.multiselect("Estados (UF)", options=ufs_disp, default=ufs_disp)

    combs_sel = st.multiselect(
        "Combustíveis",
        options=sorted(df["combustivel"].unique()),
        default=sorted(df["combustivel"].unique()),
    )

    niveis_sel = st.multiselect(
        "Nível de preço",
        options=["Baixo", "Médio", "Alto", "Crítico"],
        default=["Baixo", "Médio", "Alto", "Crítico"],
    )

    st.markdown("---")
    st.caption(
        "Dados simulados fornecidos pelo professor. "
        "Para análises reais, consulte a [Série Histórica da ANP]"
        "(https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)."
    )

# aplica filtros
mask = (
    df["ano"].between(*anos_sel)
    & df["mes"].isin(meses_sel)
    & df["regiao"].isin(regioes_sel)
    & df["uf"].isin(ufs_sel)
    & df["combustivel"].isin(combs_sel)
    & df["nivel_preco"].isin(niveis_sel)
)
dff = df.loc[mask].copy()


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.title("Preços de combustíveis no Brasil — 2015 a 2024")
st.caption(
    "Como gasolina, diesel, etanol, GNV e GLP evoluíram ao longo de uma década, "
    "comparando regiões, estados e combustíveis."
)

aba_visao, aba_temporal, aba_regional, aba_combustivel, aba_dados = st.tabs(
    ["Visão geral", "Série temporal", "Comparação regional", "Por combustível", "Dados"]
)

if dff.empty:
    st.warning("Nenhum registro com os filtros aplicados.")
    st.stop()


# ---------------------------------------------------------------------------
# Aba 1 — Visão geral
# ---------------------------------------------------------------------------
with aba_visao:
    st.subheader("Indicadores no período filtrado")

    preco_medio = dff["preco_medio"].mean()
    preco_min = dff["preco_medio"].min()
    preco_max = dff["preco_medio"].max()
    volatilidade = dff["preco_medio"].std()

    serie_mensal = dff.groupby("data")["preco_medio"].mean().sort_index()
    variacao_pct = (serie_mensal.iloc[-1] / serie_mensal.iloc[0] - 1) * 100

    comb_mais_caro = (
        dff.groupby("combustivel")["preco_medio"].mean().sort_values(ascending=False).index[0]
    )
    uf_mais_cara = dff.groupby("uf")["preco_medio"].mean().idxmax()
    uf_mais_barata = dff.groupby("uf")["preco_medio"].mean().idxmin()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Preço médio (R$/L)", f"{preco_medio:,.2f}")
    c2.metric("Variação do período", f"{variacao_pct:+.1f}%")
    c3.metric("Volatilidade (desvio)", f"{volatilidade:,.2f}")
    c4.metric("Registros filtrados", f"{len(dff):,}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Combustível mais caro (média)", comb_mais_caro)
    c6.metric("UF mais cara", uf_mais_cara)
    c7.metric("UF mais barata", uf_mais_barata)
    c8.metric("Preço mín. — máx.", f"R$ {preco_min:.2f} — {preco_max:.2f}")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("**Preço médio por combustível**")
        tabela = (
            dff.groupby("combustivel")
            .agg(
                media=("preco_medio", "mean"),
                desvio=("preco_medio", "std"),
                minimo=("preco_minimo", "min"),
                maximo=("preco_maximo", "max"),
            )
            .round(2)
            .sort_values("media", ascending=False)
        )
        st.dataframe(tabela, use_container_width=True)

    with col_b:
        st.markdown("**Distribuição por nível de preço**")
        contagem = dff["nivel_preco"].value_counts().reindex(["Baixo", "Médio", "Alto", "Crítico"])
        fig, ax = plt.subplots(figsize=(6, 4))
        cores = ["#2a9d8f", "#e9c46a", "#f4a261", "#d62828"]
        ax.bar(contagem.index.astype(str), contagem.values, color=cores)
        ax.set_ylabel("Nº de observações")
        ax.set_xlabel("")
        for i, v in enumerate(contagem.values):
            ax.text(i, v, f" {v:,}", ha="center", va="bottom", fontsize=9)
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)

    st.markdown(
        f"""
        > **Leitura rápida.** No recorte atual, o preço médio é de **R$ {preco_medio:.2f}/L**,
        > com variação ponta-a-ponta de **{variacao_pct:+.1f}%**. O combustível com média mais alta
        > é o **{comb_mais_caro}**, e o contraste geográfico mais marcante aparece entre **{uf_mais_cara}**
        > (média mais alta) e **{uf_mais_barata}** (média mais baixa).
        """
    )


# ---------------------------------------------------------------------------
# Aba 2 — Série temporal (séries temporais avançadas: média móvel)
# ---------------------------------------------------------------------------
with aba_temporal:
    st.subheader("Evolução mensal dos preços")

    serie = (
        dff.groupby(["data", "combustivel"], as_index=False)["preco_medio"].mean()
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    for comb, grupo in serie.groupby("combustivel"):
        ax.plot(grupo["data"], grupo["preco_medio"], label=str(comb),
                color=PALETA.get(str(comb), "#333"), linewidth=1.6)
    ax.set_xlabel("")
    ax.set_ylabel("Preço médio (R$/L)")
    ax.legend(frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.markdown("**Média mensal + média móvel de 3 meses**")
    serie_total = dff.groupby("data")["preco_medio"].mean().sort_index()
    mm3 = serie_total.rolling(3, min_periods=1).mean()

    fig2, ax2 = plt.subplots(figsize=(11, 4))
    ax2.plot(serie_total.index, serie_total.values, color="#999", linewidth=1, label="Média mensal")
    ax2.plot(mm3.index, mm3.values, color="#e85d04", linewidth=2, label="Média móvel (3m)")
    ax2.set_ylabel("R$/L")
    ax2.legend(frameon=False)
    fig2.tight_layout()
    st.pyplot(fig2, clear_figure=True)

    col1, col2 = st.columns(2)
    col1.markdown("**Média anual (R$/L)**")
    anual = dff.groupby("ano")["preco_medio"].mean().round(2)
    col1.dataframe(anual.rename("preço médio").to_frame(), use_container_width=True)

    col2.markdown("**Meses com maior variação (%)**")
    maior_var = (
        dff.groupby(["ano", "mes"])["variacao_mensal"].mean()
        .sort_values(ascending=False)
        .head(10)
        .round(2)
    )
    col2.dataframe(maior_var.rename("variação %").to_frame(), use_container_width=True)


# ---------------------------------------------------------------------------
# Aba 3 — Comparação regional
# ---------------------------------------------------------------------------
with aba_regional:
    st.subheader("Diferenças entre regiões e estados")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Preço médio por região**")
        por_regiao = (
            dff.groupby("regiao")["preco_medio"].mean().sort_values(ascending=False).round(2)
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        cores = [REGIAO_CORES.get(r, "#333") for r in por_regiao.index]
        ax.barh(por_regiao.index.astype(str), por_regiao.values, color=cores)
        ax.set_xlabel("R$/L")
        for i, v in enumerate(por_regiao.values):
            ax.text(v, i, f" {v:.2f}", va="center", fontsize=9)
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)

    with col2:
        st.markdown("**Ranking dos estados**")
        por_uf = dff.groupby("uf")["preco_medio"].mean().sort_values(ascending=False).round(2)
        fig, ax = plt.subplots(figsize=(6, 7))
        ax.barh(por_uf.index.astype(str)[::-1], por_uf.values[::-1], color="#264653")
        ax.set_xlabel("R$/L")
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)

    st.markdown("---")
    st.markdown("**Preço médio por região × combustível**")
    pivot = dff.pivot_table(
        index="regiao", columns="combustivel", values="preco_medio", aggfunc="mean"
    ).round(2)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlOrRd", cbar_kws={"label": "R$/L"}, ax=ax)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


# ---------------------------------------------------------------------------
# Aba 4 — Por combustível (séries temporais avançadas: índice base 100)
# ---------------------------------------------------------------------------
with aba_combustivel:
    st.subheader("Perfil de cada combustível")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dispersão do preço (boxplot)**")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ordem = sorted(dff["combustivel"].unique())
        sns.boxplot(
            data=dff, x="combustivel", y="preco_medio",
            order=ordem,
            palette=[PALETA.get(c, "#333") for c in ordem],
            ax=ax,
        )
        ax.set_xlabel("")
        ax.set_ylabel("R$/L")
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)

    with col2:
        st.markdown("**Volatilidade mensal (desvio padrão)**")
        vol = (
            dff.groupby(["ano", "combustivel"])["preco_medio"].std()
            .groupby("combustivel").mean().sort_values(ascending=False).round(3)
        )
        fig, ax = plt.subplots(figsize=(7, 4.5))
        cores = [PALETA.get(str(c), "#333") for c in vol.index]
        ax.bar(vol.index.astype(str), vol.values, color=cores)
        ax.set_ylabel("Desvio padrão médio")
        for i, v in enumerate(vol.values):
            ax.text(i, v, f" {v:.2f}", ha="center", va="bottom", fontsize=9)
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)

    st.markdown("---")
    st.markdown("**Variação acumulada desde o início do período (índice base 100)**")
    base = dff.groupby(["data", "combustivel"])["preco_medio"].mean().reset_index()
    base = base.sort_values(["combustivel", "data"])
    base["indice"] = base.groupby("combustivel")["preco_medio"].transform(lambda s: s / s.iloc[0] * 100)

    fig, ax = plt.subplots(figsize=(11, 4.5))
    for comb, grupo in base.groupby("combustivel"):
        ax.plot(grupo["data"], grupo["indice"], label=str(comb),
                color=PALETA.get(str(comb), "#333"), linewidth=1.6)
    ax.axhline(100, color="#999", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Índice (início = 100)")
    ax.legend(frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.1))
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


# ---------------------------------------------------------------------------
# Aba 5 — Dados brutos
# ---------------------------------------------------------------------------
with aba_dados:
    st.subheader("Tabela filtrada")
    st.caption(f"{len(dff):,} linhas após aplicação dos filtros.")
    st.dataframe(dff, use_container_width=True, height=420)

    csv_bytes = dff.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar CSV filtrado",
        data=csv_bytes,
        file_name="precos_combustiveis_filtrado.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Conclusão executiva
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Conclusão")
st.markdown(
    """
    O dashboard entrega uma leitura em três camadas: **(1)** uma visão agregada com KPIs
    e rankings, **(2)** uma camada temporal com média móvel para suavizar o ruído mensal
    e um índice base 100 para comparar a variação acumulada entre combustíveis, e
    **(3)** cortes regionais e por combustível com volatilidade.

    A base utilizada é **simulada**, o que limita a leitura econômica dos resultados.
    O que o projeto demonstra é o ferramental completo (pandas + matplotlib + seaborn + Streamlit),
    pronto para ser repetido sobre a Série Histórica real da ANP.
    """
)
