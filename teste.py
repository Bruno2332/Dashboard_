import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("📊 Dashboard de Vendas Interativo")

# Upload do CSV
arquivo = st.file_uploader("Envie seu arquivo CSV de vendas", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)


    st.sidebar.header("⚙️ Opções de Visualização")
    opcao = st.sidebar.selectbox(
        "Selecione o tipo de análise:",
        [
            "Vendedor que mais vendeu (quantidade)",
            "Região que mais fatura (valor total)",
            "Média de vendas por vendedor",
            "Média de vendas por região"
        ]
    )

    # --- Lógica das opções ---
    if opcao == "Vendedor que mais vendeu (quantidade)":
        resultado = df["Vendedor"].value_counts().reset_index()
        resultado.columns = ["Vendedor", "Quantidade de vendas"]
        st.subheader("📈 Vendedor com maior número de vendas")
        fig = px.bar(
            resultado,
            x="Vendedor",
            y="Quantidade de vendas",
            color="Vendedor",
            title="Vendas por Vendedor"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif opcao == "Região que mais fatura (valor total)":
        resultado = df.groupby("Região")["Valor"].sum().sort_values(ascending=False).reset_index()
        st.subheader("💰 Faturamento total por região")
        fig = px.bar(
            resultado,
            x="Região",
            y="Valor",
            color="Região",
            title="Faturamento por Região"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif opcao == "Média de vendas por vendedor":
        resultado = df.groupby("Vendedor")["Valor"].mean().sort_values(ascending=False).reset_index()
        resultado["Valor"] = resultado["Valor"].round(2)
        st.subheader("📊 Média de valor das vendas por vendedor")
        fig = px.bar(
            resultado,
            x="Vendedor",
            y="Valor",
            color="Vendedor",
            title="Média de Vendas por Vendedor"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif opcao == "Média de vendas por região":
        resultado = df.groupby("Região")["Valor"].mean().sort_values(ascending=False).reset_index()
        resultado["Valor"] = resultado["Valor"].round(2)
        st.subheader("🌎 Média de valor das vendas por região")
        fig = px.bar(
            resultado,
            x="Região",
            y="Valor",
            color="Região",
            title="Média de Vendas por Região"
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Destaque adicional ---
    st.markdown("---")
    st.write("### 📋 Dados brutos (prévia)")
    st.dataframe(df.head(10))

