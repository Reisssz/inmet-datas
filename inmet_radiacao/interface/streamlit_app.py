import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import OUTPUT_FOLDER


st.set_page_config(page_title="☀️ Painel Radiação Solar", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: white; color: #0056b3; }
        h1, h2, h3 { color: #003366; }
    </style>
""", unsafe_allow_html=True)

st.title("☀️ Radiação Solar - Estado do Pará")

if st.button("🔄 Atualizar dados via API"):
    with st.spinner("Conectando à API..."):
        try:
            response = requests.get("http://localhost:8000/coletar")
            if response.status_code == 200:
                st.success("✅ Coleta finalizada com sucesso")
            else:
                st.error("❌ Erro na API")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")

arquivos = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(".CSV")]

dfs = []
for f in arquivos:
    try:
        df = pd.read_csv(os.path.join(OUTPUT_FOLDER, f), sep=";", encoding="utf-8")
        dfs.append(df)
    except:
        pass

if dfs:
    df_concat = pd.concat(dfs, ignore_index=True)
    df_concat["DATA_HORA"] = pd.to_datetime(df_concat["DATA_HORA"], errors="coerce")

    st.dataframe(df_concat.head(100))

    fig = px.line(df_concat, x="DATA_HORA", y="RADIACAO", title="Radiação Solar ao Longo do Tempo")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum dado disponível. Execute a coleta primeiro.")
