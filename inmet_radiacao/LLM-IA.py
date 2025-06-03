import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Analisador de Radiação", layout="centered")

st.title("☀️ Painel de Análise de Radiação Solar")
st.markdown("Digite um comando como se fosse no ChatGPT:")

# Função para carregar os dados
def carregar_dados(caminho):
    df = pd.read_csv(caminho, sep=",", decimal=",")
    df["DATA_HORA"] = pd.to_datetime(df["DATA_HORA"], errors='coerce')
    df["RADIACAO"] = pd.to_numeric(df["RADIACAO"], errors="coerce")
    return df

# Função de análise
def calcular_media_por_hora(df, ano, mes):
    df_filtrado = df[(df["DATA_HORA"].dt.year == ano) & (df["DATA_HORA"].dt.month == mes)]
    df_filtrado["HORA"] = df_filtrado["DATA_HORA"].dt.hour
    medias = df_filtrado.groupby("HORA")["RADIACAO"].mean().reset_index()
    return medias

# Upload do CSV
uploaded_file = st.file_uploader("📁 Envie seu arquivo CSV de radiação", type=["csv"])

# Entrada de prompt estilo ChatGPT
prompt = st.text_input("💬 Faça uma pergunta:", placeholder="Ex: Qual foi a radiação do mês 01 de 2021?" )

# Entrada de parâmetros do painel solar
st.sidebar.header("⚙️ Configurações do Painel Solar")
area_painel = st.sidebar.number_input("Área total dos painéis (m²)", min_value=0.0, value=10.0, step=1.0)
eficiencia = st.sidebar.slider("Eficiência do sistema (%)", min_value=0, max_value=100, value=15) / 100

# Inicializa variáveis
df = None
medias = None

if uploaded_file:
    df = carregar_dados(uploaded_file)

    if prompt:
        # Detecção simples do mês e ano na frase
        import re
        match = re.search(r"m[eê]s\s*(\d{1,2})\s*de\s*(\d{4})", prompt)
        if match:
            mes = int(match.group(1))
            ano = int(match.group(2))
            medias = calcular_media_por_hora(df, ano, mes)

            st.success(f"Médias horárias de radiação para {mes:02d}/{ano}:")
            st.dataframe(medias)

            # Conversão para kWh
            medias["RADIACAO_KWH"] = medias["RADIACAO"] / 1000
            total_kwh_m2_mes = medias["RADIACAO_KWH"].sum() * 30  # estimando 30 dias

            st.markdown(f"\n🔋 **Estimativa de radiação total no mês:** {total_kwh_m2_mes:.2f} kWh/m²")

            # Cálculo de geração com base no painel
            energia_gerada_kwh = total_kwh_m2_mes * area_painel * eficiencia
            st.markdown(f"\n⚡ **Energia gerada estimada no mês:** {energia_gerada_kwh:.2f} kWh")
            


            # Botão para salvar CSV
            nome_arquivo = f"media_radiacao_{ano}_{mes:02d}.csv"
            csv_data = medias.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Baixar média mensal em CSV",
                data=csv_data,
                file_name=nome_arquivo,
                mime='text/csv' )
        else:
            st.warning("❗ Tente usar um comando como: 'Qual foi a radiação do mês 01 de 2021?'")
else:
    st.info("Envie um arquivo para começar.")
    